<template>
  <div class="ad-shell">

    <!-- ── Sidebar ─────────────────────────────────────────────── -->
    <aside class="ad-sidebar">
      <!-- Brand -->
      <div class="ad-sidebar__brand">
        <div class="ad-sidebar__logo">
          <svg width="20" height="20" viewBox="0 0 22 22" fill="none">
            <path d="M11 2L20 7V15L11 20L2 15V7L11 2Z" stroke="#FF5A1F" stroke-width="1.5" fill="none"/>
            <path d="M11 6L16 9V13L11 16L6 13V9L11 6Z" fill="#FF5A1F" opacity="0.6"/>
          </svg>
        </div>
        <div>
          <div class="ad-sidebar__brand-name">PREDLY ENGINE</div>
          <div class="ad-sidebar__brand-sub">CINEMATIC INTELLIGENCE</div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="ad-sidebar__nav">
        <button
          v-for="item in navItems"
          :key="item.id"
          class="ad-nav-item"
          :class="{ 'ad-nav-item--active': activePage === item.id }"
          @click="activePage = item.id"
        >
          <span class="ad-nav-item__icon" v-html="item.icon"></span>
          <span class="ad-nav-item__label">{{ item.label }}</span>
          <span v-if="activePage === item.id" class="ad-nav-item__bar"></span>
        </button>
      </nav>

      <!-- Compute Engine CTA -->
      <div class="ad-sidebar__footer">
        <button class="ad-compute-btn">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <rect x="1" y="1" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.2"/>
            <path d="M4 7h6M7 4v6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          COMPUTE ENGINE
        </button>
      </div>
    </aside>

    <!-- ── Main ─────────────────────────────────────────────────── -->
    <div class="ad-main">

      <!-- Top Bar -->
      <header class="ad-topbar">
        <div class="ad-topbar__search">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <circle cx="6" cy="6" r="4.5" stroke="rgba(255,255,255,0.25)" stroke-width="1.2"/>
            <path d="M9.5 9.5L12 12" stroke="rgba(255,255,255,0.25)" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          <input class="ad-topbar__search-input" :placeholder="searchPlaceholder" v-model="searchQuery" />
        </div>
        <div class="ad-topbar__actions">
          <button class="ad-topbar__icon-btn" title="Notifications">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 1.5A4.5 4.5 0 0 0 3.5 6v3L2 11h12l-1.5-2V6A4.5 4.5 0 0 0 8 1.5z" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
              <path d="M6.5 11.5a1.5 1.5 0 0 0 3 0" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
            </svg>
          </button>
          <button class="ad-topbar__icon-btn" title="Help">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="6.5" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
              <path d="M6 6.5C6 5.4 6.9 4.5 8 4.5s2 .9 2 2c0 .9-.6 1.6-1.4 1.9-.4.1-.6.5-.6.9V10" stroke="rgba(255,255,255,0.4)" stroke-width="1.2" stroke-linecap="round"/>
              <circle cx="8" cy="11.5" r=".6" fill="rgba(255,255,255,0.4)"/>
            </svg>
          </button>
          <div class="ad-topbar__user">
            <div class="ad-topbar__user-info">
              <span class="ad-topbar__user-name">{{ currentUser?.name || 'Admin User' }}</span>
              <span class="ad-topbar__user-role">{{ currentUser?.is_admin ? 'ROOT ACCESS' : currentUser?.role?.toUpperCase() }}</span>
            </div>
            <div class="ad-topbar__avatar">
              {{ (currentUser?.name || 'A').charAt(0).toUpperCase() }}
            </div>
          </div>
        </div>
      </header>

      <!-- ── Page: Users ────────────────────────────────────────── -->
      <main v-if="activePage === 'users'" class="ad-content">
        <div class="ad-page-header">
          <div class="ad-page-header__meta">MANAGEMENT PORTAL</div>
          <h1 class="ad-page-header__title">Users</h1>
        </div>

        <!-- Stat cards -->
        <div class="ad-stat-row">
          <div class="ad-stat-card">
            <div class="ad-stat-card__label">TOTAL POPULATION</div>
            <div class="ad-stat-card__value">{{ stats.total_users?.toLocaleString() ?? '—' }}</div>
            <div class="ad-stat-card__icon">
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <rect x="1.5" y="1.5" width="8" height="8" rx="1.5" stroke="rgba(182,196,255,0.5)" stroke-width="1.2"/>
                <rect x="12.5" y="1.5" width="8" height="8" rx="1.5" stroke="rgba(182,196,255,0.5)" stroke-width="1.2"/>
                <rect x="1.5" y="12.5" width="8" height="8" rx="1.5" stroke="rgba(182,196,255,0.5)" stroke-width="1.2"/>
                <rect x="12.5" y="12.5" width="8" height="8" rx="1.5" stroke="rgba(182,196,255,0.5)" stroke-width="1.2"/>
              </svg>
            </div>
          </div>
          <div class="ad-stat-card">
            <div class="ad-stat-card__label">ACTIVE NOW</div>
            <div class="ad-stat-card__value">
              {{ stats.active_users?.toLocaleString() ?? '—' }}
              <span class="ad-stat-card__badge ad-stat-card__badge--green">+12% vs last hr</span>
            </div>
            <div class="ad-stat-card__icon ad-stat-card__icon--orange">
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <circle cx="11" cy="11" r="9" stroke="rgba(255,90,31,0.5)" stroke-width="1.2"/>
                <path d="M7 11l3 3 5-5" stroke="rgba(255,90,31,0.8)" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="ad-stat-card">
            <div class="ad-stat-card__label">SYSTEM INTEGRITY</div>
            <div class="ad-stat-card__progress-wrap">
              <div class="ad-stat-card__progress-bar">
                <div class="ad-stat-card__progress-fill" :style="`width:${stats.system_integrity ?? 98.2}%`"></div>
              </div>
              <span class="ad-stat-card__progress-label">{{ stats.system_integrity ?? 98.2 }}% OPTIMAL</span>
            </div>
          </div>
        </div>

        <!-- Users table -->
        <div class="ad-table-card">
          <div v-if="usersLoading" class="ad-loader">
            <span class="ad-spinner"></span> Loading users…
          </div>
          <table v-else class="ad-table">
            <thead>
              <tr>
                <th>IDENTITY</th>
                <th>ROLE</th>
                <th>STATUS</th>
                <th>LAST SESSION</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id" class="ad-table__row ad-table__row--clickable" @click.stop="openUserDetail(user)">
                <td class="ad-table__identity">
                  <div class="ad-avatar">{{ user.name.charAt(0) }}</div>
                  <div>
                    <div class="ad-table__name">{{ user.name }}</div>
                    <div class="ad-table__email">{{ user.email }}</div>
                  </div>
                </td>
                <td>
                  <span class="ad-badge ad-badge--role">{{ formatRole(user.role) }}</span>
                </td>
                <td>
                  <span class="ad-status-pill" :class="user.online ? 'ad-status-pill--active' : (user.status === 'suspended' ? 'ad-status-pill--suspended' : 'ad-status-pill--inactive')">
                    <span class="ad-status-pill__dot" :class="{ 'ad-status-pill__dot--pulse': user.online }"></span>
                    {{ user.online ? 'ONLINE' : (user.status === 'active' ? 'OFFLINE' : user.status.toUpperCase()) }}
                  </span>
                </td>
                <td class="ad-table__muted">{{ formatSession(user.last_session) }}</td>
                <td>
                  <button class="ad-action-btn" @click.stop="openUserMenu(user, $event)">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <circle cx="7" cy="2.5" r="1" fill="currentColor"/>
                      <circle cx="7" cy="7" r="1" fill="currentColor"/>
                      <circle cx="7" cy="11.5" r="1" fill="currentColor"/>
                    </svg>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="5" class="ad-table__empty">No users found</td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="ad-pagination">
            <span class="ad-pagination__info">SHOWING {{ users.length }} OF {{ usersMeta.total?.toLocaleString() }} USERS</span>
            <div class="ad-pagination__controls">
              <button class="ad-pg-btn" :disabled="usersMeta.page <= 1" @click="loadUsers(usersMeta.page - 1)">‹</button>
              <button
                v-for="p in pageRange(usersMeta.page, usersMeta.pages)"
                :key="p"
                class="ad-pg-btn"
                :class="{ 'ad-pg-btn--active': p === usersMeta.page }"
                @click="loadUsers(p)"
              >{{ p }}</button>
              <button class="ad-pg-btn" :disabled="usersMeta.page >= usersMeta.pages" @click="loadUsers(usersMeta.page + 1)">›</button>
            </div>
          </div>
        </div>
      </main>

      <!-- ── Page: Predictions ──────────────────────────────────── -->
      <main v-else-if="activePage === 'predictions'" class="ad-content">
        <div class="ad-page-header ad-page-header--split">
          <div>
            <div class="ad-page-header__meta">SYSTEM INTELLIGENCE</div>
            <h1 class="ad-page-header__title">Prediction History</h1>
          </div>
          <div class="ad-kpi-row">
            <div class="ad-kpi">
              <div class="ad-kpi__label">GLOBAL ACCURACY</div>
              <div class="ad-kpi__value ad-kpi__value--orange">{{ stats.global_accuracy ?? '—' }}<span class="ad-kpi__unit">%</span></div>
            </div>
            <div class="ad-kpi ad-kpi--blue">
              <div class="ad-kpi__label">ACTIVE SIMS</div>
              <div class="ad-kpi__value">{{ stats.active_sims?.toLocaleString() ?? '—' }}</div>
            </div>
          </div>
        </div>

        <!-- Filter row -->
        <div class="ad-filter-row">
          <button class="ad-filter-btn">
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
              <path d="M1.5 3.5h10M3.5 6.5h6M5.5 9.5h2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
            </svg>
            Filter by User
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
          </button>
          <button class="ad-filter-btn">
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
              <circle cx="6.5" cy="6.5" r="3" stroke="currentColor" stroke-width="1.2"/>
              <circle cx="6.5" cy="6.5" r="1" fill="currentColor"/>
            </svg>
            Simulation Type
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
          </button>
          <div style="flex:1"></div>
          <button class="ad-icon-btn" title="Refresh" @click="loadPredictions(predsMeta.page)">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M12 7A5 5 0 1 1 7 2a5 5 0 0 1 3.54 1.46L12 5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              <path d="M12 2v3h-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="ad-icon-btn" title="Export">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M7 1v8M4 6l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M1 10v2a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- Predictions table -->
        <div class="ad-table-card">
          <div v-if="predsLoading" class="ad-loader">
            <span class="ad-spinner"></span> Loading predictions…
          </div>
          <table v-else class="ad-table">
            <thead>
              <tr>
                <th>USER PROFILE</th>
                <th>SIMULATION TYPE</th>
                <th>STATUS</th>
                <th>ACCURACY %</th>
                <th>DATE</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pred in filteredPredictions" :key="pred.id" class="ad-table__row">
                <td class="ad-table__identity">
                  <div class="ad-avatar">{{ pred.user.name.charAt(0) }}</div>
                  <div>
                    <div class="ad-table__name">{{ pred.user.name }}</div>
                    <div class="ad-table__email">ID: PRD-{{ String(pred.id).padStart(4, '0') }}</div>
                  </div>
                </td>
                <td>
                  <span class="ad-sim-type">
                    <span class="ad-sim-type__dot" :style="simTypeColor(pred.simulation_type)"></span>
                    {{ pred.simulation_type }}
                  </span>
                </td>
                <td>
                  <span class="ad-pred-status" :class="`ad-pred-status--${pred.status}`">
                    <span class="ad-pred-status__dot"></span>
                    {{ pred.status.toUpperCase() }}
                  </span>
                </td>
                <td>
                  <div v-if="pred.status === 'in_progress'" class="ad-accuracy-syncing">Syncing…</div>
                  <div v-else-if="pred.accuracy != null" class="ad-accuracy">
                    <div class="ad-accuracy__bar">
                      <div class="ad-accuracy__fill" :style="`width:${pred.accuracy}%;background:${accuracyColor(pred.accuracy)}`"></div>
                    </div>
                    <span class="ad-accuracy__label" :style="`color:${accuracyColor(pred.accuracy)}`">{{ pred.accuracy }}%</span>
                  </div>
                  <span v-else class="ad-table__muted">—</span>
                </td>
                <td class="ad-table__muted">
                  <div>{{ formatDate(pred.created_at) }}</div>
                  <div style="font-size:0.65rem">{{ formatTime(pred.created_at) }} GMT</div>
                </td>
              </tr>
              <tr v-if="filteredPredictions.length === 0 && !predsLoading">
                <td colspan="5" class="ad-table__empty">No predictions found</td>
              </tr>
            </tbody>
          </table>

          <div class="ad-pagination">
            <span class="ad-pagination__info">Showing 1-{{ predictions.length }} of {{ predsMeta.total?.toLocaleString() }} predictions</span>
            <div class="ad-pagination__controls">
              <button class="ad-pg-btn" :disabled="predsMeta.page <= 1" @click="loadPredictions(predsMeta.page - 1)">‹</button>
              <button
                v-for="p in pageRange(predsMeta.page, predsMeta.pages)"
                :key="p"
                class="ad-pg-btn"
                :class="{ 'ad-pg-btn--active': p === predsMeta.page }"
                @click="loadPredictions(p)"
              >{{ p }}</button>
              <button class="ad-pg-btn" :disabled="predsMeta.page >= predsMeta.pages" @click="loadPredictions(predsMeta.page + 1)">›</button>
            </div>
          </div>
        </div>

        <!-- Compute Efficiency Chart -->
        <div class="ad-chart-card">
          <div class="ad-chart-card__header">
            <div>
              <div class="ad-chart-card__title">Compute Efficiency</div>
              <div class="ad-chart-card__sub">Real-time resource allocation across prediction nodes</div>
            </div>
            <button class="ad-optimal-btn">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M6 1l1.5 3h3L8 6l1 3.5L6 8l-3 1.5L4 6 1.5 4h3z" fill="#FF5A1F" opacity="0.8"/>
              </svg>
              OPTIMAL RANGE
            </button>
          </div>
          <div class="ad-chart">
            <div
              v-for="(bar, i) in computeBars"
              :key="i"
              class="ad-chart__bar-wrap"
            >
              <div
                class="ad-chart__bar"
                :style="`height:${bar.height}%;background:${bar.color};opacity:${bar.opacity}`"
              ></div>
            </div>
          </div>
        </div>
      </main>

      <!-- ── Page: System Status ────────────────────────────────── -->
      <main v-else-if="activePage === 'system'" class="ad-content">
        <div class="ad-page-header">
          <div class="ad-page-header__meta">INFRASTRUCTURE</div>
          <h1 class="ad-page-header__title">System Status</h1>
        </div>
        <div class="ad-system-cards">
          <div class="ad-system-card">
            <div class="ad-system-card__label">Security Engine</div>
            <div class="ad-system-card__val ad-system-card__val--green">NOMINAL</div>
          </div>
          <div class="ad-system-card">
            <div class="ad-system-card__label">Uptime</div>
            <div class="ad-system-card__val">{{ stats.uptime_pct ?? 99.8 }}%</div>
          </div>
          <div class="ad-system-card">
            <div class="ad-system-card__label">API Version</div>
            <div class="ad-system-card__val">A.A.P.V4.0.2</div>
          </div>
          <div class="ad-system-card">
            <div class="ad-system-card__label">Global Accuracy</div>
            <div class="ad-system-card__val ad-system-card__val--orange">{{ stats.global_accuracy ?? '—' }}%</div>
          </div>
        </div>
      </main>

      <!-- ── Page: Settings ─────────────────────────────────────── -->
      <main v-else-if="activePage === 'settings'" class="ad-content">
        <div class="ad-page-header">
          <div class="ad-page-header__meta">CONFIGURATION</div>
          <h1 class="ad-page-header__title">Settings</h1>
        </div>
        <div class="ad-settings-card">
          <div class="ad-settings-row">
            <div>
              <div class="ad-settings-row__label">Your Account</div>
              <div class="ad-settings-row__val">{{ currentUser?.email }}</div>
            </div>
            <span class="ad-badge ad-badge--role">{{ formatRole(currentUser?.role || 'admin') }}</span>
          </div>
          <div class="ad-settings-row">
            <div>
              <div class="ad-settings-row__label">Access Level</div>
              <div class="ad-settings-row__val">Root Admin</div>
            </div>
            <span class="ad-status-pill ad-status-pill--active"><span class="ad-status-pill__dot"></span> ACTIVE</span>
          </div>
          <div class="ad-settings-row ad-settings-row--danger">
            <div>
              <div class="ad-settings-row__label">Sign Out</div>
              <div class="ad-settings-row__val">End your admin session</div>
            </div>
            <button class="ad-logout-btn" @click="handleLogout">Sign Out</button>
          </div>
        </div>
      </main>

      <!-- ── User Detail Drawer ──────────────────────────────────── -->
      <Teleport to="body">
        <div v-if="userDetail.open" class="ud-backdrop" @click="closeUserDetail"></div>
        <div class="ud-drawer" :class="{ 'ud-drawer--open': userDetail.open }">
          <div class="ud-drawer__header">
            <div class="ud-drawer__avatar">{{ userDetail.user?.name?.charAt(0) ?? '?' }}</div>
            <div>
              <div class="ud-drawer__name">{{ userDetail.user?.name }}</div>
              <div class="ud-drawer__email">{{ userDetail.user?.email }}</div>
            </div>
            <button class="ud-drawer__close" @click="closeUserDetail">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="ud-drawer__stat">
            <div class="ud-drawer__stat-label">TOTAL PREDICTIONS</div>
            <div class="ud-drawer__stat-value">{{ userDetail.total }}</div>
          </div>

          <div class="ud-drawer__section-label">PREDICTION HISTORY</div>

          <div v-if="userDetail.loading" class="ud-drawer__loader">
            <span class="ad-spinner"></span> Loading…
          </div>
          <div v-else-if="userDetail.error" class="ud-drawer__empty" style="color:#ff5a1f">
            Error: {{ userDetail.error }}
          </div>
          <div v-else-if="userDetail.predictions.length === 0" class="ud-drawer__empty">
            No predictions yet
          </div>
          <table v-else class="ud-table">
            <thead>
              <tr>
                <th>SIMULATION TYPE</th>
                <th>STATUS</th>
                <th>DATE</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in userDetail.predictions" :key="p.id">
                <td class="ud-table__title">{{ p.title }}</td>
                <td>
                  <span class="ad-pred-status" :class="`ad-pred-status--${p.status}`">
                    <span class="ad-pred-status__dot"></span>
                    {{ p.status.toUpperCase() }}
                  </span>
                </td>
                <td class="ud-table__date">{{ formatSession(p.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Teleport>

    </div><!-- /ad-main -->

    <!-- Context menu for user actions -->
    <div v-if="contextMenu.visible" class="ad-context-menu" :style="`top:${contextMenu.y}px;left:${contextMenu.x}px`">
      <button @click="changeRole('admin')">Promote to Admin</button>
      <button @click="changeRole('user')">Set as User</button>
      <button @click="toggleStatus">{{ contextMenu.user?.status === 'active' ? 'Deactivate' : 'Activate' }}</button>
      <button class="ad-context-menu__danger" @click="deleteUser">Delete User</button>
    </div>
    <div v-if="contextMenu.visible" class="ad-context-overlay" @click="contextMenu.visible = false"></div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getUser, logout, getToken } from '../auth.js'

const router = useRouter()
const currentUser = computed(() => getUser())
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'

// ── Nav ───────────────────────────────────────────────────────────────────
const activePage = ref('users')

const navItems = [
  {
    id: 'users', label: 'Users',
    icon: `<svg width="17" height="17" viewBox="0 0 17 17" fill="none"><circle cx="8.5" cy="5.5" r="3" stroke="currentColor" stroke-width="1.2"/><path d="M2 14c0-3.31 2.91-6 6.5-6s6.5 2.69 6.5 6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`
  },
  {
    id: 'predictions', label: 'Predictions',
    icon: `<svg width="17" height="17" viewBox="0 0 17 17" fill="none"><rect x="2" y="2" width="13" height="13" rx="1.5" stroke="currentColor" stroke-width="1.2"/><path d="M5 11l3-3 2 2 2-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: 'system', label: 'System Status',
    icon: `<svg width="17" height="17" viewBox="0 0 17 17" fill="none"><rect x="2" y="2" width="13" height="13" rx="1.5" stroke="currentColor" stroke-width="1.2"/><path d="M5 9h2l1.5-4 2 8 1.5-4H14" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: 'settings', label: 'Settings',
    icon: `<svg width="17" height="17" viewBox="0 0 17 17" fill="none"><circle cx="8.5" cy="8.5" r="2.5" stroke="currentColor" stroke-width="1.2"/><path d="M8.5 2v1.5M8.5 13.5V15M2 8.5h1.5M13.5 8.5H15M4.1 4.1l1 1M11.9 11.9l1 1M4.1 12.9l1-1M11.9 5.1l1-1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`
  },
]

const searchQuery = ref('')
const searchPlaceholder = computed(() => {
  const map = { users: 'Search users, roles, or identifiers…', predictions: 'Search predictions, nodes, or hash…', system: 'Search systems…', settings: 'Search settings…' }
  return map[activePage.value] || 'Search…'
})

// ── Data ──────────────────────────────────────────────────────────────────
const stats = ref({})
const users = ref([])
const usersMeta = ref({ page: 1, pages: 1, total: 0 })
const usersLoading = ref(false)
const userDetail = ref({ open: false, user: null, loading: false, predictions: [], total: 0, error: null })

const predictions = ref([])
const predsMeta = ref({ page: 1, pages: 1, total: 0 })
const predsLoading = ref(false)

async function apiFetch(path, opts = {}) {
  const token = getToken()
  return fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', ...(opts.headers || {}) },
  })
}

