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
          <!-- Graph view mode pill -->
          <span v-if="graphData" class="gb-canvas-topbar__mode-pill">
            <span class="material-symbols-outlined" style="font-size:11px">device_hub</span>
            {{ graphData.node_count }} nodes · {{ graphData.edge_count }} edges
          </span>
          <span v-else-if="entityTypes.length" class="gb-canvas-topbar__mode-pill gb-canvas-topbar__mode-pill--ontology">
            <span class="material-symbols-outlined" style="font-size:11px">schema</span>
            ONTOLOGY VIEW
          </span>
        </div>
        <div class="gb-canvas-topbar__right">
          <button class="gb-canvas-topbar__icon-btn" title="Settings">
            <span class="material-symbols-outlined" style="font-size:20px">settings</span>
          </button>
          <button class="gb-canvas-topbar__icon-btn" title="Notifications">
            <span class="material-symbols-outlined" style="font-size:20px">notifications</span>
          </button>

        </div>
      </div>

      <!-- Graph Canvas -->
      <div class="gb-canvas" ref="canvasRef" @click.self="clearSelection">
        <!-- Zoom layer — scales and pans everything except the controls bar -->
        <div
          class="gb-canvas__zoom-layer"
          :style="{
            transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})`,
            transformOrigin: 'center center',
            cursor: isPanning ? 'grabbing' : 'grab',
          }"
          @mousedown="onPanStart"
          @mousemove="onPanMove"
          @mouseup="onPanEnd"
          @mouseleave="onPanEnd"
          @click.self="clearSelection"
        >
        <!-- SVG — edges (below nodes) -->
        <svg class="gb-canvas__svg" :width="canvasW" :height="canvasH">
          <defs>
            <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="rgba(182,196,255,0.55)" />
            </marker>
            <marker id="arr-sel" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="rgba(255,90,31,0.9)" />
            </marker>
            <filter id="edge-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="2.5" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <linearGradient
              v-for="(edge, i) in graphEdges" :key="'g'+i"
              :id="'eg'+i"
              gradientUnits="userSpaceOnUse"
              :x1="edge.x1" :y1="edge.y1" :x2="edge.x2" :y2="edge.y2"
            >
              <stop offset="0%"   :stop-color="selectedEdgeIdx === i ? 'rgba(255,90,31,0.9)'  : 'rgba(255,90,31,0.5)'" />
              <stop offset="100%" :stop-color="selectedEdgeIdx === i ? 'rgba(182,196,255,0.9)' : 'rgba(182,196,255,0.35)'" />
            </linearGradient>
          </defs>

          <g
            v-for="(edge, i) in graphEdges" :key="i"
            class="gb-edge-group"
            :class="{ 'gb-edge-group--selected': selectedEdgeIdx === i }"
            @click.stop="selectEdge(edge, i)"
          >
            <!-- Wide transparent hit area -->
            <path :d="edge.path" fill="none" stroke="transparent" stroke-width="14" style="cursor:pointer" />
            <!-- Visible edge -->
            <path
              :d="edge.path"
              fill="none"
              :stroke="`url(#eg${i})`"
              :stroke-width="selectedEdgeIdx === i ? 2.5 : 1.2"
              :filter="selectedEdgeIdx === i ? 'url(#edge-glow)' : undefined"
              marker-end="url(#arr)"
              class="gb-canvas__edge"
              :class="{ 'gb-canvas__edge--animated': selectedEdgeIdx !== i, 'gb-canvas__edge--selected': selectedEdgeIdx === i }"
            />
            <!-- Edge label -->
            <text
              v-if="showEdgeLabels && edge.label"
              :x="edge.lx" :y="edge.ly - 5"
              text-anchor="middle"
              font-family="monospace"
              font-size="8"
              :fill="selectedEdgeIdx === i ? 'rgba(255,181,158,0.9)' : 'rgba(182,196,255,0.45)'"
            >{{ edge.label.slice(0, 20) }}</text>
          </g>
        </svg>

        <!-- Nodes -->
        <div
          v-for="node in graphNodes"
          :key="node.id"
          class="gb-canvas__node"
          :class="{
            'gb-canvas__node--center':    node.center,
            'gb-canvas__node--active':    highlightedNodeIds?.has(node.id) || selectedNode?.id === node.id,
            'gb-canvas__node--building':  isProcessing && node.center,
            'gb-canvas__node--hovered':   hoveredNode?.id === node.id,
          }"
          :style="{
            left: node.x + 'px',
            top:  node.y + 'px',
            '--node-color': node.color?.border || 'rgba(182,196,255,0.6)',
            '--node-bg':    node.color?.bg    || 'rgba(182,196,255,0.1)',
            '--node-glow':  node.color?.glow  || 'rgba(182,196,255,0.25)',
            '--node-text':  node.color?.text  || 'rgba(182,196,255,0.9)',
            animationDelay:    node.floatDelay    + 's',
            animationDuration: node.floatDuration + 's',
          }"
          @click.stop="selectNode(node)"
          @mouseenter="hoveredNode = node"
          @mouseleave="hoveredNode = null"
        >
          <!-- Center hub -->
          <template v-if="node.center">
            <div class="gb-node-hub">
              <span class="gb-node-hub__ring"></span>
              <span class="material-symbols-outlined gb-node-hub__icon">hub</span>
            </div>
          </template>
          <!-- Entity circle node -->
          <template v-else>
            <div class="gb-node-circle"
              :class="{
                'gb-node-circle--active':  highlightedNodeIds?.has(node.id) || selectedNode?.id === node.id,
                'gb-node-circle--hovered': hoveredNode?.id === node.id,
              }"
            >
              <div class="gb-node-circle__dot"></div>
              <div class="gb-node-circle__label font-mono">{{ node.label }}</div>
            </div>
          </template>
        </div>

        <!-- Hover Tooltip -->
        <transition name="tooltip-fade">
          <div
            v-if="hoveredNode && !hoveredNode.center"
            class="gb-canvas__tooltip"
            :style="tooltipStyle(hoveredNode)"
          >
            <div class="gb-canvas__tooltip-header">
              <span class="material-symbols-outlined" style="font-size:14px;color:var(--node-text,rgba(182,196,255,0.9))">{{ hoveredNode.icon }}</span>
              <span class="gb-canvas__tooltip-name font-mono">{{ hoveredNode.label }}</span>
            </div>
            <div class="gb-canvas__tooltip-row">
              <span class="gb-canvas__tooltip-key">Type</span>
              <span class="gb-canvas__tooltip-val">{{ hoveredNode.entityData?.type || hoveredNode.entityData?.labels?.[0] || 'entity' }}</span>
            </div>
            <!-- Real graph node: show attributes count -->
            <div v-if="hoveredNode.entityData?.attributes && Object.keys(hoveredNode.entityData.attributes).length" class="gb-canvas__tooltip-row">
              <span class="gb-canvas__tooltip-key">Attributes</span>
              <span class="gb-canvas__tooltip-val">{{ Object.keys(hoveredNode.entityData.attributes).length }}</span>
            </div>
            <!-- Ontology node: show property count -->
            <div v-else-if="hoveredNode.entityData?.properties?.length" class="gb-canvas__tooltip-row">
              <span class="gb-canvas__tooltip-key">Fields</span>
              <span class="gb-canvas__tooltip-val">{{ hoveredNode.entityData.properties.length }}</span>
            </div>
            <!-- Summary (real node) or description (ontology) -->
            <div v-if="hoveredNode.entityData?.summary || hoveredNode.entityData?.description" class="gb-canvas__tooltip-desc">
              {{ (hoveredNode.entityData.summary || hoveredNode.entityData.description || '').slice(0, 130) }}{{ (hoveredNode.entityData.summary || hoveredNode.entityData.description || '').length > 130 ? '…' : '' }}
            </div>
            <!-- Real node attributes as pills -->
            <div v-if="hoveredNode.entityData?.attributes && Object.keys(hoveredNode.entityData.attributes).length" class="gb-canvas__tooltip-props">
              <span
                v-for="[k, v] in Object.entries(hoveredNode.entityData.attributes).slice(0, 5)"
                :key="k"
                class="gb-canvas__tooltip-prop"
              >{{ k }}: {{ String(v).slice(0, 20) }}</span>
              <span v-if="Object.keys(hoveredNode.entityData.attributes).length > 5" class="gb-canvas__tooltip-prop gb-canvas__tooltip-prop--more">
                +{{ Object.keys(hoveredNode.entityData.attributes).length - 5 }} more
              </span>
            </div>
            <!-- Ontology node property pills -->
            <div v-else-if="hoveredNode.entityData?.properties?.length" class="gb-canvas__tooltip-props">
              <span
                v-for="p in hoveredNode.entityData.properties.slice(0, 5)"
                :key="typeof p === 'string' ? p : p.name"
                class="gb-canvas__tooltip-prop"
              >{{ typeof p === 'string' ? p : p.name }}</span>
              <span v-if="hoveredNode.entityData.properties.length > 5" class="gb-canvas__tooltip-prop gb-canvas__tooltip-prop--more">
                +{{ hoveredNode.entityData.properties.length - 5 }} more
              </span>
            </div>
          </div>
        </transition>

        <!-- Idle / empty state -->
        <div v-if="currentPhase === 1 && !isProcessing && entityTypes.length === 0" class="gb-canvas__empty">
          <span class="material-symbols-outlined" style="font-size:32px;color:rgba(182,196,255,0.2)">hub</span>
          <p class="font-mono" style="font-size:0.6875rem;color:rgba(182,196,255,0.2);margin-top:0.5rem">
            Click "Build Graph" to start
          </p>
        </div>
        </div><!-- end gb-canvas__zoom-layer -->

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
            <button class="gb-canvas-controls__zoom-btn" @click="resetView">
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

        <!-- Mode Toggle -->
        <div class="gb-config__mode-toggle">
          <button
            class="gb-config__mode-btn"
            :class="{ 'gb-config__mode-btn--active': !autoMode }"
            @click="autoMode = false"
          >
            <span class="material-symbols-outlined" style="font-size:13px">tune</span>
            Manual
          </button>
          <button
            class="gb-config__mode-btn"
            :class="{ 'gb-config__mode-btn--active': autoMode }"
            @click="autoMode = true"
          >
            <span class="material-symbols-outlined" style="font-size:13px">auto_mode</span>
            Auto
          </button>
        </div>

        <!-- Auto mode info -->
        <div v-if="autoMode" class="gb-config__auto-info">
          <span class="material-symbols-outlined" style="font-size:13px;color:var(--primary);flex-shrink:0">info</span>
          <span style="font-size:0.6875rem;color:var(--text-muted);line-height:1.5">All steps will run automatically and navigate to the report when complete.</span>
        </div>

        <!-- Top action button -->
        <button
          v-if="isProcessing"
          class="gb-config__stop-btn gb-config__stop-btn--top"
          @click="stopBuild"
        >
          STOP BUILD ENGINE
          <span class="material-symbols-outlined" style="font-size:16px">close</span>
        </button>
        <button
          v-else-if="currentPhase === 2"
          class="gb-config__proceed-btn gb-config__proceed-btn--top"
          @click="proceedToEnv"
        >
          PROCEED TO ENV SETUP
          <span class="material-symbols-outlined" style="font-size:16px">arrow_forward</span>
        </button>
        <button
          v-else-if="!isProcessing && currentPhase === 1"
          class="gb-config__start-btn gb-config__start-btn--top"
          @click="startBuild"
        >
          START BUILD ENGINE
          <span class="material-symbols-outlined" style="font-size:16px">bolt</span>
        </button>
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

      <!-- Stop / Proceed buttons (duplicate at bottom for convenience) -->
      <div class="gb-config__actions">
        <div v-if="!autoMode && !isProcessing && currentPhase === 1" class="gb-config__scroll-hint">
          <span class="material-symbols-outlined" style="font-size:14px;color:var(--primary)">keyboard_double_arrow_up</span>
          <span style="font-size:0.6875rem;color:var(--text-muted)">Button also available at the top of this panel</span>
        </div>
      </div>
    </aside>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'

