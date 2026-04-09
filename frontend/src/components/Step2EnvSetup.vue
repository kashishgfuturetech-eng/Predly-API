<template>
  <div class="env-setup">
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
    <div class="env-setup__phase card" :class="phaseClass(0)">
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

      <div v-if="phase === 0 && !isProcessing" class="env-setup__cta">
        <button class="btn-primary" @click="initSimulation">
          <span class="material-symbols-outlined" style="font-size:18px">play_circle</span>
          Initialize Instance
        </button>
      </div>
    </div>

    <!-- ── Phase 02: Agent Personas ── -->
    <div class="env-setup__phase card" :class="phaseClass(1)">
      <div class="env-setup__phase-header">
        <span class="chip chip-blue label-sm">POST /api/simulation/prepare</span>
        <div class="env-setup__phase-title-row">
          <span class="env-setup__phase-num font-mono">02</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Generate Agent Personas</h2>
          <div class="env-setup__phase-badge">
            <span v-if="phase > 1" class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
            </span>
            <div v-else-if="phase === 1 && isProcessing" class="ai-chip">
              <span class="ai-chip-dot"></span>
              <span class="label-sm" style="color:var(--secondary)">{{ statusMsg || 'Generating personas…' }}</span>
            </div>
            <span v-else class="chip chip-muted">Waiting</span>
          </div>
        </div>
        <p class="env-setup__phase-desc">
          Combined with context, automatically invoke tools to organize entities and relationships
          from the knowledge graph. Initialize simulation individuals with unique behaviors and
          memories based on reality seeds.
        </p>
      </div>

      <!-- Progress bar while preparing -->
      <div v-if="phase === 1 && isProcessing" class="env-setup__progress">
        <div class="env-setup__progress-track">
          <div class="env-setup__progress-fill env-setup__progress-fill--indeterminate"></div>
        </div>
        <span class="label-sm" style="color:var(--text-muted)">{{ statusMsg || 'Building agent memories from graph…' }}</span>
      </div>

      <!-- Agent Stats -->
      <div v-if="profiles.length > 0" class="env-setup__agent-stats">
        <div class="card-nested env-setup__agent-stat" v-for="s in agentStats" :key="s.label">
          <div class="env-setup__stat-val font-headline" style="font-size:1.5rem">{{ s.value }}</div>
          <div class="label-sm" style="color:var(--text-muted)">{{ s.label }}</div>
        </div>
      </div>

      <!-- Profiles Preview -->
      <div v-if="profiles.length > 0" class="env-setup__profiles">
        <span class="label-sm" style="color:var(--text-muted)">Agent Profiles Preview</span>
        <div class="env-setup__profiles-grid">
          <div v-for="p in profiles.slice(0, 6)" :key="p.id" class="env-setup__profile-card card-nested">
            <div class="env-setup__profile-avatar">
              {{ (p.name || p.username || '?').charAt(0).toUpperCase() }}
            </div>
            <div class="env-setup__profile-info">
              <div class="env-setup__profile-name">{{ p.name || p.username }}</div>
              <div class="env-setup__profile-role label-sm">{{ p.role || p.occupation || 'Agent' }}</div>
            </div>
            <span class="chip chip-blue" style="font-size:.6rem">{{ p.platform || 'Info Plaza' }}</span>
          </div>
        </div>
        <button v-if="profiles.length > 6" class="btn-ghost" style="font-size:.75rem;margin-top:.5rem">
          +{{ profiles.length - 6 }} more profiles
          <span class="material-symbols-outlined" style="font-size:14px">expand_more</span>
        </button>
      </div>

      <div v-if="phaseError[1]" class="env-setup__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError[1] }}
      </div>

      <div v-if="phase === 1 && !isProcessing" class="env-setup__cta">
        <button class="btn-primary" @click="generatePersonas">
          <span class="material-symbols-outlined" style="font-size:18px">group</span>
          Generate Personas
        </button>
      </div>
    </div>

    <!-- ── Phase 03: Simulation Config ── -->
    <div class="env-setup__phase card" :class="phaseClass(2)">
      <div class="env-setup__phase-header">
        <span class="chip chip-blue label-sm">POST /api/simulation/configure</span>
        <div class="env-setup__phase-title-row">
          <span class="env-setup__phase-num font-mono">03</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Simulation Parameters</h2>
          <div class="env-setup__phase-badge">
            <span v-if="phase > 2" class="chip chip-green">
              <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
            </span>
            <span v-else class="chip chip-muted">{{ phase < 2 ? 'Waiting' : 'Configure' }}</span>
          </div>
        </div>
        <p class="env-setup__phase-desc">
          Tune simulation duration, agent density, active hours, and platform-specific behavior rules.
        </p>
      </div>

      <div v-if="phase >= 2" class="env-setup__config-grid">
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

      <!-- Recommendation Logic -->
      <div v-if="phase >= 2" class="env-setup__rec-section">
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

      <div v-if="phaseError[2]" class="env-setup__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError[2] }}
      </div>

      <div v-if="phase === 2" class="env-setup__cta">
        <button class="btn-primary" @click="saveConfig" :disabled="isProcessing">
          <span class="material-symbols-outlined" style="font-size:18px">save</span>
          {{ isProcessing ? 'Saving…' : 'Save Configuration' }}
        </button>
      </div>

      <!-- Final -->
      <div v-if="phase > 2" class="env-setup__complete">
        <div class="chip chip-green">
          <span class="material-symbols-outlined" style="font-size:14px">check_circle</span>
          Env Setup Complete
        </div>
        <button class="btn-primary" @click="$emit('completed', { simulation_id: simulationId })">
          Launch Simulation
          <span class="material-symbols-outlined" style="font-size:18px">rocket_launch</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createSimulation, prepareSimulation, configureSimulation, pollTask } from '../api.js'