async function loadStats() {
  try {
    const res = await apiFetch('/admin/stats')
    const body = await res.json()
    if (body.success) stats.value = body.data
  } catch { /* silently fail — show dashes */ }
}

async function loadUsers(page = 1) {
  usersLoading.value = true
  try {
    const res  = await apiFetch(`/admin/users?page=${page}&limit=10`)
    const body = await res.json()
    if (body.success) {
      users.value    = body.data.users
      usersMeta.value = { page: body.data.page, pages: body.data.pages, total: body.data.total }
    }
  } catch { /* network error */ } finally { usersLoading.value = false }
}

async function openUserDetail(user) {
  userDetail.value = { open: true, user, loading: true, predictions: [], total: 0, error: null }
  try {
    const res  = await apiFetch(`/admin/users/${user.id}/predictions`)
    const body = await res.json()
    if (body.success) {
      userDetail.value.predictions = body.data.predictions
      userDetail.value.total       = body.data.total
    } else {
      userDetail.value.error = body.error || 'Failed to load predictions'
      console.error('[UserDetail] API error:', body)
    }
  } catch (e) {
    userDetail.value.error = e.message || 'Network error'
    console.error('[UserDetail] fetch error:', e)
  } finally { userDetail.value.loading = false }
}
function closeUserDetail() { userDetail.value.open = false }

