<template>
  <div class="al-page">
    <!-- Neural-net particle background -->
    <canvas ref="canvas" class="al-canvas"></canvas>
    <!-- Radial glow -->
    <div class="al-glow al-glow--top"></div>
    <div class="al-glow al-glow--bottom"></div>

    <!-- Brand header -->
    <header class="al-brand">
      <div class="al-logo-mark">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <path d="M11 2L20 7V15L11 20L2 15V7L11 2Z" stroke="#FF5A1F" stroke-width="1.5" fill="none"/>
          <path d="M11 6L16 9V13L11 16L6 13V9L11 6Z" fill="#FF5A1F" opacity="0.6"/>
        </svg>
      </div>
      <span class="al-brand-name">Predly<span class="al-brand-dot">.</span>Engine</span>
    </header>

    <!-- Page title -->
    <div class="al-page-title">
      <h1 class="al-heading">Admin Portal</h1>
      <p class="al-subheading">Access the Obsidian Architect Protocol<br>with secure credentials.</p>
    </div>

    <!-- Card -->
    <div class="al-card">
      <div class="al-card__fingerprint">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M12 1C7.03 1 3 5.03 3 10c0 3.1 1.52 5.85 3.87 7.56M12 1c4.97 0 9 4.03 9 9 0 3.1-1.52 5.85-3.87 7.56M12 1v4m0 18v-4" stroke="rgba(255,255,255,0.2)" stroke-width="1.2" stroke-linecap="round"/>
          <path d="M8 10c0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.5-.83 2.81-2.05 3.5" stroke="rgba(255,90,31,0.6)" stroke-width="1.2" stroke-linecap="round"/>
          <circle cx="12" cy="10" r="1.5" fill="#FF5A1F" opacity="0.8"/>
        </svg>
      </div>

      <!-- Error -->
      <div v-if="errorMsg" class="al-error">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="6" stroke="#f87171" stroke-width="1.2"/>
          <path d="M7 4v3M7 9.5v.5" stroke="#f87171" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
        {{ errorMsg }}
      </div>

      <!-- USER IDENTITY -->
      <div class="al-field">
        <label class="al-label">USER IDENTITY</label>
        <input
          v-model="email"
          type="email"
          class="al-input"
          placeholder="admin@predly.engine"
          autocomplete="username"
          @keyup.enter="focusPassword"
        />
      </div>

      <!-- SECURITY KEY -->
      <div class="al-field">
        <div class="al-label-row">
          <label class="al-label">SECURITY KEY</label>
          <button class="al-recover" type="button">RECOVER</button>
        </div>
        <input
          ref="passwordRef"
          v-model="password"
          type="password"
          class="al-input"
          placeholder="••••••••••••"
          autocomplete="current-password"
          @keyup.enter="handleLogin"
        />
      </div>

      <!-- CTA -->
      <button
        class="al-cta"
        :class="{ 'al-cta--loading': loading }"
        :disabled="loading"
        @click="handleLogin"
      >
        <span v-if="loading" class="al-spinner"></span>
        <template v-else>
          INITIALIZE SESSION
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </template>
      </button>

      <!-- Divider -->
      <div class="al-divider-row">
        <span class="al-divider-line"></span>
        <span class="al-divider-text">AUTHENTICATION</span>
        <span class="al-divider-line"></span>
      </div>

      <!-- Google federated -->
      <button class="al-google" @click="loginWithGoogle" :disabled="loading">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/>
          <path d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853"/>
          <path d="M3.964 10.707A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z" fill="#FBBC05"/>
          <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 6.293C4.672 4.166 6.656 3.58 9 3.58z" fill="#EA4335"/>
        </svg>
        Federated Identity
      </button>

      <!-- User login link -->
      <p class="al-switch">
        Not an admin?
        <router-link to="/login" class="al-switch-link">User login →</router-link>
      </p>
    </div>

    <!-- Status bar -->
    <div class="al-status">
      <span class="al-status-dot"></span>
      <span class="al-status-text">SECURITY ENGINE: NOMINAL</span>
    </div>

    <!-- Footer -->
    <footer class="al-footer">
      <span>© 2024 PREDLY TECHNOLOGY /</span>
      <span class="al-footer-ver">A.A.P.V4.0.2</span>
      <span class="al-footer-links">
        <a href="#">ARCHITECTURE</a>
        <a href="#">PRIVACY</a>
        <a href="#">L-SUPPORT</a>
      </span>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { setToken, consumeRedirectAfterLogin } from '../auth.js'