const props = defineProps({ projectData: Object })
const emit = defineEmits(['completed'])

// ── State ──────────────────────────────────────────────────────────────────
const autoMode = ref(false)
const currentPhase = ref(1)   // 1 = ready to build, 2 = build complete
const builtGraphId = ref(null) // stores the real graph_id returned by the backend
const isProcessing = ref(false)
const phaseError = ref('')
const statusMsg = ref('')
const logLines = ref([])
const selectedNode = ref(null)
const hoveredNode = ref(null)
const selectedEdgeIdx = ref(null)   // index into graphEdges array, or null
const showEdgeLabels = ref(false)
const graphData = ref(null)  // real graph data: { nodes: [], edges: [] }
const zoomLevel = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const panStart = ref({ x: 0, y: 0 })
const canvasRef = ref(null)
const terminalRef = ref(null)

// ── Node color palette ──────────────────────────────────────────────────────
const NODE_COLORS = [
  { bg: 'rgba(59,130,246,0.12)',  border: 'rgba(59,130,246,0.55)',  text: '#93c5fd', glow: 'rgba(59,130,246,0.3)' },
  { bg: 'rgba(168,85,247,0.12)', border: 'rgba(168,85,247,0.55)', text: '#d8b4fe', glow: 'rgba(168,85,247,0.3)' },
  { bg: 'rgba(236,72,153,0.12)', border: 'rgba(236,72,153,0.55)', text: '#f9a8d4', glow: 'rgba(236,72,153,0.3)' },
  { bg: 'rgba(16,185,129,0.12)', border: 'rgba(16,185,129,0.55)', text: '#6ee7b7', glow: 'rgba(16,185,129,0.3)' },
  { bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.55)', text: '#fcd34d', glow: 'rgba(245,158,11,0.3)' },
  { bg: 'rgba(239,68,68,0.12)',  border: 'rgba(239,68,68,0.55)',  text: '#fca5a5', glow: 'rgba(239,68,68,0.3)' },
  { bg: 'rgba(20,184,166,0.12)', border: 'rgba(20,184,166,0.55)', text: '#5eead4', glow: 'rgba(20,184,166,0.3)' },
  { bg: 'rgba(234,179,8,0.12)',  border: 'rgba(234,179,8,0.55)',  text: '#fde047', glow: 'rgba(234,179,8,0.3)' },
]