async function loadPredictions(page = 1) {
  predsLoading.value = true
  try {
    const res  = await apiFetch(`/admin/predictions?page=${page}&limit=15`)
    const body = await res.json()
    if (body.success) {
      predictions.value = body.data.predictions
      predsMeta.value   = { page: body.data.page, pages: body.data.pages, total: body.data.total }
    }
  } catch { /* network error */ } finally { predsLoading.value = false }
}

// Watch page switch to lazy-load
watch(activePage, (page) => {
  if (page === 'predictions' && predictions.value.length === 0) loadPredictions()
})

let refreshTimer = null
onMounted(() => {
  loadStats()
  loadUsers()
  document.addEventListener('click', closeContextMenu)
  refreshTimer = setInterval(() => {
    if (activePage.value === 'users') loadUsers(usersMeta.value.page)
  }, 30000)
})
onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu)
  if (refreshTimer) clearInterval(refreshTimer)
})

// ── Filtering ─────────────────────────────────────────────────────────────
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const q = searchQuery.value.toLowerCase()
  return users.value.filter(u =>
    u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q) || u.role.includes(q)
  )
})
const filteredPredictions = computed(() => {
  if (!searchQuery.value) return predictions.value
  const q = searchQuery.value.toLowerCase()
  return predictions.value.filter(p =>
    p.user.name.toLowerCase().includes(q) || p.simulation_type.toLowerCase().includes(q) || p.status.includes(q)
  )
})

