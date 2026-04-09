<template>
  <div class="report">
    <!-- Top action bar -->
    <div class="report__topbar">
      <div>
        <div class="step-tag">Step 04 — Report Generation</div>
        <h1 class="display-lg report__title" style="margin-top:.5rem">Prediction Report</h1>
      </div>
      <div class="report__topbar-actions">
        <button class="btn-secondary" @click="downloadReport" :disabled="!isComplete">
          <span class="material-symbols-outlined" style="font-size:16px">download</span>
          Export PDF
        </button>
        <button v-if="isComplete" class="btn-primary" @click="$emit('completed')">
          Open Interaction
          <span class="material-symbols-outlined" style="font-size:18px">chat</span>
        </button>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="errorMsg" class="report__error-banner">
      <span class="material-symbols-outlined" style="font-size:16px">error</span>
      {{ errorMsg }}
      <button class="btn-ghost" style="margin-left:auto;font-size:.75rem" @click="errorMsg=''">Dismiss</button>
    </div>

    <div class="report__split">
      <!-- ── LEFT: Report Document ── -->
      <div class="report__doc card" ref="docRef">
        <!-- Waiting State -->
        <div v-if="!reportOutline && !isGenerating" class="report__waiting">
          <div class="report__waiting-rings">
            <div class="report__ring" style="animation-delay:0ms"></div>
            <div class="report__ring" style="animation-delay:200ms"></div>
            <div class="report__ring" style="animation-delay:400ms"></div>
          </div>
          <span class="report__waiting-text">Waiting for Report Agent…</span>
          <button class="btn-primary" @click="beginReport">
            <span class="material-symbols-outlined" style="font-size:18px">auto_awesome</span>
            Generate Report
          </button>
        </div>

        <!-- Generating state -->
        <div v-else-if="isGenerating && !reportOutline" class="report__waiting">
          <div class="ai-chip">
            <span class="ai-chip-dot"></span>
            <span class="label-sm" style="color:var(--secondary)">{{ generatingMsg || 'Starting Report Agent…' }}</span>
          </div>
          <div v-if="generateProgress > 0" style="width:200px">
            <div class="report__progress-track" style="margin-top:.75rem">
              <div class="report__progress-fill" :style="`width:${generateProgress}%`"></div>
            </div>
            <div class="label-sm" style="color:var(--text-muted);text-align:center;margin-top:.375rem">{{ generateProgress }}%</div>
          </div>
        </div>

        <!-- Report Content -->
        <div v-else-if="reportOutline" class="report__content">
          <!-- Report Header Block -->
          <div class="report__header-block">
            <div class="report__meta-row">
              <span class="chip chip-orange">Prediction Report</span>
              <span class="report__id font-mono label-sm">ID: {{ activeReportId || reportId }}</span>
              <span class="report__date label-sm">{{ reportDate }}</span>
            </div>
            <h2 class="report__main-title font-headline">{{ reportOutline.title }}</h2>
            <p class="report__summary">{{ reportOutline.summary }}</p>
            <div class="section-divider"></div>
          </div>

          <!-- Sections -->
          <div class="report__sections">
            <div
              v-for="(section, idx) in reportOutline.sections"
              :key="idx"
              class="report__section"
              :class="{
                'report__section--active':    currentSectionIdx === idx + 1,
                'report__section--completed': isSectionDone(idx + 1),
                'report__section--pending':   !isSectionDone(idx + 1) && currentSectionIdx !== idx + 1,
              }"
            >
              <div
                class="report__section-header"
                :class="{'report__section-header--clickable': isSectionDone(idx + 1)}"
                @click="isSectionDone(idx + 1) && toggleCollapse(idx)"
              >
                <span class="report__section-num font-mono">{{ String(idx + 1).padStart(2, '0') }}</span>
                <h3 class="report__section-title headline-md">{{ section.title }}</h3>
                <div class="report__section-header-right">
                  <span v-if="isSectionDone(idx + 1)" class="chip chip-green" style="font-size:.6rem">
                    <span class="material-symbols-outlined" style="font-size:11px">check</span>
                  </span>
                  <div v-else-if="currentSectionIdx === idx + 1" class="ai-chip" style="padding:.2rem .625rem">
                    <span class="ai-chip-dot"></span>
                    <span class="label-sm" style="color:var(--secondary)">Writing…</span>
                  </div>
                  <span v-else class="chip chip-muted" style="font-size:.6rem">Pending</span>
                  <span
                    v-if="isSectionDone(idx + 1)"
                    class="material-symbols-outlined report__collapse-icon"
                    :class="{'report__collapse-icon--open': !collapsedSet.has(idx)}"
                  >expand_more</span>
                </div>
              </div>

              <div class="report__section-body" v-show="!collapsedSet.has(idx)">
                <div
                  v-if="generatedSections[idx + 1]"
                  class="report__generated"
                  v-html="renderMarkdown(generatedSections[idx + 1])"
                ></div>
                <div v-else-if="currentSectionIdx === idx + 1" class="report__writing">
                  <div class="report__writing-cursor font-mono">{{ writingPreview }}<span class="report__cursor-blink">|</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── RIGHT: Workflow Timeline ── -->
      <div class="report__timeline card">
        <span class="label-sm" style="color:var(--text-muted);margin-bottom:1.25rem;display:block">Report Workflow</span>

        <div class="report__timeline-list">
          <div
            v-for="(step, i) in timelineSteps"
            :key="i"
            class="report__timeline-item"
            :class="{
              'report__timeline-item--done':    step.status === 'done',
              'report__timeline-item--active':  step.status === 'active',
              'report__timeline-item--pending': step.status === 'pending',
            }"
          >
            <div class="report__timeline-connector" v-if="i > 0"></div>
            <div class="report__timeline-dot">
              <span v-if="step.status === 'done'" class="material-symbols-outlined" style="font-size:14px">check</span>
              <div v-else-if="step.status === 'active'" class="spinner" style="width:12px;height:12px;border-width:1.5px"></div>
              <span v-else class="report__timeline-pending-dot"></span>
            </div>
            <div class="report__timeline-content">
              <div class="report__timeline-title">{{ step.title }}</div>
              <div class="report__timeline-desc label-sm">{{ step.desc }}</div>
              <div v-if="step.status !== 'pending'" class="report__timeline-time label-sm">{{ step.time }}</div>
            </div>
          </div>
        </div>

        <!-- Section Progress -->
        <div v-if="reportOutline" class="report__section-progress">
          <div class="section-divider"></div>
          <span class="label-sm" style="color:var(--text-muted)">Section Progress</span>
          <div class="report__progress-track">
            <div class="report__progress-fill" :style="`width:${sectionProgressPct}%`"></div>
          </div>
          <span class="label-sm" style="color:var(--text-muted)">
            {{ Object.keys(generatedSections).length }} / {{ reportOutline.sections.length }} sections
          </span>
        </div>

        <!-- Agent log live feed -->
        <div v-if="agentLogLines.length" class="report__agentlog card-nested" style="margin-top:1rem">
          <span class="label-sm" style="color:var(--text-muted);display:block;margin-bottom:.5rem">Agent Activity</span>
          <div class="report__agentlog-body">
            <div v-for="(line, i) in agentLogLines.slice(-8)" :key="i" class="report__agentlog-line label-sm">{{ line }}</div>
          </div>
        </div>

        <!-- Tokens used -->
        <div v-if="tokensUsed" class="report__tokens card-nested" style="margin-top:1rem">
          <span class="label-sm" style="color:var(--text-muted)">Tokens Used</span>
          <div class="font-mono" style="color:var(--primary);font-size:1.125rem;font-weight:700">{{ tokensUsed.toLocaleString() }}</div>
          <div class="label-sm" style="color:var(--text-muted)">gemma3:4b (Ollama)</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ─── Props ────────────────────────────────────────────────────────────────────
