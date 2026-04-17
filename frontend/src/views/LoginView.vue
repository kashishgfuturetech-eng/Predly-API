<template>
  <div class="login-page">
    <!-- Backgrounds -->
    <div class="login-page__grid"></div>
    <div class="login-page__orb login-page__orb--orange"></div>
    <div class="login-page__orb login-page__orb--blue"></div>

    <!-- Card -->
    <div class="login-page__card animate-fade-up">

      <!-- Top accent bar -->
      <div class="login-page__accent-bar"></div>

      <div class="login-page__inner">

        <!-- Brand -->
        <div class="login-page__brand">
          <div class="login-page__logo-mark">
            <span class="material-symbols-outlined" style="font-size:22px">hub</span>
          </div>
          <h1 class="login-page__title font-headline">Predly</h1>
          <p class="login-page__subtitle label-sm">Secure terminal entry for authorized agents.</p>
        </div>

        <!-- Divider -->
        <div class="login-page__divider"></div>

        <!-- Error banner -->
        <div v-if="errorMsg" class="login-page__error animate-fade-up">
          <span class="material-symbols-outlined" style="font-size:14px">error_outline</span>
          {{ errorMsg }}
        </div>

        <!-- Google button -->
        <button class="login-page__google-btn" @click="loginWithGoogle" :disabled="isRedirecting">
          <span v-if="isRedirecting" class="login-page__spinner"></span>
          <template v-else>
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/>
              <path d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853"/>
              <path d="M3.964 10.707A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z" fill="#FBBC05"/>
              <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 6.293C4.672 4.166 6.656 3.58 9 3.58z" fill="#EA4335"/>
            </svg>
          </template>
          <span>{{ isRedirecting ? 'Authenticating…' : 'Continue with Google' }}</span>
        </button>

        <!-- Info row -->
        <div class="login-page__info-row">
          <span class="material-symbols-outlined" style="font-size:13px;color:var(--text-muted)">lock</span>
          <span class="login-page__info-text label-sm">OAuth 2.0 · Encrypted session · No passwords stored</span>
        </div>

        <!-- Divider -->
        <div class="login-page__divider"></div>

        <!-- Footer links -->
        <div class="login-page__footer">
          <a href="#" class="login-page__footer-link label-sm">System Protocol</a>
          <span class="login-page__footer-dot"></span>
          <a href="#" class="login-page__footer-link label-sm">Encryption Logic</a>
        </div>

      </div>
    </div>

    <!-- Status bar -->
    <div class="login-page__status">
      <span class="login-page__status-dot"></span>
      <span class="login-page__status-text font-mono">LOCAL NODE ACTIVE: V4.2 OBSIDIAN</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { setToken, consumePendingProject, consumeRedirectAfterLogin } from '../auth.js'

const router = useRouter()
const route = useRoute()

const isRedirecting = ref(false)
const errorMsg = ref('')

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'

onMounted(() => {
  const token = route.query.token
  const error = route.query.error

  if (error) {
    const msgs = {
      oauth_cancelled: 'Google sign-in was cancelled.',
      oauth_failed: 'Google sign-in failed. Please try again.',
      token_exchange_failed: 'Authentication failed. Please try again.',
      userinfo_failed: 'Could not retrieve account info. Please try again.',
      google_not_configured: 'Google OAuth is not configured on this server.',
    }
    errorMsg.value = msgs[error] || 'Authentication failed.'
    return
  }

  if (token) {
    setToken(token)
    const pendingProject = consumePendingProject()
    const redirectPath = consumeRedirectAfterLogin()
    if (pendingProject) {
      router.replace({ name: 'Main', params: { projectId: pendingProject } })
    } else if (redirectPath) {
      router.replace(redirectPath)
    } else {
      router.replace({ name: 'Home' })
    }
  }
})