// ── Icon map by common entity type keywords ─────────────────────────────────
function entityIcon(name = '') {
  const n = name.toLowerCase()
  if (n.includes('user') || n.includes('person') || n.includes('customer')) return 'person'
  if (n.includes('product') || n.includes('item') || n.includes('good')) return 'inventory_2'
  if (n.includes('order') || n.includes('transaction') || n.includes('purchase')) return 'receipt_long'
  if (n.includes('company') || n.includes('org') || n.includes('vendor')) return 'business'
  if (n.includes('event') || n.includes('activity')) return 'event'
  if (n.includes('location') || n.includes('address') || n.includes('place')) return 'location_on'
  if (n.includes('category') || n.includes('tag') || n.includes('label')) return 'label'
  if (n.includes('review') || n.includes('rating') || n.includes('feedback')) return 'star'
  if (n.includes('payment') || n.includes('invoice') || n.includes('bill')) return 'payments'
  if (n.includes('message') || n.includes('chat') || n.includes('comment')) return 'chat'
  return 'account_circle'
}

// ── Tooltip position ─────────────────────────────────────────────────────────
function tooltipStyle(node) {
  if (!node) return {}
  const cx = canvasW.value / 2
  const left = node.x > cx ? node.x - 220 : node.x + 10
  return { left: left + 'px', top: (node.y - 60) + 'px' }
}

