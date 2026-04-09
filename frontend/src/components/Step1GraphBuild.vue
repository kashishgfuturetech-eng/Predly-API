<template>
  <div class="graph-build">
    <!-- Metrics Row -->
    <div class="graph-build__metrics">
      <div class="graph-build__metric card" v-for="m in metrics" :key="m.label">
        <div class="orb orb-blue" style="width:80px;height:80px;top:-20px;right:-20px;opacity:0.3;"></div>
        <span class="label-sm" style="color:var(--text-muted)">{{ m.label }}</span>
        <div class="graph-build__metric-val font-headline">{{ m.value }}</div>
        <div class="graph-build__metric-sub">{{ m.sub }}</div>
      </div>
    </div>

    <!-- ── Phase 01: Ontology Generation ── -->
    <!-- Already completed on Home page via /ontology/generate -->
    <div class="graph-build__phase card" :class="phaseClass(0)">
      <div class="graph-build__phase-header">
        <div class="graph-build__phase-meta">
          <span class="chip chip-blue label-sm">POST /api/graph/ontology/generate</span>
          <span class="chip chip-green" style="margin-left:.5rem">
            <span class="material-symbols-outlined" style="font-size:11px">check</span> Completed on upload
          </span>
        </div>
        <div class="graph-build__phase-title-row">
          <span class="graph-build__phase-num font-mono">01</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Ontology Generation</h2>
        </div>
        <p class="graph-build__phase-desc">
          LLM analyzed your documents and simulation requirements, extracted reality seeds,
          and generated the ontology structure. Results are shown below.
        </p>
      </div>

      <!-- Detail overlay -->
      <transition name="overlay">
        <div v-if="selectedItem" class="graph-build__overlay glass-elevated">
          <div class="graph-build__overlay-header">
            <div style="display:flex;align-items:center;gap:.75rem">
              <span class="chip" :class="selectedItem.itemType === 'entity' ? 'chip-orange' : 'chip-blue'">
                {{ selectedItem.itemType === 'entity' ? 'ENTITY' : 'RELATION' }}
              </span>
              <span class="headline-md" style="color:var(--text-primary)">{{ selectedItem.name }}</span>
            </div>
            <button class="btn-ghost" @click="selectedItem = null">
              <span class="material-symbols-outlined">close</span>
            </button>
          </div>
          <p class="graph-build__overlay-desc">{{ selectedItem.description }}</p>

          <div v-if="selectedItem.attributes?.length" class="graph-build__overlay-section">
            <span class="label-sm" style="color:var(--text-muted)">Attributes</span>
            <div class="graph-build__attr-list">
              <div v-for="attr in selectedItem.attributes" :key="attr.name" class="graph-build__attr-item">
                <span class="graph-build__attr-name font-mono">{{ attr.name }}</span>
                <span class="chip chip-muted" style="font-size:.6rem">{{ attr.type }}</span>
                <span class="graph-build__attr-desc">{{ attr.description }}</span>
              </div>
            </div>
          </div>

          <div v-if="selectedItem.examples?.length" class="graph-build__overlay-section">
            <span class="label-sm" style="color:var(--text-muted)">Examples</span>
            <div style="display:flex;flex-wrap:wrap;gap:.375rem">
              <span v-for="ex in selectedItem.examples" :key="ex" class="chip chip-orange">{{ ex }}</span>
            </div>
          </div>

          <div v-if="selectedItem.source_targets?.length" class="graph-build__overlay-section">
            <span class="label-sm" style="color:var(--text-muted)">Connections</span>
            <div class="graph-build__conn-list">
              <div v-for="(c, i) in selectedItem.source_targets" :key="i" class="graph-build__conn-item">
                <span class="chip chip-muted">{{ c.source }}</span>
                <span class="material-symbols-outlined" style="font-size:16px;color:var(--primary)">arrow_forward</span>
                <span class="chip chip-muted">{{ c.target }}</span>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Entity Types from real API response -->
      <div v-if="entityTypes.length" class="graph-build__tags-section" :class="{'graph-build__tags-section--dimmed': selectedItem}">
        <span class="label-sm" style="color:var(--text-muted)">Generated Entity Types</span>
        <div class="graph-build__tag-list">
          <button
            v-for="entity in entityTypes"
            :key="entity.name"
            class="graph-build__tag"
            :class="{'graph-build__tag--selected': selectedItem?.name === entity.name}"
            @click="selectItem(entity, 'entity')"
          >
            <span class="material-symbols-outlined" style="font-size:14px">category</span>
            {{ entity.name }}
          </button>
        </div>
      </div>

      <!-- Relation Types -->
      <div v-if="relationTypes.length" class="graph-build__tags-section" :class="{'graph-build__tags-section--dimmed': selectedItem}">
        <span class="label-sm" style="color:var(--text-muted)">Generated Relation Types</span>
        <div class="graph-build__tag-list">
          <button
            v-for="rel in relationTypes"
            :key="rel.name"
            class="graph-build__tag graph-build__tag--relation"
            :class="{'graph-build__tag--selected': selectedItem?.name === rel.name}"
            @click="selectItem(rel, 'relation')"
          >
            <span class="material-symbols-outlined" style="font-size:14px">share</span>
            {{ rel.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- ── Phase 02: Graph Build (Entity Extraction + Neo4j Storage combined) ── -->
    <!-- Calls POST /api/graph/build — returns task_id, then we poll /task/:id -->
    <div class="graph-build__phase card" :class="phaseClass(1)">
      <div class="graph-build__phase-header">
        <div class="graph-build__phase-meta">
          <span class="chip chip-blue label-sm">POST /api/graph/build</span>
        </div>
        <div class="graph-build__phase-title-row">
          <span class="graph-build__phase-num font-mono">02</span>
          <h2 class="headline-md" style="color:var(--text-primary)">Entity Extraction &amp; Graph Storage</h2>
        </div>
        <p class="graph-build__phase-desc">
          Extract all named entities and relationships from documents using the ontology as schema,
          then write nodes and edges to Neo4j with vector embeddings for agent reasoning.
        </p>

        <!-- Status -->
        <div class="graph-build__phase-status">
          <span v-if="currentPhase > 1" class="chip chip-green">
            <span class="material-symbols-outlined" style="font-size:12px">check</span> Completed
          </span>
          <div v-else-if="currentPhase === 1 && isProcessing" class="ai-chip">
            <span class="ai-chip-dot"></span>
            <span class="label-sm" style="color:var(--secondary)">{{ statusMsg }}</span>
          </div>
          <span v-else-if="currentPhase === 1" class="chip chip-muted">Ready</span>
          <span v-else class="chip chip-muted">Waiting</span>
        </div>
      </div>

      <!-- Progress bar while building -->
      <div v-if="currentPhase === 1 && isProcessing && buildProgress > 0" class="graph-build__progress">
        <div class="graph-build__progress-header">
          <span class="label-sm" style="color:var(--text-muted)">Build Progress</span>
          <span class="font-mono" style="font-size:.75rem;color:var(--primary)">{{ buildProgress }}%</span>
        </div>
        <div class="graph-build__progress-bar">
          <div class="graph-build__progress-fill" :style="{ width: buildProgress + '%' }"></div>
        </div>
      </div>

      <!-- Stats grid after completion -->
      <div v-if="currentPhase > 1" class="graph-build__stats-grid">
        <div class="card-nested" v-for="s in graphStats" :key="s.label">
          <div class="graph-build__stat-val font-headline">{{ s.value }}</div>
          <div class="label-sm" style="color:var(--text-muted)">{{ s.label }}</div>
        </div>
      </div>

      <!-- Graph storage info -->
      <div v-if="currentPhase > 1 && graphStorageInfo" class="graph-build__info-card card-nested">
        <div class="graph-build__info-row" v-for="row in graphStorageInfo" :key="row.label">
          <span class="graph-build__info-label label-sm">{{ row.label }}</span>
          <span class="graph-build__info-val font-mono">{{ row.value }}</span>
        </div>
      </div>

      <!-- Error -->
      <div v-if="phaseError" class="graph-build__error">
        <span class="material-symbols-outlined" style="font-size:16px">error</span>
        {{ phaseError }}
      </div>

      <!-- CTA -->
      <div v-if="currentPhase === 1 && !isProcessing" class="graph-build__cta">
        <button class="btn-primary" @click="startBuild" :disabled="isProcessing">
          <span class="material-symbols-outlined" style="font-size:18px">account_tree</span>
          Build Graph
        </button>
      </div>

      <!-- Final CTA -->
      <div v-if="currentPhase > 1" class="graph-build__complete">
        <div class="graph-build__complete-badge chip chip-green">
          <span class="material-symbols-outlined" style="font-size:14px">check_circle</span>
          Graph Build Complete
        </div>
        <button class="btn-primary" @click="proceedToEnv">
          Proceed to Env Setup
          <span class="material-symbols-outlined" style="font-size:18px">arrow_forward</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { pollTask } from '../api.js'

const props = defineProps({ projectData: Object })
const emit = defineEmits(['completed'])

// Phase 0 = ontology (already done), Phase 1 = build, Phase 2 = done
const currentPhase = ref(1)
const isProcessing = ref(false)
const selectedItem = ref(null)
const statusMsg = ref('')
const phaseError = ref('')
const buildProgress = ref(0)

// Pull ontology from projectData (already returned by /ontology/generate on Home)
const entityTypes = computed(() =>
  props.projectData?.ontology?.entity_types ?? []
)
const relationTypes = computed(() =>
  // backend uses both "edge_types" and "relation_types" — handle both
  props.projectData?.ontology?.relation_types ??
  props.projectData?.ontology?.edge_types ?? []
)

const metrics = ref([
  { label: 'Documents',       value: '—', sub: 'Reality seeds loaded' },
  { label: 'Tokens Processed', value: '—', sub: 'Context window usage' },
  { label: 'Graph ID',        value: 'Pending', sub: 'Neo4j node ID' },
])

const graphStats = ref([
  { label: 'Nodes Written', value: '—' },
  { label: 'Edges Written', value: '—' },
  { label: 'Text Chunks',   value: '—' },
])

const graphStorageInfo = ref(null)

onMounted(() => {
  // Populate doc count from projectData
  const docCount = props.projectData?.files?.length ?? '—'
  metrics.value[0].value = String(docCount)

  const textLen = props.projectData?.total_text_length
  if (textLen) metrics.value[1].value = `${(textLen / 1000).toFixed(1)}K chars`
})

function phaseClass(phase) {
  // Phase 0 is always completed (done on Home)
  if (phase === 0) return 'graph-build__phase--completed'
  if (currentPhase.value > phase) return 'graph-build__phase--completed'
  if (currentPhase.value === phase) return 'graph-build__phase--active'
  return 'graph-build__phase--locked'
}

function selectItem(item, type) {
  selectedItem.value = selectedItem.value?.name === item.name
    ? null
    : { ...item, itemType: type }
}

// ── Single real call: POST /api/graph/build ────────────────────────────────
// This is the only backend route that exists for this step.
// It kicks off entity extraction + Neo4j storage as one async job,
// returns a task_id we then poll via GET /api/graph/task/:id

async function startBuild() {
  if (isProcessing.value) return

  const projectId = props.projectData?.project_id
  if (!projectId) {
    phaseError.value = 'No project_id found — did the upload complete successfully?'
    return
  }

  isProcessing.value = true
  phaseError.value = ''
  buildProgress.value = 0
  statusMsg.value = 'Starting graph build…'

  try {
    // ── Step A: kick off the build job ──────────────────────────────────────
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'
    const res = await fetch(`${BASE_URL}/graph/build`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId }),
    })

    const json = await res.json()

    if (!res.ok || !json.success) {
      throw new Error(json.error || `HTTP ${res.status}`)
    }

    const taskId = json.data?.task_id
    if (!taskId) throw new Error('Backend did not return a task_id')

    statusMsg.value = 'Build job queued — polling for progress…'

    // ── Step B: poll task until completed ───────────────────────────────────
    const result = await pollTaskWithProgress(taskId)

    // ── Step C: update UI from result ───────────────────────────────────────
    const graphId    = result?.graph_id   || result?.result?.graph_id    || 'GRF-OK'
    const nodeCount  = result?.node_count ?? result?.result?.node_count  ?? '—'
    const edgeCount  = result?.edge_count ?? result?.result?.edge_count  ?? '—'
    const chunkCount = result?.chunk_count ?? result?.result?.chunk_count ?? '—'

    metrics.value[2].value = graphId

    graphStats.value = [
      { label: 'Nodes Written', value: String(nodeCount)  },
      { label: 'Edges Written', value: String(edgeCount)  },
      { label: 'Text Chunks',   value: String(chunkCount) },
    ]

    graphStorageInfo.value = [
      { label: 'Graph ID',    value: graphId          },
      { label: 'Node Count',  value: String(nodeCount) },
      { label: 'Edge Count',  value: String(edgeCount) },
      { label: 'Storage',     value: 'Neo4j (local)'  },
    ]

    currentPhase.value = 2

  } catch (err) {
    phaseError.value = err.message
  } finally {
    isProcessing.value = false
    statusMsg.value = ''
  }
}

