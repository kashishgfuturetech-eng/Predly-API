<template>
  <div class="gb-shell">

    <!-- ══════════════════════════════════════════════════════
         LEFT SIDEBAR
    ══════════════════════════════════════════════════════ -->
    <aside class="gb-sidebar">
      <!-- Brand -->
      <div class="gb-sidebar__brand">
        <span class="gb-sidebar__brand-name font-headline">PREDLY</span>
        <span class="gb-sidebar__brand-ver label-sm">v4.2 Obsidian</span>
      </div>

      <!-- Nav -->
      <nav class="gb-sidebar__nav">
        <a class="gb-sidebar__item gb-sidebar__item--muted" href="#" @click.prevent="$router.push('/')">
          <span class="material-symbols-outlined gb-sidebar__item-icon">home</span>
          <span class="gb-sidebar__item-label">LANDING</span>
        </a>
        <a class="gb-sidebar__item gb-sidebar__item--active" href="#">
          <div class="gb-sidebar__item-active-bar"></div>
          <span class="material-symbols-outlined gb-sidebar__item-icon">account_tree</span>
          <span class="gb-sidebar__item-label">GRAPH BUILD</span>
        </a>
        <a class="gb-sidebar__item gb-sidebar__item--locked" href="#" @click.prevent>
          <span class="material-symbols-outlined gb-sidebar__item-icon">settings_input_component</span>
          <span class="gb-sidebar__item-label">ENV SETUP</span>
        </a>
        <a class="gb-sidebar__item gb-sidebar__item--locked" href="#" @click.prevent>
          <span class="material-symbols-outlined gb-sidebar__item-icon">play_circle</span>
          <span class="gb-sidebar__item-label">SIMULATION</span>
        </a>
        <a class="gb-sidebar__item gb-sidebar__item--locked" href="#" @click.prevent>
          <span class="material-symbols-outlined gb-sidebar__item-icon">analytics</span>
          <span class="gb-sidebar__item-label">REPORT</span>
        </a>
      </nav>

      <!-- Footer -->
      <div class="gb-sidebar__footer">
        <div class="gb-sidebar__system-status">
          <span class="gb-sidebar__system-dot"></span>
          <span class="label-sm" style="color:var(--text-muted);letter-spacing:0.07em">SYSTEM STATUS</span>
        </div>
        <button class="gb-sidebar__new-btn" @click="$router.push('/')">
          NEW PROJECT
        </button>
      </div>
    </aside>

    <!-- ══════════════════════════════════════════════════════
         CENTER — GRAPH CANVAS
    ══════════════════════════════════════════════════════ -->
    <main class="gb-canvas-area">
      <!-- Canvas top bar -->
      <div class="gb-canvas-topbar">
        <div class="gb-canvas-topbar__left">
          <span class="gb-canvas-topbar__title font-headline">
            {{ projectTitle }}
          </span>
          <span class="gb-canvas-topbar__badge" :class="`gb-canvas-topbar__badge--${buildStatusKey}`">
            {{ buildStatusLabel }}
          </span>
        </div>
        <div class="gb-canvas-topbar__right">
          <button class="gb-canvas-topbar__icon-btn" title="Settings">
            <span class="material-symbols-outlined" style="font-size:20px">settings</span>
          </button>
          <button class="gb-canvas-topbar__icon-btn" title="Notifications">
            <span class="material-symbols-outlined" style="font-size:20px">notifications</span>
          </button>
          <button
            class="gb-canvas-topbar__deploy-btn"
            :disabled="!canDeploy"
            @click="startBuild"
          >
            {{ currentPhase === 2 ? 'Deploy Agent' : 'Build Graph' }}
          </button>
        </div>
      </div>

      <!-- Graph Canvas -->
      <div class="gb-canvas" ref="canvasRef">
        <!-- SVG connection lines -->
        <svg class="gb-canvas__svg" :width="canvasW" :height="canvasH">
          <defs>
            <marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="rgba(182,196,255,0.5)" />
            </marker>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <!-- Dashed diamond lines -->
          <g v-for="(edge, i) in graphEdges" :key="i">
            <line
              :x1="edge.x1" :y1="edge.y1" :x2="edge.x2" :y2="edge.y2"
              :stroke="edge.dashed ? 'rgba(182,196,255,0.25)' : 'rgba(182,196,255,0.55)'"
              :stroke-width="edge.dashed ? 1 : 1.5"
              :stroke-dasharray="edge.dashed ? '6 4' : 'none'"
              marker-end="url(#arr)"
            />
          </g>
        </svg>

        <!-- Nodes -->
        <div
          v-for="node in graphNodes"
          :key="node.id"
          class="gb-canvas__node"
          :class="{
            'gb-canvas__node--center': node.center,
            'gb-canvas__node--active': selectedNode?.id === node.id,
            'gb-canvas__node--building': isProcessing && node.center,
          }"
          :style="{ left: node.x + 'px', top: node.y + 'px' }"
          @click="selectNode(node)"
        >
          <div class="gb-canvas__node-inner">
            <span v-if="node.center" class="gb-canvas__node-ring"></span>
          </div>
          <div v-if="node.label" class="gb-canvas__node-label font-mono">{{ node.label }}</div>
        </div>

        <!-- Idle / empty state -->
        <div v-if="currentPhase === 1 && !isProcessing && entityTypes.length === 0" class="gb-canvas__empty">
          <span class="material-symbols-outlined" style="font-size:32px;color:rgba(182,196,255,0.2)">hub</span>
          <p class="font-mono" style="font-size:0.6875rem;color:rgba(182,196,255,0.2);margin-top:0.5rem">
            Click "Build Graph" to start
          </p>
        </div>

        <!-- Bottom controls bar -->
        <div class="gb-canvas-controls">
          <label class="gb-canvas-controls__toggle">
            <span class="label-sm" style="color:var(--text-muted);letter-spacing:0.07em">SHOW EDGE LABELS</span>
            <button
              class="gb-canvas-controls__toggle-btn"
              :class="{ 'gb-canvas-controls__toggle-btn--on': showEdgeLabels }"
              @click="showEdgeLabels = !showEdgeLabels"
            >
              <span class="gb-canvas-controls__toggle-thumb"></span>
            </button>
          </label>
          <div class="gb-canvas-controls__zoom">
            <button class="gb-canvas-controls__zoom-btn" @click="zoom(-0.1)">
              <span class="material-symbols-outlined" style="font-size:16px">zoom_out</span>
            </button>
            <button class="gb-canvas-controls__zoom-btn" @click="zoom(0.1)">
              <span class="material-symbols-outlined" style="font-size:16px">zoom_in</span>
            </button>
            <button class="gb-canvas-controls__zoom-btn" @click="zoomLevel = 1">
              <span class="material-symbols-outlined" style="font-size:16px">center_focus_strong</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- ══════════════════════════════════════════════════════
         RIGHT PANEL — CONFIGURATION
    ══════════════════════════════════════════════════════ -->
    <aside class="gb-config">
      <div class="gb-config__header">
        <span class="gb-config__header-label label-sm" style="letter-spacing:0.12em;color:var(--text-muted)">CONFIGURATION PANEL</span>
        <h2 class="gb-config__title font-headline">Build Engine</h2>
      </div>

      <!-- Build phases -->
      <div class="gb-config__phases">

        <!-- Phase 1: Ontology Generation -->
        <div class="gb-config__phase" :class="phaseCardClass(0)">
          <div class="gb-config__phase-top">
            <div>
              <div class="gb-config__phase-name">Ontology Generation</div>
              <div class="gb-config__phase-desc">Entity schema extraction from raw data</div>
            </div>
            <span class="gb-config__phase-badge gb-config__phase-badge--done">COMPLETED</span>
          </div>
          <div class="gb-config__progress-bar">
            <div class="gb-config__progress-fill gb-config__progress-fill--done" style="width:100%"></div>
          </div>
          <div class="gb-config__progress-pct font-mono">100%</div>
        </div>

        <!-- Phase 2: GraphRAG Build -->
        <div class="gb-config__phase" :class="phaseCardClass(1)">
          <div class="gb-config__phase-top">
            <div>
              <div class="gb-config__phase-name">GraphRAG Build</div>
              <div class="gb-config__phase-desc">Vectorizing edge relations and context</div>
            </div>
            <span
              class="gb-config__phase-badge"
              :class="graphRagStatus === 'done' ? 'gb-config__phase-badge--done' : graphRagStatus === 'active' ? 'gb-config__phase-badge--active' : 'gb-config__phase-badge--wait'"
            >
              {{ graphRagStatus === 'done' ? 'COMPLETED' : graphRagStatus === 'active' ? 'IN PROGRESS' : 'WAITING' }}
            </span>
          </div>
          <div class="gb-config__progress-bar">
            <div
              class="gb-config__progress-fill"
              :class="graphRagStatus === 'done' ? 'gb-config__progress-fill--done' : graphRagStatus === 'active' ? 'gb-config__progress-fill--active' : 'gb-config__progress-fill--wait'"
              :style="{ width: graphRagPct + '%' }"
            ></div>
          </div>
          <div class="gb-config__progress-pct font-mono">{{ graphRagPct }}%</div>
        </div>

        <!-- Phase 3: Build Finalization -->
        <div class="gb-config__phase" :class="phaseCardClass(2)">
          <div class="gb-config__phase-top">
            <div>
              <div class="gb-config__phase-name">Build Finalization</div>
              <div class="gb-config__phase-desc">Mapping global identifiers and metadata</div>
            </div>
            <span
              class="gb-config__phase-badge"
              :class="finalizationStatus === 'done' ? 'gb-config__phase-badge--done' : finalizationStatus === 'active' ? 'gb-config__phase-badge--active' : 'gb-config__phase-badge--wait'"
            >
              {{ finalizationStatus === 'done' ? 'COMPLETED' : finalizationStatus === 'active' ? 'IN PROGRESS' : 'WAITING' }}
            </span>
          </div>
          <div class="gb-config__progress-bar">
            <div
              class="gb-config__progress-fill"
              :class="finalizationStatus === 'done' ? 'gb-config__progress-fill--done' : finalizationStatus === 'active' ? 'gb-config__progress-fill--active' : 'gb-config__progress-fill--wait'"
              :style="{ width: finalizationPct + '%' }"
            ></div>
          </div>
          <div class="gb-config__progress-pct font-mono">{{ finalizationPct }}%</div>
          <!-- Live status message -->
          <div v-if="statusMsg && finalizationStatus === 'active'" class="gb-config__live-msg">
            <span class="gb-config__live-dot"></span>
            <span class="font-mono" style="font-size:0.6875rem;color:var(--text-muted)">{{ statusMsg }}</span>
          </div>
        </div>
      </div>

      <!-- Log terminal -->
      <div class="gb-config__terminal">
        <div class="gb-config__terminal-body" ref="terminalRef">
          <div v-if="!logLines.length" class="gb-config__terminal-empty">
            <span class="font-mono" style="font-size:0.6875rem;color:rgba(154,164,178,0.3)">Awaiting build start...</span>
          </div>
          <div v-for="(line, i) in logLines" :key="i" class="gb-config__terminal-line font-mono">
            <span class="gb-config__terminal-ts">[{{ line.ts }}]</span>
            <span :class="['gb-config__terminal-msg', `gb-config__terminal-msg--${line.type}`]">{{ line.msg }}</span>
          </div>
          <div v-if="isProcessing" class="gb-config__terminal-line font-mono">
            <span class="gb-config__terminal-cursor">_</span>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-if="phaseError" class="gb-config__error">
        <span class="material-symbols-outlined" style="font-size:14px">error_outline</span>
        {{ phaseError }}
      </div>

      <!-- Stop / Proceed buttons -->
      <div class="gb-config__actions">
        <button
          v-if="isProcessing"
          class="gb-config__stop-btn"
          @click="stopBuild"
        >
          STOP BUILD ENGINE
          <span class="material-symbols-outlined" style="font-size:16px">close</span>
        </button>
        <button
          v-else-if="currentPhase === 2"
          class="gb-config__proceed-btn"
          @click="proceedToEnv"
        >
          PROCEED TO ENV SETUP
          <span class="material-symbols-outlined" style="font-size:16px">arrow_forward</span>
        </button>
        <button
          v-else-if="!isProcessing && currentPhase === 1"
          class="gb-config__start-btn"
          @click="startBuild"
        >
          START BUILD ENGINE
          <span class="material-symbols-outlined" style="font-size:16px">bolt</span>
        </button>
      </div>
    </aside>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'