// Build phase progress (animated)
const graphRagStatus = ref('wait')   // wait | active | done
const graphRagPct = ref(0)
const finalizationStatus = ref('wait')
const finalizationPct = ref(0)

// ── Project info ────────────────────────────────────────────────────────────
const projectTitle = computed(() => {
  const files = props.projectData?.files
  const fname = files?.[0]?.filename || files?.[0]?.name
  if (fname) return fname.replace(/\.[^.]+$/, '').replace(/[-_]/g, ' ')
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

// IDs of nodes connected to the currently selected edge
const highlightedNodeIds = computed(() => {
  if (selectedEdgeIdx.value === null) return null
  const edge = graphEdges.value[selectedEdgeIdx.value]
  if (!edge) return null
  return new Set([edge.sourceId, edge.targetId].filter(Boolean))
})

// ── Layout helpers ───────────────────────────────────────────────────────────
function makeCurvedEdge(x1, y1, x2, y2, label = '', dashed = false) {
  const dx = x2 - x1, dy = y2 - y1
  const dist = Math.sqrt(dx*dx + dy*dy) || 1
  const s = 24 / dist, e = 24 / dist   // 24px offset = just outside a 20px circle + 4px padding
  const sx = x1 + dx*s,   sy = y1 + dy*s
  const ex = x2 - dx*e,   ey = y2 - dy*e
  const mx = (sx+ex)/2 + dy*0.1, my = (sy+ey)/2 - dx*0.1
  return {
    path: `M ${sx} ${sy} Q ${mx} ${my} ${ex} ${ey}`,
    x1: sx, y1: sy, x2: ex, y2: ey,
    lx: (sx+ex)/2, ly: (sy+ey)/2,
    angle: Math.atan2(ey-sy, ex-sx) * 180 / Math.PI,
    label, dashed,
  }
}

// Deterministic seeded PRNG (LCG) — so layout doesn't jump on re-renders
function seededRandom(seed) {
  let s = 0
  for (let i = 0; i < seed.length; i++) s = Math.imul(s * 31 + seed.charCodeAt(i), 1) | 0
  return () => {
    s = (Math.imul(1664525, s) + 1013904223) | 0
    return ((s >>> 0) / 4294967296)
  }
}

/**
 * Force-directed layout (synchronous, fixed iterations).
 * nodeIds  — array of string IDs (no hub/center)
 * edgePairs — [[sourceId, targetId], ...]
 * Returns { [id]: { x, y } }
 */
function runForceLayout(nodeIds, edgePairs, w, h) {
  const cx = w / 2, cy = h / 2
  const n = nodeIds.length
  if (n === 0) return {}
  const rng = seededRandom(nodeIds.join('|'))

  // Initial positions: loose ring with jitter so force has room to act
  const pos = {}, vel = {}
  nodeIds.forEach((id, i) => {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2
    const r0 = Math.min(w, h) * 0.28
    pos[id] = {
      x: cx + r0 * Math.cos(angle) + (rng() - 0.5) * 90,
      y: cy + r0 * Math.sin(angle) + (rng() - 0.5) * 90,
    }
    vel[id] = { x: 0, y: 0 }
  })

  // Build a degree map so high-degree nodes get slightly more repulsion budget
  const degree = {}
  nodeIds.forEach(id => { degree[id] = 0 })
  edgePairs.forEach(([a, b]) => {
    if (degree[a] !== undefined) degree[a]++
    if (degree[b] !== undefined) degree[b]++
  })

  const ITERATIONS   = 280
  const REPULSION    = 6500        // node-node repulsion strength
  const LINK_DIST    = 140         // ideal spring length
  const LINK_K       = 0.055       // spring constant
  const CENTER_K     = 0.010       // weak gravity toward center
  const DAMPING      = 0.82
  const PADDING      = 55          // min distance from canvas edge
  const BOTTOM_PAD   = 80          // extra room for controls bar

  for (let iter = 0; iter < ITERATIONS; iter++) {
    const alpha = Math.pow(0.985, iter)   // cooling schedule

    // ── Repulsion (O(n²), fine for n ≤ 40) ──────────────────────────────────
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const a = nodeIds[i], b = nodeIds[j]
        let dx = pos[b].x - pos[a].x
        let dy = pos[b].y - pos[a].y
        let dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 1) { dx = rng() - 0.5; dy = rng() - 0.5; dist = 0.5 }
        const rep = REPULSION / (dist * dist)
        const ux = dx / dist, uy = dy / dist
        vel[a].x -= ux * rep;  vel[a].y -= uy * rep
        vel[b].x += ux * rep;  vel[b].y += uy * rep
      }
    }

    // ── Link springs ─────────────────────────────────────────────────────────
    edgePairs.forEach(([sid, tid]) => {
      if (!pos[sid] || !pos[tid]) return
      const dx = pos[tid].x - pos[sid].x
      const dy = pos[tid].y - pos[sid].y
      const dist = Math.sqrt(dx * dx + dy * dy) || 1
      const spring = (dist - LINK_DIST) * LINK_K
      const ux = dx / dist, uy = dy / dist
      vel[sid].x += ux * spring;  vel[sid].y += uy * spring
      vel[tid].x -= ux * spring;  vel[tid].y -= uy * spring
    })

    // ── Center gravity ───────────────────────────────────────────────────────
    nodeIds.forEach(id => {
      vel[id].x += (cx - pos[id].x) * CENTER_K
      vel[id].y += (cy - pos[id].y) * CENTER_K
    })

    // ── Integrate ────────────────────────────────────────────────────────────
    nodeIds.forEach(id => {
      pos[id].x += vel[id].x * alpha
      pos[id].y += vel[id].y * alpha
      vel[id].x *= DAMPING
      vel[id].y *= DAMPING
      pos[id].x = Math.max(PADDING, Math.min(w - PADDING, pos[id].x))
      pos[id].y = Math.max(PADDING, Math.min(h - BOTTOM_PAD, pos[id].y))
    })
  }

  return pos
}