// Polls GET /api/graph/task/:id and updates the progress bar + status message
// in real time from the task's message + progress fields
async function pollTaskWithProgress(taskId, intervalMs = 3000, timeoutMs = 600000) {
  const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'
  const start = Date.now()

  return new Promise((resolve, reject) => {
    const id = setInterval(async () => {
      if (Date.now() - start > timeoutMs) {
        clearInterval(id)
        reject(new Error('Build timed out — check backend logs'))
        return
      }

      try {
        const res  = await fetch(`${BASE_URL}/graph/task/${taskId}`)
        const json = await res.json()
        const task = json.data

        // Update live progress UI
        if (task?.message) statusMsg.value = task.message
        if (typeof task?.progress === 'number') buildProgress.value = task.progress

        if (task?.status === 'completed') {
          clearInterval(id)
          buildProgress.value = 100
          resolve(task.result ?? task)
        }
        if (task?.status === 'failed') {
          clearInterval(id)
          reject(new Error(task.error || task.message || 'Build failed'))
        }
      } catch (e) {
        // network hiccup — keep polling
        console.warn('Poll error (will retry):', e.message)
      }
    }, intervalMs)
  })
}

function proceedToEnv() {
  emit('completed', {
    graph_id: metrics.value[2].value,
    ontology: props.projectData?.ontology ?? { entity_types: [], edge_types: [] },
  })
}
</script>