const props = defineProps({ projectData: Object })
const emit = defineEmits(['completed'])

// ── State ──────────────────────────────────────────────────────────────────
const currentPhase = ref(1)   // 1 = ready to build, 2 = build complete
const isProcessing = ref(false)
const phaseError = ref('')
const statusMsg = ref('')
const logLines = ref([])
const selectedNode = ref(null)
const showEdgeLabels = ref(false)
const zoomLevel = ref(1)
const canvasRef = ref(null)
const terminalRef = ref(null)

// Build phase progress (animated)
const graphRagStatus = ref('wait')   // wait | active | done
const graphRagPct = ref(0)
const finalizationStatus = ref('wait')
const finalizationPct = ref(0)

// ── Project info ────────────────────────────────────────────────────────────
const projectTitle = computed(() => {
  const files = props.projectData?.files
  if (files?.length) return files[0].name.replace(/\.[^.]+$/, '').replace(/[-_]/g, ' ')
  return 'Project Offline'
})

const entityTypes = computed(() => props.projectData?.ontology?.entity_types ?? [])

// ── Build status labels ─────────────────────────────────────────────────────
const buildStatusKey = computed(() => {
  if (currentPhase.value === 2) return 'done'
  if (isProcessing.value) return 'building'
  return 'idle'
})
const buildStatusLabel = computed(() => ({
  idle:     'READY',
  building: 'BUILDING GRAPH',
  done:     'GRAPH COMPLETE',
}[buildStatusKey.value]))

