#!/usr/bin/env python3
"""
Promote or demote a user to/from the admin role.

Usage (from project root):
  python scripts/set_admin.py admin@predly.engine
  python scripts/set_admin.py admin@predly.engine --role user   # demote back

Must be run from the backend/ directory or with PYTHONPATH set.
"""

import argparse
import sys
import os

# Allow running directly without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.user_store import set_user_role, get_user_role, email_exists


def main():
    parser = argparse.ArgumentParser(description='Set a user role in Predly')
    parser.add_argument('email', help='User email address')
    parser.add_argument('--role', default='admin',
                        choices=['admin', 'user', 'senior_architect',
                                 'ai_specialist', 'observer', 'data_engineer'],
                        help='Role to assign (default: admin)')
    args = parser.parse_args()

    email = args.email.strip().lower()
    if not email_exists(email):
        print(f'❌  User "{email}" not found. Have them register first via the app.')
        sys.exit(1)

    current = get_user_role(email)
    if current == args.role:
        print(f'ℹ️   "{email}" already has role "{args.role}". Nothing changed.')
        sys.exit(0)

    ok = set_user_role(email, args.role)
    if ok:
        print(f'✅  "{email}" promoted from "{current}" → "{args.role}"')
    else:
        print(f'❌  Update failed for "{email}"')
        sys.exit(1)


if __name__ == '__main__':
    main()