function loginWithGoogle() {
  isRedirecting.value = true
  window.location.href = `${API_BASE}/auth/google`
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #0a0c0f;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* Grid */
.login-page__grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 181, 158, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 181, 158, 0.025) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* Orbs */
.login-page__orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.login-page__orb--orange {
  width: 700px; height: 700px;
  top: -300px; right: -200px;
  background: radial-gradient(circle, rgba(255, 90, 31, 0.22) 0%, transparent 70%);
}
.login-page__orb--blue {
  width: 550px; height: 550px;
  bottom: -200px; left: -200px;
  background: radial-gradient(circle, rgba(14, 63, 174, 0.2) 0%, transparent 70%);
}

/* Card */
.login-page__card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  margin: 1.5rem;
  background: rgba(18, 22, 28, 0.85);
  border: 1px solid rgba(171, 137, 127, 0.15);
  border-radius: var(--radius-xl, 16px);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow:
    0 32px 80px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 181, 158, 0.03),
    0 -1px 0 0 rgba(255, 181, 158, 0.06) inset;
  overflow: hidden;
}

/* Top accent gradient line */
.login-page__accent-bar {
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, #FF5A1F 40%, #FF8C5A 60%, transparent 100%);
  opacity: 0.7;
}

.login-page__inner {
  padding: 2rem 2rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Brand */
.login-page__brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0 0.25rem;
}
.login-page__logo-mark {
  width: 48px; height: 48px;
  border-radius: var(--radius-md, 10px);
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 6px 20px rgba(255, 90, 31, 0.35);
  margin-bottom: 0.25rem;
}
.login-page__title {
  font-size: 1.625rem;
  font-weight: 700;
  color: var(--text-primary, #f0f0f0);
  margin: 0;
  letter-spacing: -0.02em;
}
.login-page__subtitle {
  color: var(--text-muted, rgba(255,255,255,0.38));
  text-align: center;
}

/* Divider */
.login-page__divider {
  height: 1px;
  background: rgba(171, 137, 127, 0.1);
}

/* Error */
.login-page__error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  background: rgba(239, 68, 68, 0.07);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius-md, 10px);
  color: #f87171;
  font-size: 0.8125rem;
}

/* Google button — matches project's primary action style */
.login-page__google-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.8125rem 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(171, 137, 127, 0.22);
  border-radius: var(--radius-md, 10px);
  color: var(--text-primary, #f0f0f0);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-headline, inherit);
  letter-spacing: 0.01em;
  backdrop-filter: blur(8px);
}
.login-page__google-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 90, 31, 0.3);
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.1);
  transform: translateY(-1px);
}
.login-page__google-btn:active:not(:disabled) { transform: translateY(0); }
.login-page__google-btn:disabled { opacity: 0.55; cursor: not-allowed; }

/* Info row */
.login-page__info-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
}
.login-page__info-text {
  color: var(--text-muted, rgba(255,255,255,0.3));
  text-align: center;
}

/* Footer */
.login-page__footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}
.login-page__footer-link {
  color: var(--text-muted, rgba(255,255,255,0.25));
  text-decoration: none;
  letter-spacing: 0.06em;
  transition: color 0.15s;
  text-transform: uppercase;
  font-size: 0.625rem;
}
.login-page__footer-link:hover { color: var(--text-secondary, rgba(255,255,255,0.5)); }
.login-page__footer-dot {
  width: 3px; height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
}

/* Spinner */
.login-page__spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-top-color: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Status bar */
.login-page__status {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 1;
  background: rgba(16, 20, 25, 0.7);
  border: 1px solid rgba(171, 137, 127, 0.12);
  border-radius: 999px;
  padding: 0.3rem 0.875rem;
  backdrop-filter: blur(8px);
}
.login-page__status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 6px rgba(74, 222, 128, 0.7);
  animation: pulse-g 2s ease-in-out infinite;
  flex-shrink: 0;
}
@keyframes pulse-g { 0%,100%{opacity:1} 50%{opacity:0.45} }
.login-page__status-text {
  font-size: 0.5625rem;
  letter-spacing: 0.1em;
  color: rgba(255, 255, 255, 0.3);
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.55s cubic-bezier(0.4, 0, 0.2, 1) both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
