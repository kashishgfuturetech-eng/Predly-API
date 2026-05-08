<template>
  <div class="env-setup">
    <!-- Auto-mode banner -->
    <div v-if="autoMode" class="env-setup__auto-banner">
      <span class="env-setup__auto-dot"></span>
      <span><strong style="color:var(--primary)">Auto Mode Active</strong> — All steps are running automatically. No action needed.</span>
    </div>

    <!-- Quick Stats -->
    <div class="env-setup__stats">
      <div class="env-setup__stat card" v-for="s in quickStats" :key="s.label">
        <div class="orb" :class="s.orb" style="width:70px;height:70px;top:-15px;right:-15px;opacity:0.4;"></div>
        <span class="label-sm" style="color:var(--text-muted)">{{ s.label }}</span>
        <div class="env-setup__stat-val font-headline">{{ s.value }}</div>
        <div class="env-setup__stat-sub">{{ s.sub }}</div>
      </div>
    </div>

    <!-- ── Phase 01: Simulation Instance ── -->
    <div ref="envPhaseRef0" class="env-setup__phase card" :class="phaseClass(0)">
      <div class="env-setup__phase-header">
        <span class="chip chip-blue label-sm">POST /api/simulation/create</span>
        <div class="env-setup__phase-title-row">
          <span class="env-setup__phase-num font-mono">01</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Simulation Instance Initialization</h2>
          <div class="env-setup__phase-badge">
            <span v-if="phase > 0" class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
            </span>
            <div v-else-if="phase === 0 && isProcessing" class="ai-chip">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">{{ statusMsg || 'Initializing…' }}</span>
            </div>
            <span v-else class="chip chip-muted">Initialization</span>
          </div>
        </div>
        <p class="env-setup__phase-desc">Create new simulation instance and fetch simulated world parameter template.</p>
      </div>

      <div v-if="simulationId" class="env-setup__info-card card-nested">
        <div class="env-setup__info-row" v-for="row in instanceInfo" :key="row.label">
          <span class="env-setup__info-label label-sm">{{ row.label }}</span>
          <span class="env-setup__info-val font-mono">{{ row.value }}</span>
          <button v-if="row.copyable" class="btn-ghost" style="padding:.125rem .25rem" @click="copy(row.value)" :title="'Copy ' + row.label">
            <span class="material-symbols-outlined" style="font-size:14px">content_copy</span>
          </button>
        </div>
      </div>

      <div v-if="phaseError[0]" class="env-setup__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError[0] }}
      </div>

      <div v-if="phase === 0 && !isProcessing" class="env-setup__cta" ref="phase0Ref">
        <button class="btn-primary" @click="initSimulation">
          <span class="material-symbols-outlined" style="font-size:18px">play_circle</span>
          Initialize Instance
        </button>
      </div>
    </div>

    <!-- ── Phase 02: Entity Preview ── -->
    <div ref="envPhaseRef1" class="env-setup__phase card" :class="phaseClass(1)">
      <div class="env-setup__phase-header">
        <span class="chip chip-blue label-sm">GET /api/simulation/entities/:graph_id</span>
        <div class="env-setup__phase-title-row">
          <span class="env-setup__phase-num font-mono">02</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Graph Entity Preview</h2>
          <div class="env-setup__phase-badge">
            <span v-if="phase > 1" class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
            </span>
            <div v-else-if="phase === 1 && isProcessing" class="ai-chip">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">{{ statusMsg || 'Scanning graph…' }}</span>
            </div>
            <span v-else class="chip chip-muted">Waiting</span>
          </div>
        </div>
        <p class="env-setup__phase-desc">
          Scan the knowledge graph to discover available entities. Review what's in the graph
          before deciding how many agents to generate.
        </p>
      </div>

      <div v-if="entityPreview.length > 0" class="env-setup__entity-preview">
        <div class="env-setup__entity-summary card-nested">
          <div class="env-setup__entity-total">
            <span class="env-setup__stat-val font-headline" style="font-size:2rem">{{ totalEntities }}</span>
            <span class="label-sm" style="color:var(--text-muted)">Total entities available in graph</span>
          </div>
          <div class="env-setup__entity-types">
            <div v-for="t in entityPreview" :key="t.type" class="env-setup__entity-type-chip">
              <span class="material-symbols-outlined" style="font-size:14px">person</span>
              <span class="env-setup__entity-type-name">{{ t.type }}</span>
              <span class="env-setup__entity-type-count chip chip-blue" style="font-size:.6rem">{{ t.count }}</span>
            </div>
          </div>
        </div>

        <div class="env-setup__preview-note">
          <span class="material-symbols-outlined" style="font-size:15px;color:var(--primary)">info</span>
          <span class="label-sm" style="color:var(--text-muted)">
            You'll set how many of these become simulation agents in the next step.
            Each agent gets a unique LLM-generated persona based on its graph data.
          </span>
        </div>
      </div>

      <div v-if="phaseError[1]" class="env-setup__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError[1] }}
      </div>

      <div v-if="phase === 1 && !isProcessing" class="env-setup__cta" ref="phase1Ref">
        <button class="btn-primary" @click="previewEntities">
          <span class="material-symbols-outlined" style="font-size:18px">hub</span>
          Scan Graph Entities
        </button>
      </div>
    </div>

    <!-- ── Phase 03: Configure + Generate ── -->
    <div ref="envPhaseRef2" class="env-setup__phase card" :class="phaseClass(2)">
      <div class="env-setup__phase-header">
        <span class="chip chip-blue label-sm">POST /api/simulation/configure → /prepare</span>
        <div class="env-setup__phase-title-row">
          <span class="env-setup__phase-num font-mono">03</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Configure & Generate Agents</h2>
          <div class="env-setup__phase-badge">
            <span v-if="phase > 2" class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
            </span>
            <span v-else class="chip chip-muted">{{ phase < 2 ? 'Waiting' : 'Configure' }}</span>
          </div>
        </div>
        <p class="env-setup__phase-desc">
          Set simulation parameters, then generate agent personas. Agent count is capped at
          <strong style="color:var(--text-primary)">{{ totalEntities || '—' }}</strong> available graph entities.
        </p>
      </div>

      <div v-if="phase >= 2">
        <!-- Agent Count — highlighted as the key decision -->
        <div class="env-setup__agent-count-row card-nested">
          <div class="env-setup__agent-count-label">
            <span class="material-symbols-outlined" style="font-size:18px;color:var(--primary)">group</span>
            <div>
              <div style="font-weight:700;font-size:.9rem;color:var(--text-primary)">Agent Count</div>
              <div class="label-sm" style="color:var(--text-muted)">How many graph entities become simulation agents</div>
            </div>
          </div>
          <div class="env-setup__agent-count-ctrl">
            <button class="env-setup__count-btn" @click="adjustAgentCount(-1)" :disabled="parseInt(simConfig.agentCount) <= 1">−</button>
            <input
              v-model="simConfig.agentCount"
              type="number"
              class="input-field env-setup__count-input"
              :max="totalEntities || 9999"
              min="1"
              @change="clampAgentCount"
            />
            <button class="env-setup__count-btn" @click="adjustAgentCount(1)" :disabled="parseInt(simConfig.agentCount) >= totalEntities">+</button>
            <span class="label-sm" style="color:var(--text-muted);white-space:nowrap">of {{ totalEntities }} available</span>
          </div>
        </div>

        <!-- Other config fields -->
        <div class="env-setup__config-grid">
          <div class="env-setup__config-field" v-for="field in configFields" :key="field.key">
            <label class="env-setup__config-label label-sm">{{ field.label }}</label>
            <input
              v-if="field.type === 'text' || field.type === 'number'"
              v-model="simConfig[field.key]"
              class="input-field env-setup__config-input"
              :type="field.type"
              :placeholder="field.placeholder"
            />
            <select
              v-else-if="field.type === 'select'"
              v-model="simConfig[field.key]"
              class="input-field env-setup__config-input"
            >
              <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
        </div>

        <!-- Recommendation Algorithms -->
        <div class="env-setup__rec-section">
          <span class="label-sm" style="color:var(--text-muted)">Recommendation Algorithms</span>
          <div class="env-setup__rec-grid">
            <div
              v-for="alg in recAlgorithms"
              :key="alg.key"
              class="env-setup__rec-card"
              :class="{'env-setup__rec-card--active': simConfig.algorithm === alg.key}"
              @click="simConfig.algorithm = alg.key"
            >
              <span class="material-symbols-outlined env-setup__rec-icon">{{ alg.icon }}</span>
              <div class="env-setup__rec-name">{{ alg.name }}</div>
              <div class="env-setup__rec-desc">{{ alg.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Generation progress (shown while generating) -->
        <div v-if="isGenerating" class="env-setup__gen-progress card-nested">
          <div class="env-setup__gen-progress-header">
            <div class="ai-chip">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">Generating agent personas…</span>
            </div>
            <span class="label-sm" style="color:var(--text-muted)">{{ genProgress }}%</span>
          </div>
          <div class="env-setup__progress-track">
            <div
              class="env-setup__progress-fill"
              :style="genProgress > 0 ? `width:${genProgress}%` : ''"
              :class="genProgress === 0 ? 'env-setup__progress-fill--indeterminate' : ''"
            ></div>
          </div>
          <span class="label-sm" style="color:var(--text-muted)">{{ statusMsg || 'Building agent memories from graph data…' }}</span>
          <div v-if="profiles.length > 0" class="env-setup__live-profiles">
            <span class="label-sm" style="color:var(--text-muted)">{{ profiles.length }} agents ready so far</span>
            <div class="env-setup__profiles-grid">
              <div v-for="p in profiles.slice(0, 6)" :key="p.user_id" class="env-setup__profile-card card-nested">
                <div class="env-setup__profile-avatar">{{ (p.name || p.username || '?').charAt(0).toUpperCase() }}</div>
                <div class="env-setup__profile-info">
                  <div class="env-setup__profile-name">{{ p.name || p.username }}</div>
                  <div class="env-setup__profile-role label-sm">{{ p.profession || p.mbti || 'Agent' }}</div>
                </div>
                <span class="chip chip-green" style="font-size:.6rem">Ready</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Generated agents summary (shown after done) -->
        <div v-if="profiles.length > 0 && !isGenerating" class="env-setup__gen-done card-nested">
          <div class="env-setup__gen-done-header">
            <span class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check_circle</span>
              {{ profiles.length }} agents generated
            </span>
            <span class="label-sm" style="color:var(--text-muted)">{{ profiles.length }} of {{ simConfig.agentCount }} requested · from {{ totalEntities }} available</span>
          </div>
          <div class="env-setup__profiles-grid">
            <div v-for="p in (showAllAgents ? profiles : profiles.slice(0, 6))" :key="p.user_id" class="env-setup__profile-card card-nested">
              <div class="env-setup__profile-avatar">{{ (p.name || p.username || '?').charAt(0).toUpperCase() }}</div>
              <div class="env-setup__profile-info">
                <div class="env-setup__profile-name">{{ p.name || p.username }}</div>
                <div class="env-setup__profile-role label-sm">{{ p.profession || p.mbti || 'Agent' }}</div>
              </div>
            </div>
          </div>
          <button v-if="profiles.length > 6" @click="showAllAgents = !showAllAgents" class="btn-ghost" style="font-size:.75rem;margin-top:.5rem">
            <template v-if="!showAllAgents">
              +{{ profiles.length - 6 }} more agents
              <span class="material-symbols-outlined" style="font-size:14px">expand_more</span>
            </template>
            <template v-else>
              Show fewer
              <span class="material-symbols-outlined" style="font-size:14px">expand_less</span>
            </template>
          </button>
        </div>
      </div>

      <div v-if="phaseError[2]" class="env-setup__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError[2] }}
      </div>

      <div v-if="phase === 2 && !isGenerating" class="env-setup__cta" ref="phase2Ref">
        <button class="btn-primary" @click="saveAndGenerate" :disabled="isProcessing">
          <span class="material-symbols-outlined" style="font-size:18px">rocket_launch</span>
          {{ isProcessing ? 'Saving…' : 'Save & Generate Agents' }}
        </button>
      </div>

      <!-- Final -->
      <div v-if="phase > 2" class="env-setup__complete" ref="phase3Ref">
        <div class="chip chip-green">
          <span class="material-symbols-outlined" style="font-size:14px">check_circle</span>
          Env Setup Complete — {{ profiles.length }} agents ready
        </div>
        <button
          v-if="!autoMode"
          class="btn-primary env-setup__launch-btn"
          @click="$emit('completed', { simulation_id: simulationId, max_rounds: parseInt(simConfig.rounds) })"
        >
          Launch Simulation
          <span class="material-symbols-outlined" style="font-size:18px">rocket_launch</span>
        </button>
        <div v-else class="ai-chip">
          <span class="ai-chip-dot"></span>
          <span class="label-sm" style="color:var(--secondary)">Proceeding to Simulation…</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { createSimulation, prepareSimulation, configureSimulation } from '../api.js'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'

const props = defineProps({ projectData: Object })
const emit = defineEmits(['completed'])

const autoMode = computed(() => !!props.projectData?.autoMode)

const phase        = ref(0)
const isProcessing = ref(false)
const isGenerating = ref(false)

// Auto-scroll to the newly active phase card in auto mode
watch(phase, (val) => {
  if (val >= 0 && val <= 2) scrollToEnvPhase(val)
})
const simulationId = ref(null)
const profiles     = ref([])
const statusMsg    = ref('')
const genProgress  = ref(0)
const phaseError   = ref({ 0: '', 1: '', 2: '' })

// Refs for auto-scroll targets
const phase0Ref = ref(null)
const phase1Ref = ref(null)
const phase2Ref = ref(null)
const phase3Ref = ref(null)

// Auto-scroll: in auto mode, scroll to newly active phase card
const envPhaseRef0 = ref(null)
const envPhaseRef1 = ref(null)
const envPhaseRef2 = ref(null)
const envPhaseRefs = [envPhaseRef0, envPhaseRef1, envPhaseRef2]

function scrollToEnvPhase(idx) {
  if (!autoMode.value) return
  nextTick(() => {
    const el = envPhaseRefs[idx]?.value
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function scrollToNextButton(phaseIdx) {
  if (autoMode.value) return
  const refs = [phase0Ref, phase1Ref, phase2Ref, phase3Ref]
  nextTick(() => {
    const el = refs[phaseIdx]?.value
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      // Add a brief highlight flash so user notices the button
      el.classList.add('env-setup__cta--highlight')
      setTimeout(() => el.classList.remove('env-setup__cta--highlight'), 1800)
    }
  })
}

const entityPreview = ref([])
const totalEntities = ref(0)
const showAllAgents = ref(false)

const simConfig = ref({
  duration:    '72',
  rounds:      '10',
  activeStart: '08:00',
  activeEnd:   '22:00',
  agentCount:  '9',
  platform:    'Both',
  algorithm:   'collab',
})

// ── Computed ─────────────────────────────────────────────────────────────────

const quickStats = computed(() => [
  { label: 'Simulation Duration', value: `${simConfig.value.duration}h`, sub: 'Estimated runtime', orb: 'orb-orange' },
  { label: 'Total Rounds', value: Number(simConfig.value.rounds).toLocaleString(), sub: 'Iteration cycles', orb: 'orb-blue' },
  { label: 'Active Hours', value: `${simConfig.value.activeStart.slice(0,5)}–${simConfig.value.activeEnd.slice(0,5)}`, sub: 'Agent activity window', orb: 'orb-orange' },
])

const instanceInfo = computed(() => [
  { label: 'Project ID',    value: props.projectData?.project_id || '—', copyable: true },
  { label: 'Graph ID',      value: props.projectData?.graph_id   || '—', copyable: true },
  { label: 'Simulation ID', value: simulationId.value || 'Generating…', copyable: !!simulationId.value },
  { label: 'Status',        value: simulationId.value ? 'Ready' : 'Pending', copyable: false },
])

const configFields = [
  { key: 'duration',    label: 'Duration (hours)',   type: 'number', placeholder: '72'    },
  { key: 'rounds',      label: 'Total Rounds',       type: 'number', placeholder: '10'   },
  { key: 'activeStart', label: 'Active Hours Start', type: 'text',   placeholder: '08:00' },
  { key: 'activeEnd',   label: 'Active Hours End',   type: 'text',   placeholder: '22:00' },
  { key: 'platform',    label: 'Platform',           type: 'select', options: ['Both', 'Info Plaza', 'Topic Community'] },
]

const recAlgorithms = [
  { key: 'collab',  icon: 'people',  name: 'Collaborative', desc: 'User-based filtering' },
  { key: 'content', icon: 'article', name: 'Content-Based', desc: 'Topic similarity'     },
  { key: 'hybrid',  icon: 'merge',   name: 'Hybrid',        desc: 'Combined approach'    },
  { key: 'random',  icon: 'shuffle', name: 'Random',        desc: 'Baseline control'     },
]

// ── Helpers ───────────────────────────────────────────────────────────────────

function phaseClass(p) {
  if (phase.value > p)   return 'env-setup__phase--completed'
  if (phase.value === p) return 'env-setup__phase--active'
  return 'env-setup__phase--locked'
}

function adjustAgentCount(delta) {
  const cur = parseInt(simConfig.value.agentCount) || 1
  const next = Math.max(1, Math.min(totalEntities.value || 9999, cur + delta))
  simConfig.value.agentCount = String(next)
}

function clampAgentCount() {
  const v = parseInt(simConfig.value.agentCount) || 1
  simConfig.value.agentCount = String(Math.max(1, Math.min(totalEntities.value || 9999, v)))
}

function copy(text) {
  navigator.clipboard.writeText(text).catch(() => {})
}

// ── Phase 01: Create Simulation ───────────────────────────────────────────────

async function initSimulation() {
  isProcessing.value = true
  phaseError.value[0] = ''
  statusMsg.value = 'Creating simulation instance…'
  try {
    const res = await createSimulation(props.projectData.project_id)
    if (!res.success) throw new Error(res.error || 'Simulation create failed')
    simulationId.value = res.data?.simulation_id || res.data?.id
    phase.value = 1
    // In manual mode: scroll to next button. In auto mode: trigger next step.
    if (autoMode.value) {
      await new Promise(r => setTimeout(r, 600))
      await previewEntities()
    } else {
      scrollToNextButton(1)
    }
  } catch (err) {
    phaseError.value[0] = err.message
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

// ── Phase 02: Preview Entities (fast, no LLM) ────────────────────────────────

async function previewEntities() {
  isProcessing.value = true
  phaseError.value[1] = ''
  statusMsg.value = 'Scanning knowledge graph…'
  try {
    const graphId = props.projectData?.graph_id
    if (!graphId) throw new Error('No graph_id found — build the graph first')

    const res = await fetch(`${BASE_URL}/simulation/entities/${graphId}?enrich=false`)
    const data = await res.json()
    if (!data.success) throw new Error(data.error || 'Entity scan failed')

    const raw = data.data
    totalEntities.value = raw.filtered_count || raw.total_count || 0

    // Build per-type breakdown from entities array
    const counts = {}
    if (Array.isArray(raw.entities)) {
      raw.entities.forEach(e => {
        const t = (e.labels || []).find(l => l !== 'Entity' && l !== 'Node') || 'Unknown'
        counts[t] = (counts[t] || 0) + 1
      })
      entityPreview.value = Object.entries(counts).map(([type, count]) => ({ type, count }))
    } else if (raw.entity_types && typeof raw.entity_types === 'object' && !Array.isArray(raw.entity_types)) {
      entityPreview.value = Object.entries(raw.entity_types).map(([type, count]) => ({ type, count }))
    } else {
      entityPreview.value = [{ type: 'Entities', count: totalEntities.value }]
    }

    // Pre-fill agentCount with total available as sensible default
    simConfig.value.agentCount = String(totalEntities.value)

    phase.value = 2
    if (autoMode.value) {
      await new Promise(r => setTimeout(r, 600))
      await saveAndGenerate()
    } else {
      scrollToNextButton(2)
    }
  } catch (err) {
    phaseError.value[1] = err.message
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

// ── Phase 03: Save Config → Generate Agents ──────────────────────────────────

async function saveAndGenerate() {
  isProcessing.value = true
  phaseError.value[2] = ''
  try {
    // Step A: Save configuration
    statusMsg.value = 'Saving configuration…'
    const platformMap = { 'Both': 'reddit', 'Info Plaza': 'reddit', 'Topic Community': 'twitter' }
    const mappedPlatform = platformMap[simConfig.value.platform] || 'reddit'

    const cfgRes = await configureSimulation(simulationId.value, {
      duration_hours: parseInt(simConfig.value.duration),
      max_rounds:     parseInt(simConfig.value.rounds),
      active_start:   simConfig.value.activeStart,
      active_end:     simConfig.value.activeEnd,
      agent_count:    parseInt(simConfig.value.agentCount),
      platform:       mappedPlatform,
      algorithm:      simConfig.value.algorithm,
    })
    if (!cfgRes.success) throw new Error(cfgRes.error || 'Configure failed')

    // Step B: Trigger agent generation with the configured count
    isProcessing.value = false
    isGenerating.value = true
    genProgress.value = 0
    statusMsg.value = 'Querying knowledge graph for agent seeds…'

    const prepRes = await prepareSimulation(
      simulationId.value,
      props.projectData.project_id,
      {
        agentCount:      parseInt(simConfig.value.agentCount),
        forceRegenerate: true,
      }
    )
    if (!prepRes.success) throw new Error(prepRes.error || 'Prepare failed')

    if (prepRes.data?.already_prepared && !prepRes.data?.task_id) {
      await loadProfiles()
      phase.value = 3
      if (autoMode.value) {
        await new Promise(r => setTimeout(r, 1000))
        emit('completed', { simulation_id: simulationId.value, max_rounds: parseInt(simConfig.value.rounds) })
      }
      return
    }

    // Step C: Poll progress with live profile loading
    if (prepRes.data?.task_id) {
      await pollPrepareTask(prepRes.data.task_id, simulationId.value)
    }

    await loadProfiles()
    phase.value = 3
    if (autoMode.value) {
      await new Promise(r => setTimeout(r, 1000))
      emit('completed', { simulation_id: simulationId.value, max_rounds: parseInt(simConfig.value.rounds) })
    } else {
      scrollToNextButton(3)
    }
  } catch (err) {
    phaseError.value[2] = err.message
  } finally {
    isProcessing.value = false
    isGenerating.value = false
    statusMsg.value = ''
  }
}

// ── Polling ───────────────────────────────────────────────────────────────────

async function pollPrepareTask(taskId, simId, intervalMs = 3000, timeoutMs = 600000) {
  const start = Date.now()
  const profilePoller = setInterval(() => loadProfiles(), 8000)

  return new Promise((resolve, reject) => {
    const id = setInterval(async () => {
      if (Date.now() - start > timeoutMs) {
        clearInterval(id)
        clearInterval(profilePoller)
        reject(new Error('Preparation timed out — check backend logs.'))
        return
      }
      try {
        const res = await fetch(`${BASE_URL}/simulation/prepare/status`, {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify({ task_id: taskId, simulation_id: simId }),
        })
        const data = await res.json()
        const task = data.data

        if (task?.progress !== undefined) genProgress.value = task.progress
        if (task?.message) statusMsg.value = task.message

        if (task?.status === 'completed' || task?.status === 'ready' || task?.already_prepared) {
          clearInterval(id)
          clearInterval(profilePoller)
          genProgress.value = 100
          resolve(task)
        }
        if (task?.status === 'failed') {
          clearInterval(id)
          clearInterval(profilePoller)
          reject(new Error(task.error || 'Preparation failed'))
        }
      } catch (e) {
        console.warn('Poll error (will retry):', e.message)
      }
    }, intervalMs)
  })
}

async function loadProfiles() {
  try {
    const res = await fetch(`${BASE_URL}/simulation/${simulationId.value}/profiles/realtime?platform=reddit`)
    const data = await res.json()
    const loaded = data?.data?.profiles || []
    if (loaded.length > 0) profiles.value = loaded
  } catch (e) { /* silent */ }
}

onMounted(() => {
  if (autoMode.value) {
    // Auto mode: kick off the first phase automatically after a short delay
    setTimeout(() => {
      initSimulation()
    }, 800)
  }
})
</script>

<style scoped>
.env-setup { display: flex; flex-direction: column; gap: 1.5rem; }

.env-setup__stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }

.env-setup__stat { padding: 1.25rem 1.5rem; overflow: hidden; }

.env-setup__stat-val { font-size: 1.875rem; font-weight: 700; color: var(--primary); margin: 0.25rem 0 0.125rem; }

.env-setup__stat-sub { font-size: 0.6875rem; color: var(--text-muted); }

.env-setup__phase { padding: 1.75rem; transition: opacity var(--duration-normal); }
.env-setup__phase--locked { opacity: 0.4; pointer-events: none; }
.env-setup__phase--active { border-color: rgba(255,181,158,.25); box-shadow: var(--shadow-glow-primary); }
.env-setup__phase--completed { border-color: rgba(134,239,172,.12); }

.env-setup__phase-header { display: flex; flex-direction: column; gap: .625rem; margin-bottom: 1.25rem; }

.env-setup__phase-title-row { display: flex; align-items: center; gap: .875rem; flex-wrap: wrap; }

.env-setup__phase-num { font-size: 2rem; font-weight: 700; color: var(--text-muted); opacity: .35; line-height: 1; }

.env-setup__phase-badge { margin-left: auto; }

.env-setup__phase-desc { color: var(--text-muted); font-size: .875rem; line-height: 1.7; max-width: 640px; }

.env-setup__info-card { display: flex; flex-direction: column; gap: .25rem; margin-bottom: 1.25rem; }

.env-setup__info-row { display: flex; align-items: center; gap: 1rem; padding: .5rem 0; border-bottom: 1px solid var(--ghost-border); }
.env-setup__info-row:last-child { border-bottom: none; }
.env-setup__info-label { color: var(--text-muted); min-width: 110px; }
.env-setup__info-val { flex: 1; color: var(--text-primary); font-size: .8125rem; }

/* Entity preview */
.env-setup__entity-preview { display: flex; flex-direction: column; gap: .75rem; margin-bottom: 1.25rem; }
.env-setup__entity-summary { display: flex; flex-direction: column; gap: 1rem; }
.env-setup__entity-total { display: flex; align-items: baseline; gap: .75rem; }
.env-setup__entity-types { display: flex; flex-wrap: wrap; gap: .5rem; }
.env-setup__entity-type-chip { display: flex; align-items: center; gap: .375rem; padding: .375rem .75rem; background: var(--surface-container-high); border: 1px solid var(--ghost-border); border-radius: var(--radius-full); font-size: .8125rem; color: var(--text-secondary); }
.env-setup__entity-type-name { font-weight: 600; }
.env-setup__entity-type-count { margin-left: .25rem; }
.env-setup__preview-note { display: flex; align-items: flex-start; gap: .5rem; padding: .75rem 1rem; background: rgba(255,90,31,.05); border: 1px solid rgba(255,90,31,.15); border-radius: var(--radius-md); }

/* Agent count control */
.env-setup__agent-count-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.env-setup__agent-count-label { display: flex; align-items: center; gap: .75rem; }
.env-setup__agent-count-ctrl { display: flex; align-items: center; gap: .5rem; }
.env-setup__count-btn { width: 32px; height: 32px; border-radius: var(--radius-md); background: var(--surface-container-high); border: 1px solid var(--ghost-border); color: var(--text-primary); font-size: 1.125rem; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background var(--duration-fast); }
.env-setup__count-btn:hover:not(:disabled) { background: var(--surface-high); }
.env-setup__count-btn:disabled { opacity: .35; cursor: not-allowed; }
.env-setup__count-input { width: 72px; text-align: center; font-size: 1rem; font-weight: 700; }

/* Config grid */
.env-setup__config-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.env-setup__config-field { display: flex; flex-direction: column; gap: .5rem; }
.env-setup__config-label { color: var(--text-muted); }
.env-setup__config-input { font-size: .875rem; }

/* Recommendation algorithms */
.env-setup__rec-section { display: flex; flex-direction: column; gap: .75rem; margin-bottom: 1.5rem; }
.env-setup__rec-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; }
.env-setup__rec-card { padding: 1rem; background: var(--surface-low); border: 1px solid var(--ghost-border); border-radius: var(--radius-md); cursor: pointer; transition: all var(--duration-fast); display: flex; flex-direction: column; align-items: flex-start; gap: .375rem; }
.env-setup__rec-card:hover { background: var(--surface-container-high); border-color: rgba(171,137,127,.3); }
.env-setup__rec-card--active { background: rgba(255,90,31,.08); border-color: rgba(255,90,31,.3); box-shadow: var(--shadow-glow-primary); }
.env-setup__rec-icon { font-size: 20px; color: var(--primary); margin-bottom: .25rem; }
.env-setup__rec-name { font-size: .8125rem; font-weight: 700; color: var(--text-primary); }
.env-setup__rec-desc { font-size: .6875rem; color: var(--text-muted); }

/* Generation progress */
.env-setup__gen-progress { display: flex; flex-direction: column; gap: .75rem; margin-bottom: 1.25rem; }
.env-setup__gen-progress-header { display: flex; align-items: center; justify-content: space-between; }
.env-setup__progress-track { height: 4px; background: var(--surface-container-high); border-radius: var(--radius-full); overflow: hidden; }
.env-setup__progress-fill { height: 100%; background: var(--gradient-primary); border-radius: var(--radius-full); transition: width 400ms ease; }
.env-setup__progress-fill--indeterminate { width: 40%; animation: indeterminate 1.8s ease-in-out infinite; }
@keyframes indeterminate { 0% { transform: translateX(-100%); } 100% { transform: translateX(350%); } }
.env-setup__live-profiles { display: flex; flex-direction: column; gap: .5rem; margin-top: .5rem; }

/* Gen done */
.env-setup__gen-done { display: flex; flex-direction: column; gap: .75rem; margin-bottom: 1.25rem; }
.env-setup__gen-done-header { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }

/* Profiles */
.env-setup__profiles-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: .5rem; }
.env-setup__profile-card { display: flex; align-items: center; gap: .75rem; }
.env-setup__profile-avatar { width: 32px; height: 32px; border-radius: var(--radius-full); background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: .875rem; font-weight: 700; color: var(--on-primary); flex-shrink: 0; }
.env-setup__profile-info { flex: 1; min-width: 0; }
.env-setup__profile-name { font-size: .8125rem; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.env-setup__profile-role { color: var(--text-muted); }

/* Error */
.env-setup__error { display: flex; align-items: center; gap: .5rem; padding: .75rem 1rem; background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.2); border-radius: var(--radius-md); color: #f87171; font-size: .8125rem; margin-bottom: 1rem; }

/* CTA */
.env-setup__cta { display: flex; gap: .75rem; padding-top: .25rem; position: relative; }

/* Highlight flash when auto-scrolled to */
.env-setup__cta--highlight {
  animation: cta-highlight-flash 1.8s ease-out forwards;
}
@keyframes cta-highlight-flash {
  0%   { background: rgba(255, 90, 31, 0.12); border-radius: 8px; }
  100% { background: transparent; }
}

/* Pulse ring on the primary button when it's a manual-mode "action needed" moment */
.env-setup__cta .btn-primary,
.env-setup__launch-btn {
  animation: cta-pulse-glow 2s ease-in-out infinite;
}
@keyframes cta-pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 90, 31, 0); }
  50%       { box-shadow: 0 0 0 6px rgba(255, 90, 31, 0.22); }
}

/* Auto-mode banner */
.env-setup__auto-banner {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.625rem 1rem;
  background: rgba(255, 90, 31, 0.05);
  border: 1px solid rgba(255, 90, 31, 0.15);
  border-radius: var(--radius-md);
  font-size: 0.75rem;
  color: var(--text-muted);
}
.env-setup__auto-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--primary);
  flex-shrink: 0;
  animation: blink 1.2s step-end infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Complete */
.env-setup__complete { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.25rem; background: rgba(134,239,172,.05); border: 1px solid rgba(134,239,172,.12); border-radius: var(--radius-md); margin-top: .75rem; }
</style>