// ── Context menu ──────────────────────────────────────────────────────────
const contextMenu = ref({ visible: false, x: 0, y: 0, user: null })

function openUserMenu(user, event) {
  event.stopPropagation()
  const rect = event.target.getBoundingClientRect()
  contextMenu.value = { visible: true, x: rect.left - 120, y: rect.bottom + 4, user }
}
function closeContextMenu() { contextMenu.value.visible = false }

async function changeRole(role) {
  const u = contextMenu.value.user
  contextMenu.value.visible = false
  if (!u) return
  await apiFetch(`/admin/users/${u.id}`, { method: 'PATCH', body: JSON.stringify({ role }) })
  loadUsers(usersMeta.value.page)
}
async function toggleStatus() {
  const u = contextMenu.value.user
  contextMenu.value.visible = false
  if (!u) return
  const status = u.status === 'active' ? 'inactive' : 'active'
  await apiFetch(`/admin/users/${u.id}`, { method: 'PATCH', body: JSON.stringify({ status }) })
  loadUsers(usersMeta.value.page)
}
async function deleteUser() {
  const u = contextMenu.value.user
  contextMenu.value.visible = false
  if (!u || !confirm(`Delete user ${u.email}?`)) return
  await apiFetch(`/admin/users/${u.id}`, { method: 'DELETE' })
  loadUsers(usersMeta.value.page)
}

