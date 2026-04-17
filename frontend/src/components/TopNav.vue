<template>
  <nav class="topnav glass">
    <!-- Brand -->
    <div class="topnav__brand">
      <span class="topnav__logo-mark">◈</span>
      <span class="topnav__title">Predly</span>
      <span class="topnav__version label-sm">v0.1-preview</span>
    </div>

    <!-- Center Nav Links -->
    <div v-if="showLinks" class="topnav__links">
      <router-link
        v-for="link in navLinks"
        :key="link.to"
        :to="link.to"
        class="topnav__link label-sm"
        :class="{ 'topnav__link--active': isActive(link) }"
      >
        {{ link.label }}
      </router-link>
    </div>

    <!-- Right Actions -->
    <div class="topnav__actions">
      <!-- Authenticated user -->
      <template v-if="user">
        <div class="topnav__user">
          <img
            v-if="user.picture"
            :src="user.picture"
            :alt="user.name"
            class="topnav__avatar"
            referrerpolicy="no-referrer"
          />
          <span v-else class="topnav__avatar-fallback">
            {{ user.name?.charAt(0) || user.email?.charAt(0) || '?' }}
          </span>
          <span class="topnav__user-name label-sm">{{ user.name || user.email }}</span>
        </div>
        <button class="btn-ghost topnav__logout label-sm" @click="handleLogout">
          <span class="material-symbols-outlined" style="font-size:15px">logout</span>
          Sign out
        </button>
      </template>

      <!-- Unauthenticated -->
      <template v-else>
        <slot name="actions">
          <a
            href="https://github.com/nikmcfly/Predly-Offline.git"
            target="_blank"
            class="btn-ghost topnav__github label-sm"
          >
            <span class="material-symbols-outlined" style="font-size:16px">open_in_new</span>
            Github
          </a>
        </slot>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getUser, logout } from '../auth.js'

const props = defineProps({
  showLinks: { type: Boolean, default: false },
  activeStep: { type: String, default: '' },
  projectId: { type: String, default: '' },
  simulationId: { type: String, default: '' },
})

const route = useRoute()
const user = computed(() => getUser())

const navLinks = [
  { label: 'Dashboard', to: '/' },
  { label: 'Graph Build', to: props.projectId ? `/process/${props.projectId}` : '/' },
  { label: 'Simulation', to: props.simulationId ? `/simulation/${props.simulationId}` : '/' },
  { label: 'Reports', to: '/' },
]

function isActive(link) {
  return route.path === link.to || props.activeStep === link.label
}

function handleLogout() {
  logout()
}
</script>

<style scoped>
.topnav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  background: rgba(16, 20, 25, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--ghost-border);
}

.topnav__brand {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.topnav__logo-mark {
  font-size: 1.25rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.topnav__title {
  font-family: var(--font-headline);
  font-weight: 700;
  font-size: 0.9375rem;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.topnav__version {
  color: var(--text-muted);
  padding: 0.125rem 0.5rem;
  background: var(--surface-container);
  border-radius: var(--radius-full);
  border: 1px solid var(--ghost-border);
}

.topnav__links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.topnav__link {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--duration-fast);
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
}
.topnav__link:hover { color: var(--primary); }
.topnav__link--active {
  color: var(--primary);
  border-bottom-color: var(--primary-container);
}

.topnav__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.topnav__github {
  font-size: 0.6875rem;
  letter-spacing: 0.06em;
}

/* User info */
.topnav__user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.topnav__avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.topnav__avatar-fallback {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
}

.topnav__user-name {
  color: var(--text-secondary);
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topnav__logout {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.6875rem;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  transition: color 0.15s;
}
.topnav__logout:hover { color: var(--text-secondary); }
</style>