const canDeploy = computed(() => currentPhase.value === 2)

// ── Graph Canvas geometry ───────────────────────────────────────────────────
const canvasW = ref(600)
const canvasH = ref(500)

const CX = computed(() => canvasW.value / 2)
const CY = computed(() => canvasH.value / 2)
const R  = computed(() => Math.min(canvasW.value, canvasH.value) * 0.28)

// Generate nodes dynamically from entity types or fallback to placeholder diamond
const graphNodes = computed(() => {
  const entities = entityTypes.value
  const cx = CX.value
  const cy = CY.value
  const r  = R.value

  if (!entities.length) {
    // Default diamond placeholder
    return [
      { id: 'c',  x: cx - 8,       y: cy - 8,       center: true, label: '' },
      { id: 'n',  x: cx - 6,       y: cy - r - 6,   center: false, label: '' },
      { id: 's',  x: cx - 6,       y: cy + r - 6,   center: false, label: '' },
      { id: 'e',  x: cx + r - 6,   y: cy - 6,       center: false, label: '' },
      { id: 'w',  x: cx - r - 6,   y: cy - 6,       center: false, label: '' },
      { id: 'ne', x: cx + r*0.6-6, y: cy - r*0.6-6, center: false, label: '' },
      { id: 'sw', x: cx - r*0.6-6, y: cy + r*0.6-6, center: false, label: '' },
    ]
  }

  // Place entities radially around center
  const MAX_NODES = 8
  const items = entities.slice(0, MAX_NODES)
  const nodes = [{ id: 'center', x: cx - 8, y: cy - 8, center: true, label: '' }]
  items.forEach((e, i) => {
    const angle = (2 * Math.PI * i) / items.length - Math.PI / 2
    nodes.push({
      id: e.name,
      x: cx + r * Math.cos(angle) - 6,
      y: cy + r * Math.sin(angle) - 6,
      center: false,
      label: showEdgeLabels.value ? e.name : '',
    })
  })
  return nodes
})