// ── Logout ────────────────────────────────────────────────────────────────
function handleLogout() { logout() }

// ── Helpers ───────────────────────────────────────────────────────────────
function formatRole(role) {
  const map = { admin: 'ADMIN', user: 'USER', senior_architect: 'SENIOR ARCHITECT', ai_specialist: 'AI SPECIALIST', observer: 'OBSERVER', data_engineer: 'DATA ENGINEER' }
  return map[role] || role?.toUpperCase() || 'USER'
}
function formatSession(ts) {
  if (!ts) return 'Never'
  // Append Z so the browser treats the UTC timestamp as UTC, not local time
  const d = new Date(ts.endsWith('Z') || ts.includes('+') ? ts : ts + 'Z')
  const diff = Date.now() - d.getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins} mins ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} hrs ago`
  return `${Math.floor(hrs / 24)} days ago`
}
function formatDate(ts) {
  if (!ts) return '—'
  return new Date(ts).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })
}
function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
}
function simTypeColor(type) {
  return type?.toLowerCase().includes('graph') ? 'background:#FF5A1F' : 'background:#6C8EFF'
}
function accuracyColor(val) {
  if (val >= 80) return '#FF5A1F'
  if (val >= 50) return '#FBBC05'
  return '#f87171'
}
function pageRange(current, total) {
  const pages = []
  const start = Math.max(1, current - 1)
  const end   = Math.min(total, start + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
}

// ── Fake compute efficiency bars ──────────────────────────────────────────
const computeBars = Array.from({ length: 12 }, (_, i) => {
  const isHighlight = [2, 5, 8].includes(i)
  return {
    height: 25 + Math.round(Math.random() * 65),
    color: isHighlight ? '#FF5A1F' : '#6C8EFF',
    opacity: isHighlight ? 0.85 : 0.3 + Math.random() * 0.3,
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Shell ─────────────────────────────────────────────────────────────── */
.ad-shell {
  display: flex;
  min-height: 100vh;
  background: #101419;
  font-family: 'Space Grotesk', sans-serif;
  color: #E0E2EA;
}

/* ── Sidebar ───────────────────────────────────────────────────────────── */
.ad-sidebar {
  width: 220px;
  min-width: 220px;
  background: #13171e;
  border-right: 1px solid rgba(171,137,127,0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 50;
  overflow-y: auto;
}

.ad-sidebar__brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1rem 1.1rem;
  border-bottom: 1px solid rgba(171,137,127,0.1);
}
.ad-sidebar__logo {
  width: 36px; height: 36px;
  background: rgba(255,90,31,0.1);
  border: 1px solid rgba(255,90,31,0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.ad-sidebar__brand-name {
  font-size: 0.7rem;
  font-weight: 700;
  color: #FF5A1F;
  letter-spacing: 0.06em;
  line-height: 1.2;
}
.ad-sidebar__brand-sub {
  font-size: 0.5rem;
  color: rgba(255,255,255,0.28);
  letter-spacing: 0.07em;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 2px;
}

.ad-sidebar__nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0.75rem 0.5rem;
  gap: 2px;
}
.ad-nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.65rem 0.75rem;
  border-radius: 8px;
  background: none;
  border: none;
  color: rgba(255,255,255,0.38);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  width: 100%;
  position: relative;
  transition: color 0.15s, background 0.15s;
  font-family: 'Space Grotesk', sans-serif;
}
.ad-nav-item:hover { color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.04); }
.ad-nav-item--active {
  color: #FF5A1F;
  background: rgba(255,90,31,0.06);
}
.ad-nav-item__icon { flex-shrink: 0; display: flex; }
.ad-nav-item__bar {
  position: absolute;
  right: 0; top: 20%; bottom: 20%;
  width: 3px;
  background: #FF5A1F;
  border-radius: 2px 0 0 2px;
}

.ad-sidebar__footer { padding: 1rem 0.75rem 1.25rem; margin-top: auto; }
.ad-compute-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.7rem 1rem;
  background: linear-gradient(135deg, #FF5A1F, #FF7A45);
  border: none;
  border-radius: 9px;
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  font-family: 'JetBrains Mono', monospace;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(255,90,31,0.25);
  transition: opacity 0.15s;
}
.ad-compute-btn:hover { opacity: 0.88; }

/* ── Main ──────────────────────────────────────────────────────────────── */
.ad-main {
  flex: 1;
  margin-left: 220px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Topbar ────────────────────────────────────────────────────────────── */
.ad-topbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 2rem;
  height: 60px;
  background: #13171e;
  border-bottom: 1px solid rgba(171,137,127,0.1);
  position: sticky;
  top: 0;
  z-index: 40;
}
.ad-topbar__search {
  flex: 1;
  max-width: 380px;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 8px;
  padding: 0.5rem 0.875rem;
}
.ad-topbar__search-input {
  background: none;
  border: none;
  outline: none;
  color: rgba(255,255,255,0.5);
  font-size: 0.825rem;
  font-family: 'Space Grotesk', sans-serif;
  width: 100%;
}
.ad-topbar__search-input::placeholder { color: rgba(255,255,255,0.25); }
.ad-topbar__actions { display: flex; align-items: center; gap: 0.75rem; margin-left: auto; }
.ad-topbar__icon-btn {
  width: 32px; height: 32px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background 0.15s;
}
.ad-topbar__icon-btn:hover { background: rgba(255,255,255,0.05); }
.ad-topbar__user { display: flex; align-items: center; gap: 0.6rem; }
.ad-topbar__user-info { text-align: right; }
.ad-topbar__user-name { display: block; font-size: 0.8rem; font-weight: 600; color: #E0E2EA; }
.ad-topbar__user-role { display: block; font-size: 0.55rem; letter-spacing: 0.08em; color: rgba(255,90,31,0.7); font-family: 'JetBrains Mono', monospace; }
.ad-topbar__avatar {
  width: 34px; height: 34px;
  background: linear-gradient(135deg,#FF5A1F,#FF8C5A);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  color: #fff;
}

/* ── Content ───────────────────────────────────────────────────────────── */
.ad-content { padding: 2rem; flex: 1; }

/* ── Page header ───────────────────────────────────────────────────────── */
.ad-page-header { margin-bottom: 1.75rem; }
.ad-page-header--split { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.ad-page-header__meta {
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  color: rgba(255,255,255,0.28);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 0.35rem;
}
.ad-page-header__title { font-size: 2rem; font-weight: 700; color: #E6EDF3; margin: 0; letter-spacing: -0.02em; }

/* ── KPI row ───────────────────────────────────────────────────────────── */
.ad-kpi-row { display: flex; gap: 1rem; }
.ad-kpi {
  padding: 0.75rem 1.25rem;
  border-left: 3px solid rgba(255,90,31,0.35);
  background: rgba(255,90,31,0.05);
  border-radius: 0 8px 8px 0;
  min-width: 110px;
}
.ad-kpi--blue { border-color: rgba(108,142,255,0.4); background: rgba(108,142,255,0.06); }
.ad-kpi__label { font-size: 0.55rem; letter-spacing: 0.1em; color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace; }
.ad-kpi__value { font-size: 1.75rem; font-weight: 700; color: #E6EDF3; line-height: 1.1; }
.ad-kpi__value--orange { color: #FF5A1F; }
.ad-kpi__unit { font-size: 0.9rem; color: rgba(255,255,255,0.4); }

/* ── Stat cards ────────────────────────────────────────────────────────── */
.ad-stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.ad-stat-card {
  background: #181c21;
  border: 1px solid rgba(171,137,127,0.1);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  position: relative;
  overflow: hidden;
}
.ad-stat-card__label { font-size: 0.575rem; letter-spacing: 0.1em; color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace; margin-bottom: 0.5rem; }
.ad-stat-card__value { font-size: 1.9rem; font-weight: 700; color: #E6EDF3; display: flex; align-items: baseline; gap: 0.5rem; flex-wrap: wrap; }
.ad-stat-card__icon { position: absolute; top: 1rem; right: 1rem; opacity: 0.6; }
.ad-stat-card__icon--orange { opacity: 0.8; }
.ad-stat-card__badge { font-size: 0.6rem; font-weight: 600; letter-spacing: 0.04em; padding: 0.2rem 0.5rem; border-radius: 999px; }
.ad-stat-card__badge--green { background: rgba(74,222,128,0.12); color: #4ade80; }
.ad-stat-card__progress-wrap { display: flex; flex-direction: column; gap: 0.5rem; padding-top: 0.25rem; }
.ad-stat-card__progress-bar { height: 6px; background: rgba(255,255,255,0.08); border-radius: 999px; overflow: hidden; }
.ad-stat-card__progress-fill { height: 100%; background: linear-gradient(90deg,#6C8EFF,#4ade80); border-radius: 999px; transition: width 0.5s ease; }
.ad-stat-card__progress-label { font-size: 0.7rem; font-weight: 600; color: rgba(255,255,255,0.5); font-family: 'JetBrains Mono', monospace; }

/* ── Table card ────────────────────────────────────────────────────────── */
.ad-table-card {
  background: #181c21;
  border: 1px solid rgba(171,137,127,0.1);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.ad-loader { display: flex; align-items: center; gap: 0.75rem; padding: 2.5rem; color: rgba(255,255,255,0.35); font-size: 0.875rem; }
.ad-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.12);
  border-top-color: #FF5A1F;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

.ad-table { width: 100%; border-collapse: collapse; }
.ad-table thead tr { border-bottom: 1px solid rgba(171,137,127,0.1); }
.ad-table th {
  padding: 0.75rem 1.25rem;
  font-size: 0.575rem;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.3);
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  text-align: left;
}
.ad-table__row { border-bottom: 1px solid rgba(171,137,127,0.06); transition: background 0.12s; }
.ad-table__row:last-child { border-bottom: none; }
.ad-table__row:hover { background: rgba(255,255,255,0.02); }
.ad-table td { padding: 1rem 1.25rem; font-size: 0.875rem; vertical-align: middle; }
.ad-table__identity { display: flex; align-items: center; gap: 0.75rem; }
.ad-table__name { font-weight: 600; color: #E0E2EA; font-size: 0.875rem; }
.ad-table__email { font-size: 0.675rem; color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace; margin-top: 2px; }
.ad-table__muted { color: rgba(255,255,255,0.35); font-size: 0.78rem; }
.ad-table__empty { text-align: center; padding: 3rem; color: rgba(255,255,255,0.25); font-style: italic; }

.ad-avatar {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, rgba(255,90,31,0.3), rgba(108,142,255,0.3));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.8);
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.08);
}

/* ── Badges & pills ────────────────────────────────────────────────────── */
.ad-badge {
  display: inline-block;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.575rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  font-family: 'JetBrains Mono', monospace;
}
.ad-badge--role { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.1); }

.ad-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  font-size: 0.575rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  font-family: 'JetBrains Mono', monospace;
}
.ad-status-pill--active { background: rgba(74,222,128,0.08); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
.ad-status-pill--inactive { background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.08); }
.ad-status-pill--suspended { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.ad-status-pill__dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; flex-shrink: 0; }
.ad-status-pill__dot--pulse { animation: pill-pulse 1.8s ease-in-out infinite; }
@keyframes pill-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* Prediction status */
.ad-pred-status {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  font-family: 'JetBrains Mono', monospace;
}
.ad-pred-status--completed { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
.ad-pred-status--failed { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.ad-pred-status--in_progress { background: rgba(108,142,255,0.1); color: #6C8EFF; border: 1px solid rgba(108,142,255,0.2); }
.ad-pred-status__dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

.ad-sim-type { display: flex; align-items: center; gap: 0.4rem; font-size: 0.825rem; color: rgba(255,255,255,0.55); }
.ad-sim-type__dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

/* Accuracy bar */
.ad-accuracy { display: flex; align-items: center; gap: 0.6rem; min-width: 120px; }
.ad-accuracy__bar { flex: 1; height: 5px; background: rgba(255,255,255,0.08); border-radius: 999px; overflow: hidden; }
.ad-accuracy__fill { height: 100%; border-radius: 999px; }
.ad-accuracy__label { font-size: 0.8rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
.ad-accuracy-syncing { font-size: 0.7rem; color: #6C8EFF; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em; }

.ad-action-btn {
  background: none;
  border: none;
  color: rgba(255,255,255,0.3);
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 4px;
  transition: color 0.12s, background 0.12s;
  display: flex;
}
.ad-action-btn:hover { color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.06); }

/* ── Pagination ─────────────────────────────────────────────────────────── */
.ad-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.25rem;
  border-top: 1px solid rgba(171,137,127,0.08);
}
.ad-pagination__info { font-size: 0.575rem; letter-spacing: 0.1em; color: rgba(255,255,255,0.2); font-family: 'JetBrains Mono', monospace; }
.ad-pagination__controls { display: flex; gap: 0.35rem; }
.ad-pg-btn {
  width: 30px; height: 30px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px;
  color: rgba(255,255,255,0.4);
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.12s, color 0.12s;
  font-family: 'Space Grotesk', sans-serif;
}
.ad-pg-btn:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: #E0E2EA; }
.ad-pg-btn--active { background: #FF5A1F !important; border-color: #FF5A1F !important; color: #fff !important; }
.ad-pg-btn:disabled { opacity: 0.3; cursor: not-allowed; }

/* ── Filter row ────────────────────────────────────────────────────────── */
.ad-filter-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1rem;
}
.ad-filter-btn {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 0.9rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 8px;
  color: rgba(255,255,255,0.45);
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  font-family: 'Space Grotesk', sans-serif;
  transition: background 0.15s;
}
.ad-filter-btn:hover { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.65); }
.ad-icon-btn {
  width: 34px; height: 34px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 8px;
  color: rgba(255,255,255,0.4);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.12s;
}
.ad-icon-btn:hover { background: rgba(255,255,255,0.08); }

/* ── Chart ─────────────────────────────────────────────────────────────── */
.ad-chart-card {
  background: #181c21;
  border: 1px solid rgba(171,137,127,0.1);
  border-radius: 14px;
  padding: 1.5rem;
}
.ad-chart-card__header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1.5rem; }
.ad-chart-card__title { font-size: 1rem; font-weight: 700; color: #E0E2EA; }
.ad-chart-card__sub { font-size: 0.725rem; color: rgba(255,255,255,0.3); margin-top: 0.2rem; }
.ad-optimal-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.9rem;
  background: #181c21;
  border: 1px solid rgba(255,90,31,0.25);
  border-radius: 20px;
  color: rgba(255,255,255,0.5);
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  font-family: 'JetBrains Mono', monospace;
  transition: border-color 0.15s;
}
.ad-optimal-btn:hover { border-color: rgba(255,90,31,0.5); color: rgba(255,255,255,0.7); }
.ad-chart {
  display: flex;
  align-items: flex-end;
  gap: 0.4rem;
  height: 150px;
}
.ad-chart__bar-wrap { flex: 1; display: flex; align-items: flex-end; height: 100%; }
.ad-chart__bar { width: 100%; border-radius: 4px 4px 0 0; transition: height 0.4s ease; min-height: 4px; }

/* ── System status ──────────────────────────────────────────────────────── */
.ad-system-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
.ad-system-card { background: #181c21; border: 1px solid rgba(171,137,127,0.1); border-radius: 12px; padding: 1.5rem; }
.ad-system-card__label { font-size: 0.6rem; letter-spacing: 0.1em; color: rgba(255,255,255,0.28); font-family: 'JetBrains Mono', monospace; margin-bottom: 0.5rem; }
.ad-system-card__val { font-size: 1.25rem; font-weight: 700; color: #E0E2EA; }
.ad-system-card__val--green { color: #4ade80; }
.ad-system-card__val--orange { color: #FF5A1F; }

/* ── Settings ───────────────────────────────────────────────────────────── */
.ad-settings-card { background: #181c21; border: 1px solid rgba(171,137,127,0.1); border-radius: 14px; overflow: hidden; }
.ad-settings-row { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 1.5rem; border-bottom: 1px solid rgba(171,137,127,0.07); }
.ad-settings-row:last-child { border-bottom: none; }
.ad-settings-row--danger { background: rgba(248,113,113,0.03); }
.ad-settings-row__label { font-size: 0.8rem; font-weight: 600; color: rgba(255,255,255,0.6); margin-bottom: 0.2rem; }
.ad-settings-row__val { font-size: 0.75rem; color: rgba(255,255,255,0.35); font-family: 'JetBrains Mono', monospace; }
.ad-logout-btn { padding: 0.5rem 1.25rem; background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.25); border-radius: 8px; color: #f87171; font-size: 0.8rem; font-weight: 600; cursor: pointer; font-family: 'Space Grotesk', sans-serif; transition: background 0.15s; }
.ad-logout-btn:hover { background: rgba(248,113,113,0.18); }

/* ── Context menu ───────────────────────────────────────────────────────── */
.ad-context-menu {
  position: fixed;
  z-index: 200;
  background: #1c2028;
  border: 1px solid rgba(171,137,127,0.15);
  border-radius: 10px;
  padding: 0.4rem;
  min-width: 160px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}
.ad-context-menu button {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.55rem 0.85rem;
  background: none;
  border: none;
  border-radius: 6px;
  color: rgba(255,255,255,0.6);
  font-size: 0.8rem;
  font-family: 'Space Grotesk', sans-serif;
  cursor: pointer;
  transition: background 0.12s, color 0.12s;
}
.ad-context-menu button:hover { background: rgba(255,255,255,0.06); color: #E0E2EA; }
.ad-context-menu__danger { color: #f87171 !important; }
.ad-context-menu__danger:hover { background: rgba(248,113,113,0.08) !important; }
.ad-context-overlay { position: fixed; inset: 0; z-index: 199; }
.ad-table__row--clickable { cursor: pointer; }

/* ── User Detail Drawer ──────────────────────────────────────────────────── */
.ud-backdrop {
  position: fixed; inset: 0; z-index: 299;
  background: rgba(0,0,0,0.45); backdrop-filter: blur(2px);
}
.ud-drawer {
  position: fixed; top: 0; right: 0; bottom: 0; z-index: 300;
  width: 480px; max-width: 95vw;
  background: #0e1218;
  border-left: 1px solid rgba(171,137,127,0.12);
  display: flex; flex-direction: column; gap: 0;
  transform: translateX(100%);
  transition: transform 0.25s cubic-bezier(0.4,0,0.2,1);
  overflow-y: auto;
}
.ud-drawer--open { transform: translateX(0); }

.ud-drawer__header {
  display: flex; align-items: center; gap: 1rem;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: sticky; top: 0;
  background: #0e1218; z-index: 1;
}
.ud-drawer__avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, #FF5A1F22, #6C8EFF22);
  border: 1px solid rgba(255,90,31,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; font-weight: 700; color: #FF5A1F;
  flex-shrink: 0;
}
.ud-drawer__name { font-weight: 700; color: #E0E2EA; font-size: 0.95rem; }
.ud-drawer__email { font-size: 0.7rem; color: rgba(255,255,255,0.35); font-family: 'JetBrains Mono', monospace; margin-top: 2px; }
.ud-drawer__close {
  margin-left: auto; background: none; border: none;
  color: rgba(255,255,255,0.3); cursor: pointer; padding: 0.25rem;
  transition: color 0.15s;
}
.ud-drawer__close:hover { color: #E0E2EA; }

.ud-drawer__stat {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.ud-drawer__stat-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em; color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace; }
.ud-drawer__stat-value { font-size: 2rem; font-weight: 700; color: #E0E2EA; margin-top: 0.25rem; }

.ud-drawer__section-label {
  padding: 1rem 1.5rem 0.5rem;
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
  color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace;
}
.ud-drawer__loader { padding: 2rem 1.5rem; color: rgba(255,255,255,0.35); display: flex; align-items: center; gap: 0.75rem; }
.ud-drawer__empty { padding: 2rem 1.5rem; color: rgba(255,255,255,0.25); font-style: italic; font-size: 0.875rem; }

.ud-table { width: 100%; border-collapse: collapse; }
.ud-table th {
  padding: 0.6rem 1.5rem; text-align: left;
  font-size: 0.575rem; font-weight: 700; letter-spacing: 0.08em;
  color: rgba(255,255,255,0.3); font-family: 'JetBrains Mono', monospace;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.ud-table td { padding: 0.85rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.04); vertical-align: middle; }
.ud-table tr:last-child td { border-bottom: none; }
.ud-table__title { font-size: 0.825rem; color: #C8CAD4; font-weight: 500; max-width: 220px; }
.ud-table__date { font-size: 0.75rem; color: rgba(255,255,255,0.35); font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
</style>