<style scoped>
.graph-build {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.graph-build__metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.graph-build__metric {
  padding: 1.25rem 1.5rem;
  overflow: hidden;
}

.graph-build__metric-val {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
  margin: 0.25rem 0 0.125rem;
}

.graph-build__metric-sub {
  font-size: 0.6875rem;
  color: var(--text-muted);
}

/* Phase Card */
.graph-build__phase {
  padding: 1.75rem;
  transition: opacity var(--duration-normal);
}

.graph-build__phase--locked {
  opacity: 0.45;
  pointer-events: none;
}

.graph-build__phase--active {
  border-color: rgba(255, 181, 158, 0.25);
  box-shadow: var(--shadow-glow-primary);
}

.graph-build__phase--completed {
  border-color: rgba(134, 239, 172, 0.15);
}

.graph-build__phase-header {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1.25rem;
}

.graph-build__phase-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.graph-build__phase-title-row {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.graph-build__phase-num {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-muted);
  opacity: 0.4;
  line-height: 1;
}

.graph-build__phase-desc {
  color: var(--text-muted);
  font-size: 0.875rem;
  line-height: 1.7;
  max-width: 640px;
}

.graph-build__phase-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Progress bar */
.graph-build__progress {
  margin-bottom: 1.25rem;
}

.graph-build__progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.graph-build__progress-bar {
  width: 100%;
  height: 4px;
  background: var(--surface-container-high);
  border-radius: 2px;
  overflow: hidden;
}

.graph-build__progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-container));
  border-radius: 2px;
  transition: width 0.4s ease;
}

