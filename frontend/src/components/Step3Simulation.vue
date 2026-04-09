<template>
  <div class="sim">
    <!-- Error Banner -->
    <div v-if="errorMsg" class="sim__error-banner">
      <span class="material-symbols-outlined" style="font-size:16px">error</span>
      {{ errorMsg }}
      <button class="btn-ghost" style="margin-left:auto;font-size:.75rem" @click="errorMsg=''">Dismiss</button>
    </div>

    <!-- Control Bar -->
    <div class="sim__control-bar glass">
      <!-- Platform Statuses -->
      <div class="sim__platforms">
        <!-- Info Plaza (Twitter-like) -->
        <div class="sim__platform" :class="{'sim__platform--active': runStatus.twitter_running, 'sim__platform--done': runStatus.twitter_completed}">
          <div class="sim__platform-header">
            <span class="material-symbols-outlined" style="font-size:16px">public</span>
            <span class="label-sm sim__platform-name">Info Plaza</span>
            <span v-if="runStatus.twitter_completed" class="chip chip-green" style="margin-left:auto">
              <span class="material-symbols-outlined" style="font-size:11px">check</span> Done
            </span>
            <div v-else-if="runStatus.twitter_running" class="ai-chip" style="margin-left:auto;padding:.2rem .5rem">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">Live</span>
            </div>
          </div>
          <div class="sim__platform-stats">
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Round</span>
              <span class="sim__pstat-val font-mono">{{ runStatus.twitter_current_round || 0 }}<span class="sim__pstat-total">/{{ runStatus.total_rounds || maxRounds || '—' }}</span></span>
            </div>
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Elapsed</span>
              <span class="sim__pstat-val font-mono">{{ twitterElapsed }}</span>
            </div>
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Actions</span>
              <span class="sim__pstat-val font-mono">{{ runStatus.twitter_actions_count || 0 }}</span>
            </div>
          </div>
          <div class="sim__actions-row">
            <span class="sim__action-tag label-sm" v-for="a in ['POST','LIKE','REPOST','QUOTE','FOLLOW','IDLE']" :key="a">{{ a }}</span>
          </div>
        </div>

        <!-- Divider -->
        <div class="sim__platform-divider">
          <span class="material-symbols-outlined" style="color:var(--text-muted);font-size:18px">sync</span>
        </div>

        <!-- Topic Community (Reddit-like) -->
        <div class="sim__platform" :class="{'sim__platform--active': runStatus.reddit_running, 'sim__platform--done': runStatus.reddit_completed}">
          <div class="sim__platform-header">
            <span class="material-symbols-outlined" style="font-size:16px">forum</span>
            <span class="label-sm sim__platform-name">Topic Community</span>
            <span v-if="runStatus.reddit_completed" class="chip chip-green" style="margin-left:auto">
              <span class="material-symbols-outlined" style="font-size:11px">check</span> Done
            </span>
            <div v-else-if="runStatus.reddit_running" class="ai-chip" style="margin-left:auto;padding:.2rem .5rem">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">Live</span>
            </div>
          </div>
          <div class="sim__platform-stats">
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Round</span>
              <span class="sim__pstat-val font-mono">{{ runStatus.reddit_current_round || 0 }}<span class="sim__pstat-total">/{{ runStatus.total_rounds || maxRounds || '—' }}</span></span>
            </div>
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Elapsed</span>
              <span class="sim__pstat-val font-mono">{{ redditElapsed }}</span>
            </div>
            <div class="sim__pstat">
              <span class="label-sm sim__pstat-label">Actions</span>
              <span class="sim__pstat-val font-mono">{{ runStatus.reddit_actions_count || 0 }}</span>
            </div>
          </div>
          <div class="sim__actions-row">
            <span class="sim__action-tag label-sm" v-for="a in ['POST','COMMENT','LIKE','SHARE','IDLE']" :key="a">{{ a }}</span>
          </div>
        </div>
      </div>

      <!-- Right: Controls -->
      <div class="sim__controls">
        <button
          v-if="!isRunning && !isCompleted"
          class="btn-primary"
          @click="startSimulation"
          :disabled="isStarting"
        >
          <span class="material-symbols-outlined" style="font-size:18px">{{ isStarting ? 'hourglass_empty' : 'play_arrow' }}</span>
          {{ isStarting ? 'Launching…' : 'Start Simulation' }}
        </button>
        <button v-else-if="isRunning" class="btn-secondary" @click="stopSimulation">
          <span class="material-symbols-outlined" style="font-size:18px">stop</span>
          Stop
        </button>
        <button v-if="isCompleted" class="btn-primary" @click="$emit('completed')">
          View Report
          <span class="material-symbols-outlined" style="font-size:18px">analytics</span>
        </button>
      </div>
    </div>

    <!-- Main Split Layout -->
    <div class="sim__split">
      <!-- LEFT: Action Log -->
      <div class="sim__log card">
        <div class="sim__log-header">
          <div class="sim__log-title">
            <span class="material-symbols-outlined" style="font-size:16px;color:var(--secondary)">terminal</span>
            <span class="label-sm" style="color:var(--text-muted)">Action Log</span>
          </div>
          <div style="display:flex;gap:.5rem;align-items:center">
            <span class="chip chip-muted label-sm">{{ actionLog.length }} events</span>
            <button class="btn-ghost" style="font-size:.6875rem" @click="actionLog = []">Clear</button>
          </div>
        </div>

        <!-- Filter tabs -->
        <div class="sim__log-filters">
          <button
            v-for="f in logFilters"
            :key="f"
            class="sim__filter-tab"
            :class="{'sim__filter-tab--active': activeFilter === f}"
            @click="activeFilter = f"
          >
            {{ f }}
          </button>
        </div>

        <!-- Log entries -->
        <div class="sim__log-body" ref="logBodyRef">
          <div
            v-for="(entry, i) in filteredLog"
            :key="i"
            class="sim__log-entry"
            :class="`sim__log-entry--${entry.platform}`"
          >
            <div class="sim__log-entry-header">
              <span class="sim__log-entry-time font-mono">{{ entry.time }}</span>
              <span class="chip label-sm" :class="entry.platform === 'twitter' ? 'chip-blue' : 'chip-orange'" style="font-size:.55rem">
                {{ entry.platform === 'twitter' ? 'Info Plaza' : 'Topic' }}
              </span>
              <span class="sim__log-entry-action chip chip-muted label-sm">{{ entry.action }}</span>
            </div>
            <div class="sim__log-entry-content">
              <span class="sim__log-entry-agent font-mono">{{ entry.agent }}</span>
              <span class="sim__log-entry-text">{{ entry.text }}</span>
            </div>
          </div>

          <div v-if="!filteredLog.length" class="sim__log-empty">
            <span class="material-symbols-outlined" style="font-size:32px;color:var(--text-muted)">inbox</span>
            <span class="label-sm" style="color:var(--text-muted)">No events yet. Start the simulation.</span>
          </div>
        </div>
      </div>

      <!-- RIGHT: Live Stats + Activity Graph -->
      <div class="sim__right">
        <!-- Live Metrics -->
        <div class="sim__metrics card">
          <span class="label-sm" style="color:var(--text-muted);margin-bottom:.75rem;display:block">Live Metrics</span>
          <div class="sim__metrics-grid">
            <div class="sim__metric card-nested" v-for="m in liveMetrics" :key="m.label">
              <div class="sim__metric-val font-headline">{{ m.value }}</div>
              <div class="label-sm" style="color:var(--text-muted)">{{ m.label }}</div>
              <div v-if="m.trend" class="sim__metric-trend" :class="m.trend > 0 ? 'sim__metric-trend--up' : 'sim__metric-trend--down'">
                <span class="material-symbols-outlined" style="font-size:12px">{{ m.trend > 0 ? 'trending_up' : 'trending_down' }}</span>
                {{ Math.abs(m.trend) }}%
              </div>
            </div>
          </div>
        </div>

        <!-- Activity Heatmap / Mini Graph -->
        <div class="sim__graph card">
          <div class="sim__graph-header">
            <span class="label-sm" style="color:var(--text-muted)">Activity Distribution</span>
            <div style="display:flex;gap:.375rem">
              <span class="sim__legend-dot" style="background:var(--primary-container)"></span>
              <span class="label-sm" style="color:var(--text-muted)">Info Plaza</span>
              <span class="sim__legend-dot" style="background:var(--secondary-container);margin-left:.5rem"></span>
              <span class="label-sm" style="color:var(--text-muted)">Topic</span>
            </div>
          </div>
          <div class="sim__graph-bars">
            <div
              v-for="(bar, i) in activityBars"
              :key="i"
              class="sim__graph-bar-group"
              :title="`Round ${bar.round}`"
            >
              <div class="sim__graph-bar sim__graph-bar--twitter" :style="`height:${bar.twitter}%`"></div>
              <div class="sim__graph-bar sim__graph-bar--reddit"  :style="`height:${bar.reddit}%`"></div>
            </div>
          </div>
          <div class="sim__graph-axis">
            <span class="label-sm" v-for="l in graphAxisLabels" :key="l" style="color:var(--text-muted)">{{ l }}</span>
          </div>
        </div>

        <!-- Agent Status Grid -->
        <div class="sim__agents card">
          <span class="label-sm" style="color:var(--text-muted);margin-bottom:.75rem;display:block">Agent Status</span>
          <div class="sim__agents-grid">
            <div
              v-for="agent in agentGrid"
              :key="agent.id"
              class="sim__agent-dot"
              :class="`sim__agent-dot--${agent.status}`"
              :title="`${agent.name} · ${agent.status}`"
            ></div>
          </div>
          <div class="sim__agents-legend">
            <div class="sim__agents-legend-item" v-for="l in agentLegend" :key="l.label">
              <span class="sim__legend-dot" :style="`background:${l.color}`"></span>
              <span class="label-sm" style="color:var(--text-muted)">{{ l.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, nextTick } from 'vue'

// ─── Props ──────────────────────────────────────────────────────────────────
// simulationId: The sim_xxxx ID returned by Step 2's /api/simulation/create
// projectId: Used to create the simulation if simulationId not yet set
const props = defineProps({
  simulationId: String,
  projectId: String,
})
const emit = defineEmits(['completed'])

// ─── State ───────────────────────────────────────────────────────────────────
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
const API = (path) => `${BASE_URL}/api${path}`

const maxRounds = ref(100)
const isStarting = ref(false)
const isRunning = ref(false)
const isCompleted = ref(false)
const activeFilter = ref('All')
const logBodyRef = ref(null)
const errorMsg = ref('')

// Tracks the last action index we have already ingested from the backend
const lastActionOffset = ref(0)
// The real simulation_id (may differ from prop if we create one here)
const activeSimId = ref(props.simulationId || null)

const logFilters = ['All', 'Info Plaza', 'Topic', 'POST', 'LIKE', 'COMMENT']

let pollTimer = null          // polls /run-status every 3 s
let actionPollTimer = null    // polls /actions every 5 s
let twitterTimer = null
let redditTimer = null
let twitterStart = null
let redditStart  = null

const twitterElapsed = ref('00:00')
const redditElapsed  = ref('00:00')

const runStatus = ref({
  twitter_running: false, twitter_completed: false, twitter_current_round: 0, twitter_actions_count: 0,
  reddit_running:  false, reddit_completed:  false, reddit_current_round:  0, reddit_actions_count:  0,
  total_rounds: 100,
})

const actionLog = ref([])
const activityBars = ref(Array.from({ length: 24 }, (_, i) => ({ round: i * 4, twitter: 0, reddit: 0 })))
const graphAxisLabels = ['0', '25', '50', '75', '100']

const agentGrid = ref(Array.from({ length: 50 }, (_, i) => ({
  id: i,
  name: `Agent_${String(i + 1).padStart(3, '0')}`,
  status: 'idle',
})))

const agentLegend = [
  { label: 'Active',   color: 'var(--primary-container)' },
  { label: 'Thinking', color: 'var(--secondary)' },
  { label: 'Idle',     color: 'var(--surface-container-highest)' },
  { label: 'Done',     color: '#86EFAC' },
]

// ─── Computed ─────────────────────────────────────────────────────────────────
const liveMetrics = computed(() => [
  { label: 'Total Actions',  value: (runStatus.value.twitter_actions_count + runStatus.value.reddit_actions_count).toLocaleString(), trend: isRunning.value ? 12 : null },
  { label: 'Active Agents',  value: agentGrid.value.filter(a => a.status === 'active').length, trend: null },
  { label: 'Posts Created',  value: Math.floor(runStatus.value.twitter_actions_count * 0.35), trend: isRunning.value ? 8 : null },
  { label: 'Interactions',   value: Math.floor(runStatus.value.twitter_actions_count * 0.65), trend: isRunning.value ? 15 : null },
])

const filteredLog = computed(() => {
  const log = actionLog.value.slice().reverse()
  if (activeFilter.value === 'All') return log
  if (activeFilter.value === 'Info Plaza') return log.filter(e => e.platform === 'twitter')
  if (activeFilter.value === 'Topic')      return log.filter(e => e.platform === 'reddit')
  return log.filter(e => e.action === activeFilter.value)
})

// ─── Helpers ──────────────────────────────────────────────────────────────────
function formatElapsed(start) {
  const s = Math.floor((Date.now() - start) / 1000)
  return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`
}

// Map backend action_type strings → short UI labels
function normaliseAction(actionType) {
  if (!actionType) return 'ACT'
  const t = actionType.toUpperCase()
  if (t.includes('POST') || t.includes('CREATE')) return 'POST'
  if (t.includes('LIKE'))   return 'LIKE'
  if (t.includes('REPOST') || t.includes('RETWEET')) return 'REPOST'
  if (t.includes('QUOTE'))  return 'QUOTE'
  if (t.includes('FOLLOW')) return 'FOLLOW'
  if (t.includes('COMMENT')) return 'COMMENT'
  if (t.includes('SHARE'))  return 'SHARE'
  if (t.includes('IDLE'))   return 'IDLE'
  return actionType.slice(0, 8)
}

function ingestAction(a) {
  const action = normaliseAction(a.action_type)
  const platform = (a.platform || 'twitter').toLowerCase()
  const ts = a.timestamp ? new Date(a.timestamp) : new Date()
  const timeStr = `${String(ts.getHours()).padStart(2, '0')}:${String(ts.getMinutes()).padStart(2, '0')}:${String(ts.getSeconds()).padStart(2, '0')}`

  // Extract content from action_args
  const args = a.action_args || {}
  const text = args.content || args.text || args.post_content || args.comment_content || `Round ${a.round_num || '?'} action`

  actionLog.value.push({ time: timeStr, platform, action, agent: a.agent_name || `Agent_${a.agent_id}`, text })
  if (actionLog.value.length > 300) actionLog.value.shift()

  // Animate an agent dot
  const dotIdx = (a.agent_id != null ? a.agent_id : Math.floor(Math.random() * 50)) % 50
  if (agentGrid.value[dotIdx]) {
    agentGrid.value[dotIdx].status = action === 'IDLE' ? 'idle' : 'active'
    setTimeout(() => {
      if (agentGrid.value[dotIdx]) {
        agentGrid.value[dotIdx].status = Math.random() > 0.3 ? 'idle' : 'thinking'
      }
    }, 1200)
  }
}

function updateActivityBars(twitterCount, redditCount, currentRound, totalRounds) {
  const total = totalRounds || maxRounds.value || 100
  const barIdx = Math.min(23, Math.floor((currentRound / total) * 24))
  activityBars.value[barIdx].twitter = Math.min(100, (twitterCount / Math.max(1, total)) * 100 * 5)
  activityBars.value[barIdx].reddit  = Math.min(100, (redditCount  / Math.max(1, total)) * 100 * 5)
}

// ─── Backend calls ────────────────────────────────────────────────────────────
async function apiFetch(url, options = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }))
    throw new Error(err.error || `HTTP ${res.status}`)
  }
  return res.json()
}

// Poll /run-status every 3 s
async function pollRunStatus() {
  if (!activeSimId.value) return
  try {
    const data = await apiFetch(API(`/simulation/${activeSimId.value}/run-status`))
    if (!data.success) return
    const s = data.data

    // Map backend fields → local runStatus shape
    runStatus.value = {
      twitter_running:       s.runner_status === 'running' && (s.twitter_running !== false),
      twitter_completed:     s.twitter_completed || (s.runner_status === 'completed'),
      twitter_current_round: s.twitter_current_round || s.current_round || 0,
      twitter_actions_count: s.twitter_actions_count || 0,
      reddit_running:        s.runner_status === 'running' && (s.reddit_running !== false),
      reddit_completed:      s.reddit_completed || (s.runner_status === 'completed'),
      reddit_current_round:  s.reddit_current_round || s.current_round || 0,
      reddit_actions_count:  s.reddit_actions_count || 0,
      total_rounds:          s.total_rounds || maxRounds.value,
    }

    if (s.total_rounds) maxRounds.value = s.total_rounds

    updateActivityBars(
      runStatus.value.twitter_actions_count,
      runStatus.value.reddit_actions_count,
      runStatus.value.twitter_current_round,
      runStatus.value.total_rounds
    )

    // Detect completion
    if (s.runner_status === 'completed' || s.runner_status === 'finished') {
      markCompleted()
    }
  } catch (e) {
    // Silent — don't spam error UI on poll failures
    console.warn('poll run-status error:', e.message)
  }
}

// Poll /actions every 5 s, fetching only new rows since last offset
async function pollActions() {
  if (!activeSimId.value) return
  try {
    const url = API(`/simulation/${activeSimId.value}/actions?limit=50&offset=${lastActionOffset.value}`)
    const data = await apiFetch(url)
    if (!data.success) return
    const actions = data.data?.actions || []
    if (actions.length) {
      lastActionOffset.value += actions.length
      actions.forEach(ingestAction)
      await nextTick()
      if (logBodyRef.value) logBodyRef.value.scrollTop = 0 // log is reversed
    }
  } catch (e) {
    console.warn('poll actions error:', e.message)
  }
}

// ─── Start / Stop ─────────────────────────────────────────────────────────────
async function startSimulation() {
  isStarting.value = true
  errorMsg.value = ''
  try {
    // If we don't yet have a simulation_id, create one now
    if (!activeSimId.value) {
      if (!props.projectId) throw new Error('No project_id — cannot create simulation')
      const created = await apiFetch(API('/simulation/create'), {
        method: 'POST',
        body: JSON.stringify({ project_id: props.projectId }),
      })
      if (!created.success) throw new Error(created.error || 'Failed to create simulation')
      activeSimId.value = created.data.simulation_id
    }

    // Call /start
    const started = await apiFetch(API('/simulation/start'), {
      method: 'POST',
      body: JSON.stringify({
        simulation_id: activeSimId.value,
        platform: 'parallel',
        max_rounds: maxRounds.value,
      }),
    })
    if (!started.success) throw new Error(started.error || 'Failed to start simulation')

    isRunning.value = true
    isStarting.value = false

    // Start timers
    twitterStart = Date.now()
    redditStart  = Date.now()
    twitterTimer = setInterval(() => { twitterElapsed.value = formatElapsed(twitterStart) }, 1000)
    redditTimer  = setInterval(() => { redditElapsed.value  = formatElapsed(redditStart)  }, 1000)

    // Start polling
    pollTimer       = setInterval(pollRunStatus, 3000)
    actionPollTimer = setInterval(pollActions,   5001)

    // Immediate first poll
    pollRunStatus()
    pollActions()

  } catch (e) {
    errorMsg.value = `Start failed: ${e.message}`
    isStarting.value = false
  }
}

async function stopSimulation() {
  try {
    await apiFetch(API('/simulation/stop'), {
      method: 'POST',
      body: JSON.stringify({ simulation_id: activeSimId.value }),
    })
  } catch (e) {
    errorMsg.value = `Stop failed: ${e.message}`
  }
  clearPolling()
  isRunning.value = false
  runStatus.value.twitter_running = false
  runStatus.value.reddit_running  = false
}

function markCompleted() {
  if (isCompleted.value) return
  clearPolling()
  isRunning.value   = false
  isCompleted.value = true
  agentGrid.value.forEach(a => { a.status = 'done' })
  // Final action fetch
  pollActions()
}

function clearPolling() {
  clearInterval(pollTimer)
  clearInterval(actionPollTimer)
  clearInterval(twitterTimer)
  clearInterval(redditTimer)
}

onUnmounted(clearPolling)
</script>

<style scoped>
.sim { display: flex; flex-direction: column; gap: 1.25rem; }

.sim__error-banner {
  display: flex;
  align-items: center;
  gap: .5rem;
  padding: .75rem 1.25rem;
  background: rgba(239,68,68,.08);
  border: 1px solid rgba(239,68,68,.25);
  border-radius: var(--radius-md);
  color: #f87171;
  font-size: .8125rem;
}

/* Control Bar */
.sim__control-bar {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  border-radius: var(--radius-xl);
  flex-wrap: wrap;
}

.sim__platforms {
  display: flex;
  align-items: stretch;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

.sim__platform {
  flex: 1;
  background: var(--surface-container);
  border-radius: var(--radius-md);
  padding: 1rem;
  border: 1px solid var(--ghost-border);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}
.sim__platform--active {
  border-color: rgba(182, 196, 255, 0.3);
  box-shadow: var(--shadow-glow-ai);
}
.sim__platform--done {
  border-color: rgba(134, 239, 172, 0.2);
}

.sim__platform-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.sim__platform-name { color: var(--text-secondary); }

.sim__platform-stats {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 0.75rem;
}

.sim__pstat { display: flex; flex-direction: column; gap: 0.125rem; }
.sim__pstat-label { color: var(--text-muted); font-size: 0.6rem; }
.sim__pstat-val { font-size: 1.125rem; font-weight: 700; color: var(--text-primary); }
.sim__pstat-total { font-size: 0.75rem; color: var(--text-muted); font-weight: 400; }

.sim__actions-row { display: flex; flex-wrap: wrap; gap: 0.25rem; }
.sim__action-tag {
  padding: 0.125rem 0.375rem;
  background: var(--surface-container-high);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  font-size: 0.55rem;
  letter-spacing: 0.06em;
}

.sim__platform-divider { display: flex; align-items: center; padding: 0 0.25rem; }

.sim__controls {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* Split */
.sim__split {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 1.25rem;
  align-items: start;
}

/* Log */
.sim__log { display: flex; flex-direction: column; max-height: 600px; overflow: hidden; }

.sim__log-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem 0.75rem;
}

.sim__log-title { display: flex; align-items: center; gap: 0.5rem; }

.sim__log-filters {
  display: flex;
  gap: 0.25rem;
  padding: 0 1.25rem 0.75rem;
  border-bottom: 1px solid var(--ghost-border);
  flex-wrap: wrap;
}

.sim__filter-tab {
  padding: 0.25rem 0.625rem;
  background: transparent;
  border: 1px solid var(--ghost-border);
  border-radius: var(--radius-full);
  color: var(--text-muted);
  font-size: 0.6875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast);
  font-family: var(--font-body);
  letter-spacing: 0.04em;
}
.sim__filter-tab:hover { border-color: rgba(171,137,127,.4); color: var(--text-secondary); }
.sim__filter-tab--active {
  background: rgba(255,90,31,.12);
  border-color: rgba(255,90,31,.3);
  color: var(--primary);
}

.sim__log-body {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  max-height: 460px;
}

.sim__log-entry {
  padding: 0.625rem 0.75rem;
  border-radius: var(--radius-md);
  background: var(--surface-low);
  border-left: 2px solid var(--ghost-border);
  animation: fade-in 200ms ease both;
}
.sim__log-entry--twitter { border-left-color: rgba(182,196,255,.4); }
.sim__log-entry--reddit  { border-left-color: rgba(255,181,158,.4); }

.sim__log-entry-header {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.25rem;
}

.sim__log-entry-time { font-size: 0.625rem; color: var(--text-muted); }

.sim__log-entry-content { display: flex; align-items: baseline; gap: 0.5rem; }
.sim__log-entry-agent { font-size: 0.6875rem; color: var(--secondary); flex-shrink: 0; }
.sim__log-entry-text { font-size: 0.75rem; color: var(--text-secondary); }

.sim__log-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 3rem 1rem;
}

/* Right Panel */
.sim__right { display: flex; flex-direction: column; gap: 1rem; }
.sim__metrics { padding: 1.25rem; }
.sim__metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.625rem; }
.sim__metric { padding: .75rem; }
.sim__metric-val { font-size: 1.375rem; font-weight: 700; color: var(--primary); margin-bottom: 0.125rem; }
.sim__metric-trend {
  display: flex; align-items: center; gap: 0.125rem;
  font-size: 0.625rem; font-weight: 700; margin-top: 0.25rem;
}
.sim__metric-trend--up   { color: #86EFAC; }
.sim__metric-trend--down { color: var(--error); }

/* Graph */
.sim__graph { padding: 1.25rem; }
.sim__graph-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.sim__graph-bars { display: flex; align-items: flex-end; gap: 2px; height: 80px; }
.sim__graph-bar-group { flex: 1; display: flex; align-items: flex-end; gap: 1px; height: 100%; }
.sim__graph-bar { flex: 1; border-radius: 2px 2px 0 0; min-height: 2px; transition: height 300ms var(--ease-out); }
.sim__graph-bar--twitter { background: var(--primary-container); opacity: 0.85; }
.sim__graph-bar--reddit  { background: var(--secondary-container); opacity: 0.85; }
.sim__graph-axis { display: flex; justify-content: space-between; margin-top: 0.375rem; }
.sim__legend-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

/* Agents */
.sim__agents { padding: 1.25rem; }
.sim__agents-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; margin-bottom: 0.75rem; }
.sim__agent-dot { width: 100%; aspect-ratio: 1; border-radius: 3px; cursor: pointer; transition: transform var(--duration-fast); }
.sim__agent-dot:hover { transform: scale(1.3); }
.sim__agent-dot--idle     { background: var(--surface-container-highest); }
.sim__agent-dot--active   { background: var(--primary-container); box-shadow: 0 0 4px rgba(255,90,31,.4); }
.sim__agent-dot--thinking { background: var(--secondary); box-shadow: 0 0 4px rgba(182,196,255,.4); }
.sim__agent-dot--done     { background: #86EFAC; }
.sim__agents-legend { display: flex; gap: 0.875rem; flex-wrap: wrap; }
.sim__agents-legend-item { display: flex; align-items: center; gap: 0.375rem; }

@media (max-width: 1100px) {
  .sim__split { grid-template-columns: 1fr; }
}
</style>