// simulationId: Required — the sim_xxxx from Step 3
// reportId:     Optional display fallback before API returns real ID
const props = defineProps({
  simulationId: String,
  reportId: { type: String, default: 'REF-PENDING' },
})
const emit = defineEmits(['completed'])

// ─── State ────────────────────────────────────────────────────────────────────
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
const API = (path) => `${BASE_URL}/api${path}`

const docRef          = ref(null)
const isGenerating    = ref(false)
const isComplete      = ref(false)
const reportOutline   = ref(null)
const currentSectionIdx  = ref(0)
const generatedSections  = ref({})
const collapsedSet    = ref(new Set())
const writingPreview  = ref('')
const tokensUsed      = ref(null)
const errorMsg        = ref('')
const activeReportId  = ref(null)      // real report_id from backend
const activeTaskId    = ref(null)      // task_id for polling generate/status
const agentLogLines   = ref([])        // live agent activity lines
const generateProgress = ref(0)
const generatingMsg   = ref('')

// Track how many log lines we've already ingested
const lastAgentLogLine = ref(0)
const lastConsoleLogLine = ref(0)

const reportDate = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })

let statusPollTimer  = null   // polls /generate/status while task pending
let sectionPollTimer = null   // polls /sections while report building
let agentLogTimer    = null   // polls /agent-log for live activity
let progressPollTimer = null  // polls /progress every 2s (catches completion from file)