/* Overlay */
.graph-build__overlay {
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.graph-build__overlay-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.graph-build__overlay-desc {
  color: var(--text-secondary);
  font-size: 0.875rem;
  line-height: 1.7;
}

.graph-build__overlay-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.graph-build__attr-list { display: flex; flex-direction: column; gap: 0.375rem; }

.graph-build__attr-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 0.75rem;
  background: var(--surface-container-high);
  border-radius: var(--radius-md);
}

.graph-build__attr-name { font-size: 0.8125rem; color: var(--primary); min-width: 100px; }
.graph-build__attr-desc { font-size: 0.75rem; color: var(--text-muted); flex: 1; }

.graph-build__conn-list { display: flex; flex-direction: column; gap: 0.375rem; }
.graph-build__conn-item { display: flex; align-items: center; gap: 0.625rem; }

/* Tags */
.graph-build__tags-section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 0.75rem;
  transition: opacity var(--duration-normal);
}

.graph-build__tags-section--dimmed { opacity: 0.35; }

.graph-build__tag-list { display: flex; flex-wrap: wrap; gap: 0.375rem; }

.graph-build__tag {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: rgba(255, 90, 31, 0.1);
  color: var(--primary);
  border: 1px solid rgba(255, 90, 31, 0.2);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast);
  font-family: var(--font-body);
}
.graph-build__tag:hover { background: rgba(255, 90, 31, 0.2); border-color: rgba(255, 90, 31, 0.4); }
.graph-build__tag--selected {
  background: rgba(255, 90, 31, 0.25);
  border-color: var(--primary-container);
  box-shadow: 0 0 10px rgba(255, 90, 31, 0.2);
}

