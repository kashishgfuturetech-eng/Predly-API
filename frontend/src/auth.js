const TOKEN_KEY = 'predly_auth_token'
const PENDING_PROJECT_KEY = 'predly_pending_project'
const REDIRECT_AFTER_LOGIN_KEY = 'predly_redirect_after_login'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
}

export function isAuthenticated() {
  const token = getToken()
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp > Date.now() / 1000
  } catch {
    return false
  }
}

export function getUser() {
  const token = getToken()
  if (!token) return null
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      email: payload.email,
      name: payload.name,
      picture: payload.picture,
    }
  } catch {
    return null
  }
}

export function setPendingProject(projectId) {
  localStorage.setItem(PENDING_PROJECT_KEY, projectId)
}

export function consumePendingProject() {
  const id = localStorage.getItem(PENDING_PROJECT_KEY)
  localStorage.removeItem(PENDING_PROJECT_KEY)
  return id
}

export function setRedirectAfterLogin(path) {
  localStorage.setItem(REDIRECT_AFTER_LOGIN_KEY, path)
}

export function consumeRedirectAfterLogin() {
  const path = localStorage.getItem(REDIRECT_AFTER_LOGIN_KEY)
  localStorage.removeItem(REDIRECT_AFTER_LOGIN_KEY)
  return path
}

export function logout() {
  clearAuth()
  localStorage.removeItem(PENDING_PROJECT_KEY)
  localStorage.removeItem(REDIRECT_AFTER_LOGIN_KEY)
  window.location.href = '/'
}