// ── Build type→color map from real nodes or ontology ────────────────────────
const typeColorMap = computed(() => {
  const map = {}
  let idx = 0
  const assign = t => { if (t && !(t in map)) map[t] = NODE_COLORS[idx++ % NODE_COLORS.length] }
  if (graphData.value?.nodes?.length) {
    graphData.value.nodes.forEach(n => assign(n.labels?.[0] || 'Entity'))
  } else {
    entityTypes.value.forEach((e, i) => assign(e.name || `entity-${i}`))
  }
  return map
})

// ── graphNodes ───────────────────────────────────────────────────────────────
const graphNodes = computed(() => {
  const cx = CX.value, cy = CY.value
  const w  = canvasW.value, h = canvasH.value
  const hub = { id: 'center', x: cx, y: cy, center: true, label: 'GRAPH CORE', icon: 'hub', color: null, entityData: null, floatDelay: 0, floatDuration: 3 }

  // ── Mode A: real graph data available ──────────────────────────────────────
  const realNodes = graphData.value?.nodes
  if (realNodes?.length) {
    const MAX = 40
    const sorted = [...realNodes]
      .sort((a, b) => (a.labels?.[0] || '').localeCompare(b.labels?.[0] || ''))
      .slice(0, MAX)

    // Extract edge pairs restricted to the visible node set
    const nodeSet = new Set(sorted.map(n => n.uuid))
    const edgePairs = (graphData.value.edges || [])
      .filter(e => nodeSet.has(e.source_node_uuid) && nodeSet.has(e.target_node_uuid))
      .map(e => [e.source_node_uuid, e.target_node_uuid])

    // Run force-directed layout (synchronous, deterministic)
    const positions = runForceLayout(sorted.map(n => n.uuid), edgePairs, w, h)

    const nodes = [hub]
    sorted.forEach((n, i) => {
      const pos  = positions[n.uuid] ?? { x: cx, y: cy }
      const type = n.labels?.[0] || 'Entity'
      nodes.push({
        id: n.uuid,
        x: pos.x, y: pos.y,
        center: false,
        label: (n.name || n.uuid.slice(0, 10)).slice(0, 20),
        icon: entityIcon(n.labels?.[0] || n.name || ''),
        color: typeColorMap.value[type] || NODE_COLORS[0],
        entityData: { ...n, type },
        floatDelay: -(i * 0.28),
        floatDuration: 2.6 + (i % 5) * 0.28,
      })
    })
    return nodes
  }

  // ── Mode B: ontology entity types ─────────────────────────────────────────
  const entities = entityTypes.value
  if (!entities.length) return [hub]

  const MAX = 12
  const items = entities.slice(0, MAX)
  const ids   = items.map((e, i) => e.name || `entity-${i}`)

  // Derive edge pairs from ontology edge_types
  const idxByName = {}
  items.forEach((e, i) => { idxByName[e.name || `entity-${i}`] = ids[i] })
  const edgePairs = (props.projectData?.ontology?.edge_types ?? [])
    .map(et => {
      const s = idxByName[et.source] || idxByName[et.from]
      const t = idxByName[et.target] || idxByName[et.to]
      return s && t ? [s, t] : null
    })
    .filter(Boolean)

  const positions = runForceLayout(ids, edgePairs, w, h)

  const nodes = [hub]
  items.forEach((e, i) => {
    const id  = ids[i]
    const pos = positions[id] ?? { x: cx, y: cy }
    const type = e.name || `Entity ${i+1}`
    nodes.push({
      id,
      x: pos.x, y: pos.y,
      center: false,
      label: e.name || `Entity ${i+1}`,
      icon: entityIcon(e.name || ''),
      color: typeColorMap.value[type] || NODE_COLORS[i % NODE_COLORS.length],
      entityData: e,
      floatDelay: -(i * 0.4),
      floatDuration: 2.8 + (i % 4) * 0.35,
    })
  })
  return nodes
})