const props = defineProps({ projectData: Object })
const emit = defineEmits(['completed'])

const phase = ref(0)
const isProcessing = ref(false)
const simulationId = ref(null)
const profiles = ref([])
const statusMsg = ref('')
const phaseError = ref({ 0: '', 1: '', 2: '' })

const simConfig = ref({
  duration: '72',
  rounds: '1200',
  activeStart: '08:00',
  activeEnd: '22:00',
  agentCount: '50',
  platform: 'Both',
  algorithm: 'collab',
})

const quickStats = computed(() => [
  { label: 'Simulation Duration', value: `${simConfig.value.duration}h`, sub: 'Estimated runtime', orb: 'orb-orange' },
  { label: 'Total Rounds',        value: Number(simConfig.value.rounds).toLocaleString(), sub: 'Iteration cycles', orb: 'orb-blue' },
  { label: 'Active Hours',        value: `${simConfig.value.activeStart.slice(0,5)}–${simConfig.value.activeEnd.slice(0,5)}`, sub: 'Agent activity window', orb: 'orb-orange' },
])

const instanceInfo = computed(() => [
  { label: 'Project ID',    value: props.projectData?.project_id || '—', copyable: true },
  { label: 'Graph ID',      value: props.projectData?.graph_id   || '—', copyable: true },
  { label: 'Simulation ID', value: simulationId.value || 'Generating…', copyable: !!simulationId.value },
  { label: 'Status',        value: simulationId.value ? 'Ready' : 'Pending', copyable: false },
])

const agentStats = computed(() => [
  { label: 'Agents Generated', value: profiles.value.length },
  { label: 'Expected Total',   value: simConfig.value.agentCount },
  { label: 'From Graph',       value: profiles.value.length > 0 ? 'Yes' : '—' },
])