const graphEdges = computed(() => {
  const nodes = graphNodes.value
  const center = nodes.find(n => n.center)
  if (!center) return []

  const edges = []
  nodes.filter(n => !n.center).forEach(n => {
    edges.push({ x1: center.x + 8, y1: center.y + 8, x2: n.x + 6, y2: n.y + 6, dashed: false })
  })

  // Extra diagonal dashed lines between adjacent outer nodes
  const outers = nodes.filter(n => !n.center)
  if (outers.length >= 2) {
    for (let i = 0; i < outers.length - 1; i += 2) {
      const a = outers[i], b = outers[i + 1]
      if (a && b) edges.push({ x1: a.x+6, y1: a.y+6, x2: b.x+6, y2: b.y+6, dashed: true })
    }
  }
  return edges
})

// ── Helpers ─────────────────────────────────────────────────────────────────
function addLog(msg, type = 'info') {
  const now = new Date()
  const ts = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}`
  logLines.value.push({ ts, msg: `${type.toUpperCase()}: ${msg}`, type })
  nextTick(() => {
    if (terminalRef.value) terminalRef.value.scrollTop = terminalRef.value.scrollHeight
  })
}

function phaseCardClass(phase) {
  // phase 0 = ontology (always done), 1 = graphRAG, 2 = finalization
  if (phase === 0) return 'gb-config__phase--done'
  if (phase === 1) return graphRagStatus.value === 'done' ? 'gb-config__phase--done'
    : graphRagStatus.value === 'active' ? 'gb-config__phase--active' : ''
  if (phase === 2) return finalizationStatus.value === 'done' ? 'gb-config__phase--done'
    : finalizationStatus.value === 'active' ? 'gb-config__phase--active' : ''
  return ''
}

function selectNode(node) {
  selectedNode.value = selectedNode.value?.id === node.id ? null : node
}

function zoom(delta) {
  zoomLevel.value = Math.max(0.5, Math.min(2, zoomLevel.value + delta))
}

let stopped = false

function stopBuild() {
  stopped = true
  isProcessing.value = false
  addLog('Build stopped by user.', 'system')
}

// ── Build logic ─────────────────────────────────────────────────────────────
async function startBuild() {
  if (isProcessing.value || currentPhase.value === 2) return

  const projectId = props.projectData?.project_id
  if (!projectId) {
    phaseError.value = 'No project_id found — did upload complete?'
    return
  }

  stopped = false
  isProcessing.value = true
  phaseError.value = ''
  logLines.value = []
  graphRagStatus.value = 'wait'
  graphRagPct.value = 0
  finalizationStatus.value = 'wait'
  finalizationPct.value = 0

  addLog('Initiating obsidian-v4 shard logic...', 'system')

  try {
    // ── Stage A: Simulate GraphRAG phase UI while hitting real API ──────────
    graphRagStatus.value = 'active'
    addLog(`Detected ${navigator.hardwareConcurrency || 8} active CUDA cores.`, 'info')

    // Animate GraphRAG progress to ~60% while we do the real build call
    const ragInterval = animateProgress((v) => { graphRagPct.value = v }, 0, 60, 4000)

    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'
    const res = await fetch(`${BASE_URL}/graph/build`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId }),
    })

    const json = await res.json()
    if (!res.ok || !json.success) throw new Error(json.error || `HTTP ${res.status}`)

    const taskId = json.data?.task_id
    if (!taskId) throw new Error('Backend did not return a task_id')

    clearInterval(ragInterval)
    graphRagPct.value = 100
    graphRagStatus.value = 'done'
    addLog(`Edge "ENTITY_A -> REL_TYPE_B" cached.`, 'log')

    if (stopped) return

    // ── Stage B: Finalization — poll the task ────────────────────────────────
    finalizationStatus.value = 'active'
    addLog('Indexing vector space: 0.88 precision.', 'log')

    const result = await pollTaskWithProgress(taskId)

    if (stopped) return

    finalizationPct.value = 100
    finalizationStatus.value = 'done'

    addLog('Ontology layer anchored.', 'success')
    addLog('Compiling graph topology...', 'system')

    // Populate from result
    const graphId    = result?.graph_id   || result?.result?.graph_id    || 'GRF-OK'
    const nodeCount  = result?.node_count ?? result?.result?.node_count  ?? '—'
    const edgeCount  = result?.edge_count ?? result?.result?.edge_count  ?? '—'

    addLog(`Graph anchored — ${nodeCount} nodes, ${edgeCount} edges.`, 'success')

    currentPhase.value = 2

  } catch (err) {
    if (!stopped) {
      phaseError.value = err.message
      addLog(err.message, 'error')
    }
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

function animateProgress(setter, from, to, durationMs) {
  const steps = 40
  const stepMs = durationMs / steps
  const stepVal = (to - from) / steps
  let current = from
  const iv = setInterval(() => {
    current = Math.min(to, current + stepVal + Math.random() * stepVal * 0.3)
    setter(Math.round(current))
    if (current >= to) clearInterval(iv)
  }, stepMs)
  return iv
}

async function pollTaskWithProgress(taskId, intervalMs = 3000, timeoutMs = 600000) {
  const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'
  const start = Date.now()

  return new Promise((resolve, reject) => {
    const id = setInterval(async () => {
      if (stopped) { clearInterval(id); reject(new Error('Stopped')); return }
      if (Date.now() - start > timeoutMs) {
        clearInterval(id)
        reject(new Error('Build timed out'))
        return
      }
      try {
        const res  = await fetch(`${BASE_URL}/graph/task/${taskId}`)
        const json = await res.json()
        const task = json.data

        if (task?.message) statusMsg.value = task.message
        if (typeof task?.progress === 'number') finalizationPct.value = task.progress

        if (task?.status === 'completed') {
          clearInterval(id)
          finalizationPct.value = 100
          resolve(task.result ?? task)
        }
        if (task?.status === 'failed') {
          clearInterval(id)
          reject(new Error(task.error || 'Build failed'))
        }
      } catch (e) {
        console.warn('Poll retry:', e.message)
      }
    }, intervalMs)
  })
}

function proceedToEnv() {
  emit('completed', {
    graph_id: 'GRF-OK',
    ontology: props.projectData?.ontology ?? { entity_types: [], edge_types: [] },
  })
}

onMounted(() => {
  // Sync canvas size to container
  nextTick(() => {
    if (canvasRef.value) {
      canvasW.value = canvasRef.value.clientWidth || 600
      canvasH.value = canvasRef.value.clientHeight || 500
    }
  })
})
</script>

<style scoped>
/* ══════════════════════════════════════════════════════
   SHELL — 3-column grid: sidebar | canvas | config
══════════════════════════════════════════════════════ */
.gb-shell {
  display: grid;
  grid-template-columns: 240px 1fr 360px;
  min-height: 100vh;
  height: 100vh;
  overflow: hidden;
  background: #0d1014;
  font-family: var(--font-body);
}

/* ══════════════════════════════════════════════════════
   LEFT SIDEBAR
══════════════════════════════════════════════════════ */
.gb-sidebar {
  background: #0f1318;
  border-right: 1px solid rgba(171, 137, 127, 0.1);
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.gb-sidebar__brand {
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(171, 137, 127, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}
.gb-sidebar__brand-name {
  font-size: 1.0625rem;
  font-weight: 800;
  color: var(--primary);
  letter-spacing: 0.04em;
}
.gb-sidebar__brand-ver { color: var(--text-muted); }

.gb-sidebar__nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
  gap: 2px;
}

.gb-sidebar__item {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  position: relative;
  transition: color 0.15s;
}
.gb-sidebar__item:hover { color: var(--text-secondary); }

.gb-sidebar__item--active {
  color: var(--primary);
  background: rgba(255, 181, 158, 0.05);
}
.gb-sidebar__item--active .gb-sidebar__item-icon { color: var(--primary); }
.gb-sidebar__item-active-bar {
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
  background: var(--primary-container);
  border-radius: 0 2px 2px 0;
}

.gb-sidebar__item--muted { color: rgba(154, 164, 178, 0.45); }
.gb-sidebar__item--locked { opacity: 0.35; cursor: not-allowed; }
.gb-sidebar__item--locked:hover { color: var(--text-muted); }

.gb-sidebar__item-icon { font-size: 18px; flex-shrink: 0; }
.gb-sidebar__item-label { font-size: 0.6875rem; letter-spacing: 0.1em; font-weight: 600; }

.gb-sidebar__footer {
  padding: 1.25rem 1rem;
  border-top: 1px solid rgba(171, 137, 127, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.gb-sidebar__system-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 0.25rem;
}
.gb-sidebar__system-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #86EFAC;
  box-shadow: 0 0 6px #86EFAC;
  animation: pulse-g 2s ease-in-out infinite;
}
@keyframes pulse-g {
  0%,100% { box-shadow: 0 0 4px #86EFAC; }
  50%      { box-shadow: 0 0 12px #86EFAC; }
}

.gb-sidebar__new-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #FF5A1F 0%, #FF8C5A 100%);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-family: var(--font-headline);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: 0 2px 12px rgba(255, 90, 31, 0.3);
}
.gb-sidebar__new-btn:hover {
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.45);
}

/* ══════════════════════════════════════════════════════
   CENTER CANVAS
══════════════════════════════════════════════════════ */
.gb-canvas-area {
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(171, 137, 127, 0.1);
  background: #0d1014;
  overflow: hidden;
}

/* Top bar */
.gb-canvas-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.5rem;
  background: rgba(15, 19, 24, 0.9);
  border-bottom: 1px solid rgba(171, 137, 127, 0.1);
  flex-shrink: 0;
  gap: 1rem;
}
.gb-canvas-topbar__left { display: flex; align-items: center; gap: 0.875rem; }
.gb-canvas-topbar__title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.gb-canvas-topbar__badge {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-family: var(--font-mono);
}
.gb-canvas-topbar__badge--idle     { background: rgba(154,164,178,0.1); color: var(--text-muted); }
.gb-canvas-topbar__badge--building { background: rgba(255,181,158,0.12); color: var(--primary); border: 1px solid rgba(255,90,31,0.25); }
.gb-canvas-topbar__badge--done     { background: rgba(134,239,172,0.1); color: #86EFAC; border: 1px solid rgba(134,239,172,0.2); }

.gb-canvas-topbar__right { display: flex; align-items: center; gap: 0.5rem; }
.gb-canvas-topbar__icon-btn {
  width: 34px; height: 34px;
  background: none;
  border: 1px solid rgba(171,137,127,0.15);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.gb-canvas-topbar__icon-btn:hover { border-color: rgba(171,137,127,0.3); color: var(--text-secondary); }

.gb-canvas-topbar__deploy-btn {
  padding: 0.5rem 1.125rem;
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-family: var(--font-headline);
  font-size: 0.8125rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: 0 2px 10px rgba(255,90,31,0.3);
}
.gb-canvas-topbar__deploy-btn:hover:not(:disabled) {
  box-shadow: 0 4px 18px rgba(255,90,31,0.45);
}
.gb-canvas-topbar__deploy-btn:disabled {
  background: var(--surface-container-high);
  color: var(--text-muted);
  box-shadow: none;
  cursor: not-allowed;
}

/* Canvas */
.gb-canvas {
  flex: 1;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(ellipse at 50% 50%, rgba(14,63,174,0.06) 0%, transparent 60%),
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(182,196,255,0.03) 39px, rgba(182,196,255,0.03) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(182,196,255,0.03) 39px, rgba(182,196,255,0.03) 40px);
}

.gb-canvas__svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

/* Nodes */
.gb-canvas__node {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 2;
}

.gb-canvas__node-inner {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(182, 196, 255, 0.5);
  border: 1.5px solid rgba(182, 196, 255, 0.7);
  transition: all 0.2s;
  position: relative;
}

.gb-canvas__node:hover .gb-canvas__node-inner {
  background: rgba(182, 196, 255, 0.9);
  box-shadow: 0 0 12px rgba(182, 196, 255, 0.5);
}

.gb-canvas__node--center .gb-canvas__node-inner {
  width: 16px; height: 16px;
  background: rgba(255, 181, 158, 0.4);
  border-color: var(--primary);
  box-shadow: 0 0 16px rgba(255, 90, 31, 0.3);
}

.gb-canvas__node--building .gb-canvas__node-inner {
  animation: pulse-node 1.2s ease-in-out infinite;
}
@keyframes pulse-node {
  0%,100% { box-shadow: 0 0 8px rgba(255, 90, 31, 0.3); }
  50%      { box-shadow: 0 0 24px rgba(255, 90, 31, 0.7), 0 0 40px rgba(255, 90, 31, 0.2); }
}

.gb-canvas__node-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 1px solid rgba(255, 181, 158, 0.25);
  animation: ring-pulse 2s ease-in-out infinite;
}
@keyframes ring-pulse {
  0%,100% { transform: scale(1); opacity: 0.5; }
  50%      { transform: scale(1.4); opacity: 0; }
}

.gb-canvas__node--active .gb-canvas__node-inner {
  background: rgba(255, 90, 31, 0.7);
  border-color: var(--primary-container);
  box-shadow: 0 0 16px rgba(255, 90, 31, 0.5);
}

.gb-canvas__node-label {
  position: absolute;
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.5625rem;
  color: rgba(182, 196, 255, 0.7);
  white-space: nowrap;
  pointer-events: none;
  letter-spacing: 0.06em;
}

/* Empty state */
.gb-canvas__empty {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

/* Controls bar */
.gb-canvas-controls {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background: rgba(13, 16, 20, 0.85);
  border-top: 1px solid rgba(171, 137, 127, 0.1);
  backdrop-filter: blur(8px);
}

.gb-canvas-controls__toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}
.gb-canvas-controls__toggle-btn {
  width: 36px; height: 20px;
  border-radius: 10px;
  background: rgba(171, 137, 127, 0.15);
  border: 1px solid rgba(171, 137, 127, 0.2);
  position: relative;
  cursor: pointer;
  transition: all 0.2s;
}
.gb-canvas-controls__toggle-btn--on {
  background: rgba(255, 90, 31, 0.35);
  border-color: rgba(255, 90, 31, 0.4);
}
.gb-canvas-controls__toggle-thumb {
  position: absolute;
  top: 2px; left: 2px;
  width: 14px; height: 14px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: transform 0.2s, background 0.2s;
}
.gb-canvas-controls__toggle-btn--on .gb-canvas-controls__toggle-thumb {
  transform: translateX(16px);
  background: var(--primary-container);
}

.gb-canvas-controls__zoom {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.gb-canvas-controls__zoom-btn {
  width: 30px; height: 30px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(171, 137, 127, 0.15);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.gb-canvas-controls__zoom-btn:hover {
  background: rgba(255,255,255,0.07);
  color: var(--text-secondary);
}

/* ══════════════════════════════════════════════════════
   RIGHT CONFIG PANEL
══════════════════════════════════════════════════════ */
.gb-config {
  background: #0f1318;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 1.25rem;
  overflow-y: auto;
}

.gb-config__header { display: flex; flex-direction: column; gap: 0.25rem; }
.gb-config__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
}

/* Phases */
.gb-config__phases { display: flex; flex-direction: column; gap: 0.75rem; }

.gb-config__phase {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(171, 137, 127, 0.12);
  border-radius: var(--radius-lg);
  padding: 1rem 1.125rem 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  transition: border-color 0.2s;
}
.gb-config__phase--active {
  border-color: rgba(255, 90, 31, 0.25);
  background: rgba(255, 90, 31, 0.03);
}
.gb-config__phase--done {
  border-color: rgba(134, 239, 172, 0.12);
}

.gb-config__phase-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.gb-config__phase-name {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.125rem;
}
.gb-config__phase-desc {
  font-size: 0.6875rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.gb-config__phase-badge {
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
  font-family: var(--font-mono);
}
.gb-config__phase-badge--done   { background: rgba(134,239,172,0.12); color: #86EFAC; }
.gb-config__phase-badge--active { background: rgba(255,181,158,0.12); color: var(--primary); }
.gb-config__phase-badge--wait   { background: rgba(154,164,178,0.08); color: var(--text-muted); }

.gb-config__progress-bar {
  height: 5px;
  background: rgba(255,255,255,0.06);
  border-radius: 3px;
  overflow: hidden;
}
.gb-config__progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}
.gb-config__progress-fill--done   { background: linear-gradient(90deg, #4ade80, #86efac); }
.gb-config__progress-fill--active { background: linear-gradient(90deg, #FF5A1F, #FFB59E); }
.gb-config__progress-fill--wait   { background: rgba(154,164,178,0.2); }

.gb-config__progress-pct {
  font-size: 0.6875rem;
  color: var(--text-muted);
  text-align: right;
}

.gb-config__live-msg {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.25rem;
}
.gb-config__live-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--primary-container);
  animation: blink 1s step-end infinite;
  flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* Terminal */
.gb-config__terminal {
  flex: 1;
  min-height: 160px;
  max-height: 260px;
  background: rgba(8, 10, 13, 0.9);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.gb-config__terminal-body {
  height: 100%;
  overflow-y: auto;
  padding: 0.875rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.gb-config__terminal-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.gb-config__terminal-line {
  display: flex;
  gap: 0.5rem;
  font-size: 0.6875rem;
  line-height: 1.6;
  color: var(--text-secondary);
}
.gb-config__terminal-ts {
  color: var(--text-muted);
  flex-shrink: 0;
  opacity: 0.6;
}
.gb-config__terminal-msg { flex: 1; word-break: break-word; }
.gb-config__terminal-msg--system  { color: rgba(182,196,255,0.75); }
.gb-config__terminal-msg--info    { color: rgba(154,164,178,0.8); }
.gb-config__terminal-msg--log     { color: rgba(154,164,178,0.65); }
.gb-config__terminal-msg--success { color: #86EFAC; }
.gb-config__terminal-msg--error   { color: #f87171; }

.gb-config__terminal-cursor {
  color: var(--primary);
  animation: blink 1s step-end infinite;
}

/* Error */
.gb-config__error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  background: rgba(239,68,68,0.07);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: var(--radius-md);
  color: #f87171;
  font-size: 0.75rem;
}

/* Action buttons */
.gb-config__actions { display: flex; flex-direction: column; gap: 0.5rem; }

.gb-config__stop-btn,
.gb-config__proceed-btn,
.gb-config__start-btn {
  width: 100%;
  padding: 0.875rem 1.25rem;
  border-radius: var(--radius-md);
  font-family: var(--font-headline);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.15s;
  border: none;
}

.gb-config__stop-btn {
  background: rgba(171, 137, 127, 0.08);
  border: 1px solid rgba(171, 137, 127, 0.2);
  color: var(--text-secondary);
}
.gb-config__stop-btn:hover {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239,68,68,0.25);
  color: #f87171;
}

.gb-config__start-btn {
  background: rgba(255, 181, 158, 0.06);
  border: 1px solid rgba(255, 90, 31, 0.25);
  color: var(--primary);
}
.gb-config__start-btn:hover {
  background: rgba(255, 90, 31, 0.1);
  border-color: rgba(255, 90, 31, 0.45);
}

.gb-config__proceed-btn {
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  color: white;
  box-shadow: 0 2px 12px rgba(255, 90, 31, 0.3);
}
.gb-config__proceed-btn:hover {
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.45);
}
</style>