// ── graphEdges ───────────────────────────────────────────────────────────────
const graphEdges = computed(() => {
  const nodes  = graphNodes.value
  const center = nodes.find(n => n.center)
  if (!center) return []

  // Build id→position map
  const posById = {}
  nodes.forEach(n => { posById[n.id] = n })

  const edges = []

  // ── Mode A: real graph edges ───────────────────────────────────────────────
  const realEdges = graphData.value?.edges
  if (realEdges?.length) {
    const MAX_EDGES = 60
    realEdges.slice(0, MAX_EDGES).forEach(e => {
      const from = posById[e.source_node_uuid]
      const to   = posById[e.target_node_uuid]
      if (!from || !to || from.id === to.id) return
      edges.push({
        ...makeCurvedEdge(from.x, from.y, to.x, to.y, e.fact_type || e.name || ''),
        sourceId: from.id, targetId: to.id,
      })
    })
    return edges
  }

  // ── Mode B: ontology edge_types between entity type nodes ─────────────────
  const edgeTypes = props.projectData?.ontology?.edge_types ?? []
  const byLabel = {}
  nodes.forEach(n => { if (!n.center) byLabel[n.label] = n })

  let drawn = 0
  edgeTypes.forEach(et => {
    const from = byLabel[et.source] || byLabel[et.from]
    const to   = byLabel[et.target] || byLabel[et.to]
    if (from && to && from.id !== to.id) {
      edges.push({
        ...makeCurvedEdge(from.x, from.y, to.x, to.y, et.name || et.type || ''),
        sourceId: from.id, targetId: to.id,
      })
      drawn++
    }
  })

  // Fall back to hub spokes if no ontology edges matched
  if (drawn === 0) {
    nodes.filter(n => !n.center).forEach(n => {
      edges.push({
        ...makeCurvedEdge(center.x, center.y, n.x, n.y, n.entityData?.type || ''),
        sourceId: center.id, targetId: n.id,
      })
    })
  }

  return edges
})

// ── Fetch real graph data from backend ───────────────────────────────────────
async function fetchGraphData(graphId) {
  if (!graphId) return
  try {
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'
    const res  = await fetch(`${BASE_URL}/graph/data/${graphId}`)
    const json = await res.json()
    if (json.success && json.data?.nodes?.length) {
      graphData.value = json.data
      addLog(`Graph loaded — ${json.data.node_count} nodes, ${json.data.edge_count} edges.`, 'success')
    }
  } catch (e) {
    console.warn('Could not fetch graph data:', e.message)
  }
}

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
  selectedEdgeIdx.value = null
  selectedNode.value = selectedNode.value?.id === node.id ? null : node
}

function selectEdge(edge, index) {
  selectedNode.value = null
  selectedEdgeIdx.value = selectedEdgeIdx.value === index ? null : index
}

function clearSelection() {
  selectedNode.value = null
  selectedEdgeIdx.value = null
}

function zoom(delta) {
  zoomLevel.value = Math.max(0.5, Math.min(3, zoomLevel.value + delta))
}

function resetView() {
  zoomLevel.value = 1
  panX.value = 0
  panY.value = 0
}

function onPanStart(e) {
  // Only start panning on left-click directly on the zoom layer (not on nodes/edges)
  if (e.button !== 0) return
  isPanning.value = true
  panStart.value = { x: e.clientX - panX.value, y: e.clientY - panY.value }
  e.currentTarget.style.cursor = 'grabbing'
}

function onPanMove(e) {
  if (!isPanning.value) return
  panX.value = e.clientX - panStart.value.x
  panY.value = e.clientY - panStart.value.y
}

function onPanEnd(e) {
  isPanning.value = false
  e.currentTarget.style.cursor = 'grab'
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
    const graphId    = result?.graph_id   || result?.result?.graph_id    || null
    builtGraphId.value = graphId
    const nodeCount  = result?.node_count ?? result?.result?.node_count  ?? '—'
    const edgeCount  = result?.edge_count ?? result?.result?.edge_count  ?? '—'

    addLog(`Graph anchored — ${nodeCount} nodes, ${edgeCount} edges.`, 'success')
    currentPhase.value = 2

    // Fetch the actual graph nodes + edges to populate the canvas
    if (graphId) {
      addLog('Loading graph topology from store...', 'system')
      await fetchGraphData(graphId)
    }

    // Auto mode: proceed automatically to next step
    if (autoMode.value) {
      addLog('Auto mode: proceeding to Env Setup...', 'system')
      await new Promise(r => setTimeout(r, 1200))
      proceedToEnv()
    }

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
    graph_id: builtGraphId.value,
    ontology: props.projectData?.ontology ?? { entity_types: [], edge_types: [] },
    autoMode: autoMode.value,
  })
}