const router   = useRouter()
const route    = useRoute()
const canvas   = ref(null)
const passwordRef = ref(null)

const email    = ref('')
const password = ref('')
const loading  = ref(false)
const errorMsg = ref('')

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'

// ── Neural-net canvas ────────────────────────────────────────────────────────
let animId = null
function initCanvas() {
  const cvs = canvas.value
  if (!cvs) return
  const ctx = cvs.getContext('2d')
  const W = () => { cvs.width = window.innerWidth; cvs.height = window.innerHeight }
  W()
  window.addEventListener('resize', W)

  const NODES = 60
  const nodes = Array.from({ length: NODES }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    r:  Math.random() * 2 + 1,
  }))

  function draw() {
    ctx.clearRect(0, 0, cvs.width, cvs.height)
    nodes.forEach(n => {
      n.x += n.vx; n.y += n.vy
      if (n.x < 0 || n.x > cvs.width)  n.vx *= -1
      if (n.y < 0 || n.y > cvs.height) n.vy *= -1
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2)
      ctx.fillStyle = 'rgba(255,90,31,0.35)'
      ctx.fill()
    })
    for (let i = 0; i < NODES; i++) {
      for (let j = i + 1; j < NODES; j++) {
        const dx = nodes[i].x - nodes[j].x
        const dy = nodes[i].y - nodes[j].y
        const d  = Math.sqrt(dx * dx + dy * dy)
        if (d < 120) {
          ctx.beginPath()
          ctx.moveTo(nodes[i].x, nodes[i].y)
          ctx.lineTo(nodes[j].x, nodes[j].y)
          ctx.strokeStyle = `rgba(255,90,31,${0.12 * (1 - d / 120)})`
          ctx.lineWidth = 0.6
          ctx.stroke()
        }
      }
    }
    animId = requestAnimationFrame(draw)
  }
  draw()
}

onMounted(() => {
  initCanvas()

  // Handle OAuth redirect back
  const token = route.query.token
  const error = route.query.error
  if (error) {
    errorMsg.value = 'Federated authentication failed. Try credentials.'
    return
  }
  if (token) {
    // Decode payload to verify admin flag before granting access
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (!payload.is_admin) {
        errorMsg.value = 'This Google account does not have admin privileges.'
        return
      }
    } catch {
      errorMsg.value = 'Invalid token received.'
      return
    }
    setToken(token)
    const redirect = consumeRedirectAfterLogin()
    router.replace(redirect || { name: 'AdminDashboard' })
  }
})
onUnmounted(() => { if (animId) cancelAnimationFrame(animId) })

function focusPassword() { passwordRef.value?.focus() }

async function handleLogin() {
  errorMsg.value = ''
  const em = email.value.trim().toLowerCase()
  const pw = password.value

  if (!em || !pw) {
    errorMsg.value = 'Both fields are required.'
    return
  }
  loading.value = true
  try {
    const res  = await fetch(`${API_BASE}/auth/credentials`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: em, passkey: pw }),
    })
    const body = await res.json()
    if (!res.ok || !body.success) {
      errorMsg.value = body.error || 'Authentication failed.'
      return
    }
    if (!body.data.is_admin) {
      errorMsg.value = 'This account does not have admin privileges.'
      return
    }
    setToken(body.data.token)
    const redirect = consumeRedirectAfterLogin()
    router.replace(redirect || { name: 'AdminDashboard' })
  } catch {
    errorMsg.value = 'Network error. Please try again.'
  } finally {
    loading.value = false
  }
}

