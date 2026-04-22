"""
Google OAuth + JWT authentication blueprint
"""

import time
import requests
from urllib.parse import urlencode

import jwt
from flask import Blueprint, redirect, request, jsonify, current_app

auth_bp = Blueprint('auth', __name__)

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def _create_jwt(user_info: dict) -> str:
    payload = {
        'sub': user_info['sub'],
        'email': user_info['email'],
        'name': user_info.get('name', ''),
        'picture': user_info.get('picture', ''),
        'is_admin': user_info.get('is_admin', False),
        'role': user_info.get('role', 'user'),
        'iat': int(time.time()),
        'exp': int(time.time()) + 86400 * 7,  # 7 days
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except jwt.PyJWTError:
        return None


@auth_bp.route('/google')
def google_login():
    client_id = current_app.config.get('GOOGLE_CLIENT_ID', '')
    if not client_id:
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/login?error=google_not_configured")

    callback_url = request.host_url.rstrip('/') + '/api/auth/google/callback'
    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'select_account',
        'state': request.args.get('state', ''),
    }
    return redirect(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@auth_bp.route('/google/callback')
def google_callback():
    frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
    code = request.args.get('code')
    if not code:
        return redirect(f"{frontend_url}/login?error=oauth_cancelled")

    client_id = current_app.config.get('GOOGLE_CLIENT_ID', '')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET', '')
    backend_url = current_app.config.get('BACKEND_URL', request.host_url.rstrip('/'))
    callback_url = backend_url + '/api/auth/google/callback'

    token_resp = requests.post(GOOGLE_TOKEN_URL, data={
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': callback_url,
        'grant_type': 'authorization_code',
    }, timeout=10)

    if not token_resp.ok:
        return redirect(f"{frontend_url}/login?error=token_exchange_failed")

    access_token = token_resp.json().get('access_token')
    if not access_token:
        return redirect(f"{frontend_url}/login?error=no_access_token")

    userinfo_resp = requests.get(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=10,
    )

    if not userinfo_resp.ok:
        return redirect(f"{frontend_url}/login?error=userinfo_failed")

    user_info = userinfo_resp.json()
    email = (user_info.get('email') or '').strip().lower()

    from ..services.user_store import email_exists, get_user_role, update_last_session, _connect
    if not email_exists(email):
        with _connect() as conn:
            conn.execute(
                'INSERT INTO users (email, passkey_hash, role, status) VALUES (?, ?, ?, ?)',
                (email, '', 'user', 'active'),
            )
            conn.commit()

    update_last_session(email)
    role = get_user_role(email)
    user_info['role'] = role
    user_info['is_admin'] = (role == 'admin')

    token = _create_jwt(user_info)
    state = request.args.get('state', '')
    if state == 'admin' or role == 'admin':
        return redirect(f"{frontend_url}/admin-login?token={token}")
    return redirect(f"{frontend_url}/login?token={token}")


@auth_bp.route('/me')
def me():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'error': 'No token provided'}), 401

    payload = verify_token(auth_header[7:])
    if not payload:
        return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

    return jsonify({'success': True, 'data': {
        'email': payload['email'],
        'name': payload['name'],
        'picture': payload['picture'],
    }})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    passkey = data.get('passkey') or ''

    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'success': False, 'error': 'Please enter a valid email address.'}), 400
    if len(passkey) < 6:
        return jsonify({'success': False, 'error': 'Passkey must be at least 6 characters.'}), 400

    from ..services.user_store import create_user
    ok, reason = create_user(email, passkey)
    if not ok:
        return jsonify({'success': False, 'error': reason}), 409

    user_info = {'sub': f'local:{email}', 'email': email, 'name': email.split('@')[0], 'picture': ''}
    token = _create_jwt(user_info)
    return jsonify({'success': True, 'data': {'token': token}})


@auth_bp.route('/credentials', methods=['POST'])
def credentials_login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    passkey = data.get('passkey') or ''

    if not email or not passkey:
        return jsonify({'success': False, 'error': 'Email and passkey are required.'}), 400

    from ..services.user_store import verify_user, get_user_role, update_last_session
    if not verify_user(email, passkey):
        return jsonify({'success': False, 'error': 'Invalid email or passkey.'}), 401

    update_last_session(email)
    role = get_user_role(email)
    is_admin = (role == 'admin')
    user_info = {
        'sub': f'local:{email}', 'email': email,
        'name': email.split('@')[0], 'picture': '',
        'is_admin': is_admin, 'role': role,
    }
    token = _create_jwt(user_info)
    return jsonify({'success': True, 'data': {'token': token, 'is_admin': is_admin, 'role': role}})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out'})