onMounted(() => {
  nextTick(async () => {
    // Sync canvas size to container
    if (canvasRef.value) {
      canvasW.value = canvasRef.value.clientWidth || 600
      canvasH.value = canvasRef.value.clientHeight || 500
    }
    // If project already has a built graph, load it immediately
    const existingGraphId = props.projectData?.graph_id
    if (existingGraphId) {
      currentPhase.value = 2
      await fetchGraphData(existingGraphId)
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

.gb-canvas-topbar__mode-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  font-family: var(--font-mono);
  background: rgba(59,130,246,0.1);
  color: #93c5fd;
  border: 1px solid rgba(59,130,246,0.2);
}
.gb-canvas-topbar__mode-pill--ontology {
  background: rgba(168,85,247,0.1);
  color: #d8b4fe;
  border-color: rgba(168,85,247,0.2);
}

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

.gb-canvas__zoom-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  will-change: transform;
  user-select: none;
}

.gb-canvas__svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  /* pointer-events enabled so edges are clickable */
  z-index: 1;
}

/* Edge — default subtle, animated dash, selected = bright solid */
.gb-canvas__edge {
  opacity: 0.55;
  transition: opacity 0.2s, stroke-width 0.2s;
}
.gb-canvas__edge--animated {
  stroke-dasharray: 5 9;
  animation: edge-flow 2.5s linear infinite;
}
@keyframes edge-flow {
  from { stroke-dashoffset: 28; }
  to   { stroke-dashoffset: 0; }
}
.gb-canvas__edge--selected {
  opacity: 1;
  stroke-dasharray: none;
  animation: none;
}

/* ── Floating node container ── */
.gb-canvas__node {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 2;
  animation-name: node-float;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  animation-duration: 3s;
  animation-delay: 0s;
}
@keyframes node-float {
  0%,100% { transform: translate(-50%, -50%) translateY(0px); }
  50%      { transform: translate(-50%, -50%) translateY(-6px); }
}

/* ── Center hub ── */
.gb-node-hub {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,90,31,0.2) 0%, rgba(255,90,31,0.04) 70%);
  border: 1.5px solid rgba(255,90,31,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 18px rgba(255,90,31,0.25);
  transition: all 0.2s;
}
.gb-canvas__node--building .gb-node-hub {
  animation: hub-pulse 1.4s ease-in-out infinite;
}
@keyframes hub-pulse {
  0%,100% { box-shadow: 0 0 16px rgba(255,90,31,0.3); }
  50%      { box-shadow: 0 0 36px rgba(255,90,31,0.7), 0 0 60px rgba(255,90,31,0.2); }
}
.gb-canvas__node--hovered .gb-node-hub { border-color: rgba(255,90,31,0.9); }
.gb-node-hub__ring {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  border: 1px solid rgba(255,181,158,0.18);
  animation: ring-expand 2.4s ease-out infinite;
  pointer-events: none;
}
@keyframes ring-expand {
  0%   { transform: scale(0.85); opacity: 0.6; }
  100% { transform: scale(1.3);  opacity: 0; }
}
.gb-node-hub__icon {
  font-size: 18px;
  color: var(--primary);
}

/* ── Circle entity node ── */
.gb-node-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  transition: transform 0.2s;
}
.gb-node-circle__dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--node-bg, rgba(182,196,255,0.12));
  border: 2px solid var(--node-color, rgba(182,196,255,0.55));
  box-shadow: 0 0 8px var(--node-glow, rgba(182,196,255,0.2));
  transition: all 0.2s ease;
  position: relative;
}
.gb-node-circle__dot::after {
  content: '';
  position: absolute;
  inset: 3px;
  border-radius: 50%;
  background: var(--node-color, rgba(182,196,255,0.3));
  opacity: 0.5;
}
.gb-node-circle__label {
  font-size: 0.475rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: var(--node-text, rgba(182,196,255,0.75));
  white-space: nowrap;
  max-width: 64px;
  overflow: hidden;
  text-overflow: ellipsis;
  text-transform: uppercase;
  text-align: center;
  line-height: 1;
  pointer-events: none;
}

/* Hovered circle */
.gb-node-circle--hovered .gb-node-circle__dot,
.gb-canvas__node--hovered .gb-node-circle__dot {
  width: 24px;
  height: 24px;
  border-color: var(--node-color, rgba(182,196,255,0.9));
  box-shadow: 0 0 16px var(--node-glow, rgba(182,196,255,0.5));
  background: var(--node-color, rgba(182,196,255,0.25));
}
.gb-node-circle--hovered .gb-node-circle__label,
.gb-canvas__node--hovered .gb-node-circle__label {
  color: var(--node-text, rgba(182,196,255,1));
}