const configFields = [
  { key: 'duration',    label: 'Duration (hours)',   type: 'number', placeholder: '72' },
  { key: 'rounds',      label: 'Total Rounds',       type: 'number', placeholder: '1200' },
  { key: 'activeStart', label: 'Active Hours Start', type: 'text',   placeholder: '08:00' },
  { key: 'activeEnd',   label: 'Active Hours End',   type: 'text',   placeholder: '22:00' },
  { key: 'agentCount',  label: 'Agent Count',        type: 'number', placeholder: '50' },
  { key: 'platform',    label: 'Platform',           type: 'select', options: ['Both', 'Info Plaza', 'Topic Community'] },
]

const recAlgorithms = [
  { key: 'collab',  icon: 'people',   name: 'Collaborative', desc: 'User-based filtering' },
  { key: 'content', icon: 'article',  name: 'Content-Based', desc: 'Topic similarity' },
  { key: 'hybrid',  icon: 'merge',    name: 'Hybrid',        desc: 'Combined approach' },
  { key: 'random',  icon: 'shuffle',  name: 'Random',        desc: 'Baseline control' },
]

function phaseClass(p) {
  if (phase.value > p) return 'env-setup__phase--completed'
  if (phase.value === p) return 'env-setup__phase--active'
  return 'env-setup__phase--locked'
}

// ─── Phase 01 ────────────────────────────────────────────────────────────────

async function initSimulation() {
  isProcessing.value = true
  phaseError.value[0] = ''
  statusMsg.value = 'Creating simulation instance…'
  try {
    const res = await createSimulation(props.projectData.project_id)
    if (!res.success) throw new Error(res.error || 'Simulation create failed')

    let result = res.data
    if (res.data?.task_id) {
      statusMsg.value = 'Polling for instance ID…'
      result = await pollTask(res.data.task_id)
    }

    simulationId.value = result?.simulation_id || result?.id || `SIM-${Math.random().toString(36).slice(2,8).toUpperCase()}`
    phase.value = 1
  } catch (err) {
    phaseError.value[0] = err.message
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

// ─── Phase 02 ────────────────────────────────────────────────────────────────

async function generatePersonas() {
  isProcessing.value = true
  phaseError.value[1] = ''
  statusMsg.value = 'Querying knowledge graph for agent seeds…'
  try {
    const res = await prepareSimulation(simulationId.value, props.projectData.project_id)
    if (!res.success) throw new Error(res.error || 'Prepare failed')

    let result = res.data
    if (res.data?.task_id) {
      statusMsg.value = 'Building agent memories — this takes 1–5 min on CPU…'
      result = await pollTask(res.data.task_id, 4000)
    }

    // Backend may return profiles array directly or inside a key
    const rawProfiles = result?.profiles || result?.agents || result?.data || []
    profiles.value = Array.isArray(rawProfiles) ? rawProfiles : []

    phase.value = 2
  } catch (err) {
    phaseError.value[1] = err.message
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

// ─── Phase 03 ────────────────────────────────────────────────────────────────

async function saveConfig() {
  isProcessing.value = true
  phaseError.value[2] = ''
  try {
    const res = await configureSimulation(simulationId.value, {
      duration_hours:  parseInt(simConfig.value.duration),
      max_rounds:      parseInt(simConfig.value.rounds),
      active_start:    simConfig.value.activeStart,
      active_end:      simConfig.value.activeEnd,
      agent_count:     parseInt(simConfig.value.agentCount),
      platform:        simConfig.value.platform,
      algorithm:       simConfig.value.algorithm,
    })
    if (!res.success) throw new Error(res.error || 'Configure failed')
    phase.value = 3
  } catch (err) {
    phaseError.value[2] = err.message
  } finally {
    isProcessing.value = false
  }
}

function copy(text) {
  navigator.clipboard.writeText(text).catch(() => {})
}
</script>

<style scoped>
.env-setup {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.env-setup__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.env-setup__stat {
  padding: 1.25rem 1.5rem;
  overflow: hidden;
}

.env-setup__stat-val {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--primary);
  margin: 0.25rem 0 0.125rem;
}

.env-setup__stat-sub {
  font-size: 0.6875rem;
  color: var(--text-muted);
}

/* Phase */
.env-setup__phase {
  padding: 1.75rem;
  transition: opacity var(--duration-normal);
}

.env-setup__phase--locked {
  opacity: 0.4;
  pointer-events: none;
}

.env-setup__phase--active {
  border-color: rgba(255, 181, 158, 0.25);
  box-shadow: var(--shadow-glow-primary);
}

.env-setup__phase--completed {
  border-color: rgba(134, 239, 172, 0.12);
}

.env-setup__phase-header {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1.25rem;
}

.env-setup__phase-title-row {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex-wrap: wrap;
}

.env-setup__phase-num {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-muted);
  opacity: 0.35;
  line-height: 1;
}

.env-setup__phase-badge { margin-left: auto; }

.env-setup__phase-desc {
  color: var(--text-muted);
  font-size: 0.875rem;
  line-height: 1.7;
  max-width: 640px;
}

/* Info Card */
.env-setup__info-card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1.25rem;
}

.env-setup__info-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--ghost-border);
}
.env-setup__info-row:last-child { border-bottom: none; }