function loginWithGoogle() {
  window.location.href = `${API_BASE}/auth/google?state=admin`
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

.al-page {
  min-height: 100vh;
  background: #080b0f;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  gap: 1rem;
  padding: 2rem 1rem 5rem;
  font-family: 'Rajdhani', sans-serif;
}

.al-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.al-glow {
  position: fixed;
  pointer-events: none;
  z-index: 0;
  border-radius: 50%;
  filter: blur(100px);
}
.al-glow--top {
  width: 600px; height: 400px;
  top: -150px; right: -100px;
  background: radial-gradient(ellipse, rgba(255,60,0,0.18) 0%, transparent 70%);
}
.al-glow--bottom {
  width: 500px; height: 400px;
  bottom: -150px; left: -100px;
  background: radial-gradient(ellipse, rgba(14,50,150,0.15) 0%, transparent 70%);
}

/* Brand */
.al-brand {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.al-logo-mark {
  width: 38px; height: 38px;
  background: rgba(255,90,31,0.12);
  border: 1px solid rgba(255,90,31,0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.al-brand-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #e8e8e8;
  letter-spacing: 0.02em;
}
.al-brand-dot { color: #FF5A1F; }

/* Page title */
.al-page-title {
  position: relative;
  z-index: 1;
  text-align: center;
  margin-bottom: 0.75rem;
}
.al-heading {
  font-size: 2rem;
  font-weight: 700;
  color: #f0f0f0;
  margin: 0 0 0.3rem;
  letter-spacing: 0.01em;
}
.al-subheading {
  font-size: 0.9rem;
  color: rgba(255,255,255,0.35);
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

/* Card */
.al-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 400px;
  background: rgba(14,18,26,0.75);
  border: 1px solid rgba(255,90,31,0.12);
  border-radius: 18px;
  backdrop-filter: blur(28px);
  padding: 2rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.03) inset, 0 40px 80px rgba(0,0,0,0.5);
}
.al-card__fingerprint {
  position: absolute;
  top: 1.1rem;
  right: 1.1rem;
  opacity: 0.6;
}

/* Error */
.al-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.85rem;
  background: rgba(239,68,68,0.07);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.825rem;
  font-weight: 500;
}

/* Fields */
.al-field { display: flex; flex-direction: column; gap: 0.45rem; }
.al-label-row { display: flex; justify-content: space-between; align-items: center; }
.al-label {
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: rgba(255,255,255,0.35);
  font-family: 'Share Tech Mono', monospace;
}
.al-recover {
  font-size: 0.55rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.25);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-family: 'Share Tech Mono', monospace;
  transition: color 0.15s;
}
.al-recover:hover { color: rgba(255,90,31,0.7); }

.al-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 0.9rem;
  font-family: 'Rajdhani', sans-serif;
  font-weight: 500;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}
.al-input::placeholder { color: rgba(255,255,255,0.2); }
.al-input:focus {
  border-color: rgba(255,90,31,0.45);
  box-shadow: 0 0 0 3px rgba(255,90,31,0.07);
}

/* CTA */
.al-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.875rem 1.25rem;
  background: linear-gradient(135deg, #FF5A1F, #FF7A45);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  font-family: 'Share Tech Mono', monospace;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(255,90,31,0.3);
  margin-top: 0.2rem;
}
.al-cta:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 6px 28px rgba(255,90,31,0.4);
}
.al-cta:active:not(:disabled) { transform: translateY(0); }
.al-cta:disabled { opacity: 0.55; cursor: not-allowed; }

.al-spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.25);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.65s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Divider */
.al-divider-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.al-divider-line {
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,0.07);
}
.al-divider-text {
  font-size: 0.55rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: rgba(255,255,255,0.2);
  font-family: 'Share Tech Mono', monospace;
  white-space: nowrap;
}

/* Google */
.al-google {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 9px;
  color: rgba(255,255,255,0.6);
  font-size: 0.875rem;
  font-weight: 500;
  font-family: 'Rajdhani', sans-serif;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.al-google:hover:not(:disabled) {
  background: rgba(255,255,255,0.07);
  border-color: rgba(255,255,255,0.14);
}

/* Switch */
.al-switch {
  text-align: center;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.28);
  margin: 0;
}
.al-switch-link {
  color: rgba(255,90,31,0.7);
  text-decoration: none;
  font-weight: 600;
}
.al-switch-link:hover { color: #FF5A1F; }

/* Status */
.al-status {
  position: fixed;
  bottom: 3.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(10,12,18,0.7);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 999px;
  padding: 0.3rem 0.9rem;
  backdrop-filter: blur(8px);
}
.al-status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 6px rgba(74,222,128,0.7);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.al-status-text {
  font-size: 0.55rem;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.28);
  font-family: 'Share Tech Mono', monospace;
}

/* Footer */
.al-footer {
  position: fixed;
  bottom: 0.75rem;
  left: 0; right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.5rem;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.18);
  font-family: 'Share Tech Mono', monospace;
  flex-wrap: wrap;
  padding: 0 1rem;
}
.al-footer-ver { color: rgba(255,90,31,0.55); }
.al-footer-links { display: flex; gap: 0.85rem; margin-left: auto; }
.al-footer-links a {
  color: rgba(255,255,255,0.18);
  text-decoration: none;
  letter-spacing: 0.06em;
  transition: color 0.15s;
}
.al-footer-links a:hover { color: rgba(255,90,31,0.6); }
</style>