/* Active / edge-highlighted circle */
.gb-node-circle--active .gb-node-circle__dot,
.gb-canvas__node--active .gb-node-circle__dot {
  width: 26px;
  height: 26px;
  border-color: var(--node-color);
  background: var(--node-color);
  box-shadow:
    0 0 0 4px rgba(0,0,0,0.3),
    0 0 20px var(--node-glow),
    0 0 40px var(--node-glow);
  opacity: 1;
}
.gb-node-circle--active .gb-node-circle__dot::after,
.gb-canvas__node--active .gb-node-circle__dot::after {
  display: none;
}
.gb-canvas__node--active .gb-node-circle__label {
  color: var(--node-text);
  font-weight: 800;
}

/* Edge group */
.gb-edge-group { cursor: pointer; }
.gb-canvas__edge--selected {
  opacity: 1 !important;
  stroke-dasharray: none !important;
  animation: none !important;
}

/* ── Hover Tooltip ── */
.gb-canvas__tooltip {
  position: absolute;
  z-index: 10;
  width: 190px;
  background: rgba(10, 13, 18, 0.95);
  border: 1px solid rgba(171,137,127,0.2);
  border-radius: 10px;
  padding: 0.75rem 0.875rem;
  pointer-events: none;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.gb-canvas__tooltip-header {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(171,137,127,0.12);
}
.gb-canvas__tooltip-name {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-primary);
  text-transform: uppercase;
}
.gb-canvas__tooltip-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}
.gb-canvas__tooltip-key {
  font-size: 0.6rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  font-family: var(--font-mono);
}
.gb-canvas__tooltip-val {
  font-size: 0.6rem;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  text-transform: uppercase;
}
.gb-canvas__tooltip-desc {
  font-size: 0.6rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-top: 0.375rem;
  padding-top: 0.375rem;
  border-top: 1px solid rgba(171,137,127,0.08);
}
.gb-canvas__tooltip-props {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
}
.gb-canvas__tooltip-prop {
  font-size: 0.525rem;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  background: rgba(182,196,255,0.07);
  border: 1px solid rgba(182,196,255,0.12);
  color: rgba(182,196,255,0.7);
  font-family: var(--font-mono);
  letter-spacing: 0.04em;
}
.gb-canvas__tooltip-prop--more {
  color: var(--text-muted);
  background: transparent;
  border-color: transparent;
  font-style: italic;
}

/* Tooltip transition */
.tooltip-fade-enter-active,
.tooltip-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.tooltip-fade-enter-from,
.tooltip-fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
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
  z-index: 5;
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

.gb-config__header { display: flex; flex-direction: column; gap: 0.75rem; }
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

/* Mode toggle */
.gb-config__mode-toggle {
  display: flex;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(171,137,127,0.15);
  border-radius: var(--radius-md);
  padding: 3px;
  gap: 3px;
}
.gb-config__mode-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.45rem 0.75rem;
  border-radius: calc(var(--radius-md) - 2px);
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-family: var(--font-headline);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: all 0.18s;
}
.gb-config__mode-btn--active {
  background: rgba(255, 90, 31, 0.15);
  color: var(--primary);
  border: 1px solid rgba(255, 90, 31, 0.25);
}
.gb-config__mode-btn:hover:not(.gb-config__mode-btn--active) {
  color: var(--text-secondary);
  background: rgba(255,255,255,0.04);
}

/* Auto info strip */
.gb-config__auto-info {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.625rem 0.75rem;
  background: rgba(255, 90, 31, 0.04);
  border: 1px solid rgba(255, 90, 31, 0.12);
  border-radius: var(--radius-md);
}

/* Top button variants (same styles, just positioned inside header) */
.gb-config__stop-btn--top,
.gb-config__proceed-btn--top,
.gb-config__start-btn--top {
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
.gb-config__stop-btn--top {
  background: rgba(171, 137, 127, 0.08);
  border: 1px solid rgba(171, 137, 127, 0.2);
  color: var(--text-secondary);
}
.gb-config__stop-btn--top:hover {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239,68,68,0.25);
  color: #f87171;
}
.gb-config__start-btn--top {
  background: rgba(255, 181, 158, 0.06);
  border: 1px solid rgba(255, 90, 31, 0.25);
  color: var(--primary);
}
.gb-config__start-btn--top:hover {
  background: rgba(255, 90, 31, 0.1);
  border-color: rgba(255, 90, 31, 0.45);
}
.gb-config__proceed-btn--top {
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  color: white;
  box-shadow: 0 2px 12px rgba(255, 90, 31, 0.3);
}
.gb-config__proceed-btn--top:hover {
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.45);
}

/* Mode toggle */

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

.gb-config__scroll-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  background: rgba(255, 90, 31, 0.04);
  border: 1px dashed rgba(255, 90, 31, 0.2);
  border-radius: var(--radius-md);
}
</style>