.env-setup__info-label { color: var(--text-muted); min-width: 110px; }

.env-setup__info-val {
  flex: 1;
  color: var(--text-primary);
  font-size: 0.8125rem;
}

/* Progress */
.env-setup__progress {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.env-setup__progress-track {
  height: 4px;
  background: var(--surface-container-high);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.env-setup__progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  transition: width 200ms ease;
}

/* Indeterminate animation for CPU tasks with unknown duration */
.env-setup__progress-fill--indeterminate {
  width: 40%;
  animation: indeterminate 1.8s ease-in-out infinite;
}
@keyframes indeterminate {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(350%); }
}

/* Agent Stats */
.env-setup__agent-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.env-setup__agent-stat { padding: 1rem; }

/* Profiles */
.env-setup__profiles {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.env-setup__profiles-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.env-setup__profile-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.env-setup__profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--on-primary);
  flex-shrink: 0;
}

.env-setup__profile-info { flex: 1; min-width: 0; }

.env-setup__profile-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.env-setup__profile-role { color: var(--text-muted); }

/* Config */
.env-setup__config-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.env-setup__config-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.env-setup__config-label { color: var(--text-muted); }

.env-setup__config-input { font-size: 0.875rem; }

/* Recommendation Algorithms */
.env-setup__rec-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.env-setup__rec-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.env-setup__rec-card {
  padding: 1rem;
  background: var(--surface-low);
  border: 1px solid var(--ghost-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.375rem;
}
.env-setup__rec-card:hover {
  background: var(--surface-container-high);
  border-color: rgba(171, 137, 127, 0.3);
}
.env-setup__rec-card--active {
  background: rgba(255, 90, 31, 0.08);
  border-color: rgba(255, 90, 31, 0.3);
  box-shadow: var(--shadow-glow-primary);
}

.env-setup__rec-icon {
  font-size: 20px;
  color: var(--primary);
  margin-bottom: 0.25rem;
}

.env-setup__rec-name {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--text-primary);
}

.env-setup__rec-desc {
  font-size: 0.6875rem;
  color: var(--text-muted);
}

/* Error */
.env-setup__error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius-md);
  color: #f87171;
  font-size: 0.8125rem;
  margin-bottom: 1rem;
}

/* CTA */
.env-setup__cta { display: flex; gap: 0.75rem; padding-top: 0.25rem; }

/* Complete */
.env-setup__complete {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  background: rgba(134, 239, 172, 0.05);
  border: 1px solid rgba(134, 239, 172, 0.12);
  border-radius: var(--radius-md);
  margin-top: 0.75rem;
}
</style>