.graph-build__tag--relation {
  background: rgba(14, 63, 174, 0.15);
  color: var(--secondary);
  border-color: rgba(182, 196, 255, 0.2);
}
.graph-build__tag--relation:hover {
  background: rgba(14, 63, 174, 0.25);
  border-color: rgba(182, 196, 255, 0.4);
}
.graph-build__tag--relation.graph-build__tag--selected {
  background: rgba(14, 63, 174, 0.3);
  border-color: var(--secondary);
  box-shadow: var(--shadow-glow-ai);
}

/* Stats Grid */
.graph-build__stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.graph-build__stat-val { font-size: 1.5rem; font-weight: 700; color: var(--primary); margin-bottom: 0.25rem; }

/* Info Card */
.graph-build__info-card { margin-bottom: 1.25rem; }

.graph-build__info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--ghost-border);
}
.graph-build__info-row:last-child { border-bottom: none; }
.graph-build__info-label { color: var(--text-muted); }
.graph-build__info-val { color: var(--text-primary); font-size: 0.8125rem; }

/* Error */
.graph-build__error {
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
.graph-build__cta { display: flex; gap: 0.75rem; padding-top: 0.5rem; }

.graph-build__complete {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  background: rgba(134, 239, 172, 0.06);
  border: 1px solid rgba(134, 239, 172, 0.15);
  border-radius: var(--radius-md);
  margin-top: 0.75rem;
}

/* Overlay transition */
.overlay-enter-active, .overlay-leave-active { transition: all 250ms var(--ease-out); }
.overlay-enter-from { opacity: 0; transform: translateY(-8px); }
.overlay-leave-to   { opacity: 0; transform: translateY(4px); }
</style>