// ─── Computed ─────────────────────────────────────────────────────────────────
function isSectionDone(idx) { return !!generatedSections.value[idx] }

const sectionProgressPct = computed(() => {
  if (!reportOutline.value) return 0
  return (Object.keys(generatedSections.value).length / reportOutline.value.sections.length) * 100
})

const timelineSteps = computed(() => [
  { title: 'Collect Simulation Data', desc: 'Aggregate action logs',        time: '—',  status: isGenerating.value || reportOutline.value ? 'done' : 'pending' },
  { title: 'Start Report Agent',      desc: 'Query knowledge graph',        time: '—',  status: isGenerating.value ? 'active' : (reportOutline.value ? 'done' : 'pending') },
  { title: 'Generate Section Content',desc: 'AI writes each section',       time: isComplete.value ? 'done' : '…', status: reportOutline.value && !isComplete.value ? 'active' : (isComplete.value ? 'done' : 'pending') },
  { title: 'Render & Format',         desc: 'Apply markdown + styling',     time: isComplete.value ? 'done' : '—', status: isComplete.value ? 'done' : 'pending' },
])

// ─── API helpers ──────────────────────────────────────────────────────────────
async function apiFetch(url, options = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options })
  const json = await res.json().catch(() => ({ error: res.statusText }))
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`)
  return json
}

// ─── Main entry ───────────────────────────────────────────────────────────────
async function beginReport() {
  isGenerating.value  = true
  errorMsg.value      = ''
  generateProgress.value = 0
  generatingMsg.value = 'Submitting report generation task…'

  try {
    // 1. Check if a completed report already exists for this simulation
    if (props.simulationId) {
      const check = await apiFetch(API(`/report/check/${props.simulationId}`))
      if (check.success && check.data.has_report && check.data.report_status === 'completed') {
        // Already done — just load it
        activeReportId.value = check.data.report_id
        await loadExistingReport(check.data.report_id)
        isGenerating.value = false
        return
      }
    }

    // 2. Kick off generation
    generatingMsg.value = 'Starting Report Agent — this may take several minutes on CPU…'
    const resp = await apiFetch(API('/report/generate'), {
      method: 'POST',
      body: JSON.stringify({
        simulation_id: props.simulationId,
        force_regenerate: false,
      }),
    })
    if (!resp.success) throw new Error(resp.error || 'Failed to start report generation')

    activeReportId.value = resp.data.report_id
    activeTaskId.value   = resp.data.task_id

    // If backend says it was already generated, load it directly
    if (resp.data.already_generated) {
      await loadExistingReport(activeReportId.value)
      isGenerating.value = false
      return
    }

    // 3. Poll task status until done
    statusPollTimer = setInterval(pollGenerateStatus, 4000)
    // Also start polling agent log so the user sees live activity
    agentLogTimer = setInterval(pollAgentLog, 3000)
    // Poll /progress every 2s for live file-based status (catches completion faster)
    progressPollTimer = setInterval(pollProgress, 2000)

  } catch (e) {
    errorMsg.value = `Failed to start report: ${e.message}`
    isGenerating.value = false
  }
}

// Poll /generate/status — runs while the background task is processing
async function pollGenerateStatus() {
  try {
    const resp = await apiFetch(API('/report/generate/status'), {
      method: 'POST',
      body: JSON.stringify({
        task_id: activeTaskId.value,
        simulation_id: props.simulationId,
      }),
    })
    if (!resp.success) return
    const d = resp.data

    generateProgress.value = d.progress || 0
    generatingMsg.value = d.message || generatingMsg.value

    if (d.status === 'completed' || d.already_completed) {
      clearInterval(statusPollTimer)
      clearInterval(progressPollTimer)
      statusPollTimer = null
      progressPollTimer = null
      // Always load the report — don't gate on reportOutline being null
      await loadExistingReport(d.report_id || activeReportId.value)
      isGenerating.value = false
    } else if (d.status === 'failed') {
      clearInterval(statusPollTimer)
      clearInterval(progressPollTimer)
      errorMsg.value = `Report generation failed: ${d.message || 'Unknown error'}`
      isGenerating.value = false
    }
  } catch (e) {
    console.warn('pollGenerateStatus error:', e.message)
  }
}

// Load a completed report from the backend into the UI
async function loadExistingReport(reportId) {
  if (!reportId) return
  try {
    const resp = await apiFetch(API(`/report/${reportId}`))
    if (!resp.success) throw new Error(resp.error)
    const r = resp.data

    // Build outline from report data — backend nests sections under outline
    const outlineData = r.outline || r
    reportOutline.value = {
      title:   outlineData.title || r.title || 'Prediction Report',
      summary: outlineData.summary || r.summary || r.executive_summary || '',
      sections: ((outlineData.sections) || r.sections || []).map((s) => ({
        title: typeof s === 'string' ? s : (s.title || s.name || `Section ${s.index || ''}`),
        desc:  typeof s === 'string' ? '' : (s.description || ''),
        index: typeof s === 'object' ? (s.index || 0) : 0,
      })),
    }

    if (!reportOutline.value.sections.length) {
      // Fallback: create placeholder sections so UI renders
      reportOutline.value.sections = [{ title: 'Full Report', desc: '', index: 1 }]
    }

    // Immediate poll first — if already complete this will set isComplete and clear timers
    await pollSections(reportId)
    // Only start the interval if not already complete
    if (!isComplete.value) {
      sectionPollTimer = setInterval(() => pollSections(reportId), 3000)
    }
  } catch (e) {
    errorMsg.value = `Failed to load report: ${e.message}`
  }
}

// Poll /sections — picks up sections as they are written one by one
async function pollSections(reportId) {
  if (!reportId) return
  try {
    const resp = await apiFetch(API(`/report/${reportId}/sections`))
    if (!resp.success) return
    const sections = resp.data.sections || []
    const wasComplete = isComplete.value

    sections.forEach((sec) => {
      // section shape: { filename, content, section_index }
      const idx = sec.section_index || parseInt((sec.filename || '').match(/\d+/)?.[0] || '0')
      if (idx && sec.content && !generatedSections.value[idx]) {
        currentSectionIdx.value = idx
        generatedSections.value = { ...generatedSections.value, [idx]: sec.content }
      }
    })

    if (agentLogLines.value.length) {
      const last = agentLogLines.value[agentLogLines.value.length - 1] || ''
      writingPreview.value = String(last).slice(0, 80)
    }

    const allSectionsLoaded = reportOutline.value &&
      Object.keys(generatedSections.value).length >= reportOutline.value.sections.length

    if (resp.data.is_complete || allSectionsLoaded) {
      clearInterval(sectionPollTimer)
      clearInterval(agentLogTimer)
      clearInterval(progressPollTimer)
      sectionPollTimer = null
      currentSectionIdx.value = 0
      writingPreview.value = ''
      isComplete.value = true
      isGenerating.value = false
      fetchTokenCount(reportId)
      // Do NOT emit('completed') here — the "Open Interaction" button handles navigation
    }
  } catch (e) {
    console.warn('pollSections error:', e.message)
  }
}

// Poll agent log for live activity display in the sidebar
async function pollAgentLog() {
  if (!activeReportId.value) return
  try {
    const resp = await apiFetch(API(`/report/${activeReportId.value}/agent-log?from_line=${lastAgentLogLine.value}`))
    if (!resp.success) return
    const lines = resp.data.lines || resp.data.logs || []
    if (lines.length) {
      lastAgentLogLine.value += lines.length
      agentLogLines.value = [...agentLogLines.value, ...lines].slice(-50)
    }
  } catch (e) { /* silent */ }
}

// Poll /progress every 2s — reads the file-based progress.json which updates in real time
// This catches completion faster than the task-status poll (every 4s)
async function pollProgress() {
  if (!activeReportId.value || isComplete.value) return
  try {
    const resp = await apiFetch(API(`/report/${activeReportId.value}/progress`))
    if (!resp.success) return
    const p = resp.data
    if (p.progress) generateProgress.value = p.progress
    if (p.message) generatingMsg.value = p.message
    // If progress.json says completed and we haven't loaded yet, load immediately
    if (p.status === 'completed' && !isComplete.value) {
      clearInterval(progressPollTimer)
      clearInterval(statusPollTimer)
      progressPollTimer = null
      statusPollTimer = null
      await loadExistingReport(activeReportId.value)
      isGenerating.value = false
    }
  } catch (e) { /* silent */ }
}

async function fetchTokenCount(reportId) {
  try {
    const resp = await apiFetch(API(`/report/${reportId}`))
    if (resp.success && resp.data.tokens_used) {
      tokensUsed.value = resp.data.tokens_used
    }
  } catch (e) { /* optional */ }
}

// ─── Utilities ────────────────────────────────────────────────────────────────
function toggleCollapse(idx) {
  const next = new Set(collapsedSet.value)
  if (next.has(idx)) next.delete(idx)
  else next.add(idx)
  collapsedSet.value = next
}

function renderMarkdown(text) {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^#{1,3} (.+)$/gm, '<h4 class="report-md-h">$1</h4>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^\| (.+) \|$/gm, (m) => {
      const cells = m.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`)
      return `<tr>${cells.join('')}</tr>`
    })
    .replace(/(<tr>.*<\/tr>)/gs, '<table class="report-md-table">$1</table>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/\n/g, ' ')
}

async function downloadReport() {
  if (!activeReportId.value) return
  try {
    const url = API(`/report/${activeReportId.value}/download`)
    window.open(url, '_blank')
  } catch (e) {
    errorMsg.value = `Download failed: ${e.message}`
  }
}

function clearTimers() {
  clearInterval(statusPollTimer)
  clearInterval(sectionPollTimer)
  clearInterval(agentLogTimer)
  clearInterval(progressPollTimer)
}

onUnmounted(clearTimers)
</script>

<style scoped>
.report { display: flex; flex-direction: column; gap: 1.5rem; }

.report__topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.report__title { color: var(--text-primary); margin-top: 0.5rem; }

.report__topbar-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-shrink: 0;
}

.report__error-banner {
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

/* Split */
.report__split {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 1.25rem;
  align-items: start;
}

/* Doc Panel */
.report__doc { min-height: 500px; overflow: hidden; }

.report__waiting {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1.5rem;
  padding: 3rem;
}

.report__waiting-rings { position: relative; width: 60px; height: 60px; }
.report__ring {
  position: absolute;
  inset: 0;
  border: 1.5px solid rgba(182, 196, 255, 0.3);
  border-top-color: var(--secondary);
  border-radius: 50%;
  animation: spin 1.4s linear infinite;
}
.report__ring:nth-child(2) { inset: 8px; border-width: 1px; opacity: .7; }
.report__ring:nth-child(3) { inset: 16px; border-width: 1px; opacity: .4; }
.report__waiting-text { color: var(--text-muted); font-size: 0.875rem; }

/* Content */
.report__content { padding: 2rem; }
.report__header-block { margin-bottom: 1.5rem; }
.report__meta-row { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap; }
.report__id { color: var(--text-muted); }
.report__date { color: var(--text-muted); margin-left: auto; }
.report__main-title { font-size: clamp(1.5rem, 3vw, 2rem); color: var(--text-primary); margin-bottom: 0.875rem; line-height: 1.2; }
.report__summary { color: var(--text-secondary); font-size: 0.9375rem; line-height: 1.75; }

/* Sections */
.report__sections { display: flex; flex-direction: column; gap: 0; }
.report__section { border-bottom: 1px solid var(--ghost-border); transition: background var(--duration-fast); }
.report__section:last-child { border-bottom: none; }
.report__section--active { background: rgba(255,181,158,.03); }
.report__section--pending { opacity: 0.55; }

.report__section-header { display: flex; align-items: center; gap: 1rem; padding: 1.125rem 0; }
.report__section-header--clickable { cursor: pointer; }
.report__section-header--clickable:hover .report__section-title { color: var(--primary); }

.report__section-num { font-size: 1.25rem; font-weight: 700; color: var(--text-muted); opacity: 0.4; min-width: 32px; }
.report__section-title { flex: 1; color: var(--text-primary); font-size: 1rem; transition: color var(--duration-fast); }
.report__section-header-right { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.report__collapse-icon { font-size: 20px; color: var(--text-muted); transition: transform var(--duration-normal) var(--ease-out); transform: rotate(-90deg); }
.report__collapse-icon--open { transform: rotate(0deg); }

/* Section Body */
.report__section-body { padding-bottom: 1.25rem; }
.report__generated { color: var(--text-secondary); font-size: 0.875rem; line-height: 1.8; padding-left: 2.5rem; }
.report__writing { padding-left: 2.5rem; padding-top: 0.5rem; }
.report__writing-cursor { color: var(--text-secondary); font-size: 0.8125rem; line-height: 1.7; white-space: pre-wrap; }
.report__cursor-blink { color: var(--secondary); animation: blink 700ms step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* Timeline */
.report__timeline { padding: 1.5rem; position: sticky; top: 80px; }
.report__timeline-list { display: flex; flex-direction: column; gap: 0; }
.report__timeline-item { display: flex; gap: 0.875rem; position: relative; padding-bottom: 1.25rem; }
.report__timeline-connector { position: absolute; left: 11px; top: -1.25rem; height: 1.25rem; width: 1px; background: var(--ghost-border); }
.report__timeline-dot { width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border: 1px solid var(--ghost-border); background: var(--surface-container); margin-top: 1px; }
.report__timeline-item--done .report__timeline-dot { background: rgba(134,239,172,0.15); border-color: rgba(134,239,172,0.3); color: #86EFAC; }
.report__timeline-item--active .report__timeline-dot { border-color: rgba(182,196,255,.3); box-shadow: var(--shadow-glow-ai); }
.report__timeline-pending-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--surface-container-highest); }
.report__timeline-content { flex: 1; min-width: 0; }
.report__timeline-title { font-size: 0.8125rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.125rem; }
.report__timeline-item--pending .report__timeline-title { color: var(--text-muted); }
.report__timeline-desc { color: var(--text-muted); }
.report__timeline-time { color: var(--primary); margin-top: 0.25rem; }

/* Progress */
.report__section-progress { display: flex; flex-direction: column; gap: 0.5rem; }
.report__progress-track { height: 4px; background: var(--surface-container-high); border-radius: var(--radius-full); overflow: hidden; }
.report__progress-fill { height: 100%; background: var(--gradient-primary); border-radius: var(--radius-full); transition: width 400ms var(--ease-out); }

/* Agent log sidebar */
.report__agentlog { padding: .625rem .75rem; }
.report__agentlog-body { display: flex; flex-direction: column; gap: .25rem; max-height: 120px; overflow-y: auto; }
.report__agentlog-line { color: var(--text-muted); font-size: .625rem; font-family: var(--font-mono); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.report__tokens { text-align: center; }

/* Markdown rendered content */
:deep(.report__generated strong) { color: var(--text-primary); font-weight: 700; }
:deep(.report__generated code) { font-family: var(--font-mono); font-size: 0.8em; background: var(--surface-container-high); padding: 0 4px; border-radius: 3px; color: var(--secondary); }
:deep(.report__generated ul) { padding-left: 1.25rem; margin: 0.5rem 0; }
:deep(.report__generated li) { margin-bottom: 0.25rem; }
:deep(.report__generated table) { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: .8125rem; }
:deep(.report__generated td) { padding: 0.375rem 0.625rem; border: 1px solid var(--ghost-border); color: var(--text-secondary); }
:deep(.report__generated tr:first-child td) { background: var(--surface-container-high); color: var(--text-primary); font-weight: 600; }
:deep(.report-md-h) { font-family: var(--font-headline); color: var(--text-primary); font-size: .9375rem; margin: .75rem 0 .375rem; }

@media (max-width: 1100px) {
  .report__split { grid-template-columns: 1fr; }
}
</style>