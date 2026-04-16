<template>
  <div class="prompt-view">
    <!-- Background -->
    <div class="prompt-view__grid-bg"></div>
    <div class="prompt-view__orb prompt-view__orb--orange"></div>
    <div class="prompt-view__orb prompt-view__orb--blue"></div>

    <!-- Top bar -->
    <header class="prompt-view__topbar">
      <div class="prompt-view__topbar-inner">
        <button class="prompt-view__back" @click="goBack">
          <span class="material-symbols-outlined" style="font-size:18px">arrow_back</span>
          Back
        </button>
        <div class="prompt-view__logo font-headline">
          <span class="prompt-view__logo-dot"></span>Predly
        </div>
        <div class="prompt-view__files-badge" v-if="pendingFiles.length">
          <span class="material-symbols-outlined" style="font-size:13px">description</span>
          {{ pendingFiles.length }} file{{ pendingFiles.length !== 1 ? 's' : '' }} ready
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="prompt-view__main">

      <!-- File pills -->
      <div v-if="pendingFiles.length" class="prompt-view__file-pills animate-fade-up" style="animation-delay:0ms">
        <div class="prompt-view__file-pill" v-for="(f, i) in pendingFiles" :key="i">
          <span class="material-symbols-outlined" style="font-size:12px;color:var(--secondary)">attach_file</span>
          <span class="font-mono" style="font-size:0.6875rem">{{ f.name }}</span>
        </div>
      </div>

      <!-- Prompt card -->
      <div class="prompt-view__card animate-fade-up" style="animation-delay:80ms">

        <!-- Card header -->
        <div class="prompt-view__card-header">
          <div class="prompt-view__card-icon">
            <span class="material-symbols-outlined" style="font-size:20px">auto_awesome</span>
          </div>
          <div class="prompt-view__card-title-group">
            <h2 class="prompt-view__card-title font-headline">AI Prompt Generator</h2>
            <span class="prompt-view__card-sub label-sm">Describe what you want to predict or simulate</span>
          </div>
          <button class="prompt-view__close-hint" @click="goBack" title="Back to upload">
            <span class="material-symbols-outlined" style="font-size:18px">close</span>
          </button>
        </div>

        <!-- Divider -->
        <div class="prompt-view__divider"></div>

        <!-- Textarea -->
        <div class="prompt-view__textarea-wrap">
          <textarea
            v-model="prompt"
            class="prompt-view__textarea font-body"
            placeholder="Describe what you want to create..."
            :disabled="isLoading"
            @input="errorMsg = ''"
          ></textarea>

          <!-- AI-generated prompt indicator -->
          <div v-if="isGenerating" class="prompt-view__generating-badge">
            <span class="prompt-view__gen-spinner"></span>
            <span class="font-mono" style="font-size:0.625rem;color:var(--text-muted)">AI generating…</span>
          </div>
        </div>

        <!-- Suggestion chips -->
        <div class="prompt-view__chips-row">
          <button
            v-for="chip in suggestionChips"
            :key="chip"
            class="prompt-view__chip"
            @click="appendChip(chip)"
            :disabled="isLoading || isGenerating"
          >
            {{ chip }}
          </button>
        </div>

        <!-- Divider -->
        <div class="prompt-view__divider"></div>

        <!-- Bottom bar -->
        <div class="prompt-view__bottom-bar">
          <div class="prompt-view__bottom-left">
            <!-- Generate prompt by AI button -->
            <button
              class="prompt-view__ai-btn"
              @click="generateAIPrompt"
              :disabled="isLoading || isGenerating || !pendingFiles.length"
              :title="!pendingFiles.length ? 'Upload files first to generate AI prompt' : 'Generate a prompt based on your documents'"
            >
              <span v-if="isGenerating" class="prompt-view__gen-spinner prompt-view__gen-spinner--btn"></span>
              <span v-else class="material-symbols-outlined" style="font-size:16px">auto_awesome</span>
              <span>{{ isGenerating ? 'Generating…' : 'Generate with AI' }}</span>
            </button>

            <button class="prompt-view__ref-btn" @click="triggerRefFile" :disabled="isLoading">
              <span class="material-symbols-outlined" style="font-size:15px">attach_file</span>
              Add Reference
            </button>
            <input ref="refInput" type="file" multiple accept=".pdf,.md,.txt,.json" style="display:none" @change="addRefFile" />
          </div>

          <button
            class="prompt-view__generate-btn"
            :disabled="!canSubmit || isLoading"
            @click="submitPrompt"
          >
            <span v-if="isLoading" class="prompt-view__btn-row">
              <span class="prompt-view__spinner"></span>{{ loadingMsg }}
            </span>
            <span v-else class="prompt-view__btn-row">
              Generate
              <span class="material-symbols-outlined" style="font-size:16px">bolt</span>
            </span>
          </button>
        </div>
      </div>

      <!-- Error -->
      <div v-if="errorMsg" class="prompt-view__error animate-fade-up">
        <span class="material-symbols-outlined" style="font-size:14px">error_outline</span>
        {{ errorMsg }}
      </div>

      <!-- Log stream -->
      <div v-if="isLoading && logLines.length" class="prompt-view__log animate-fade-up">
        <div class="prompt-view__log-header label-sm">
          <span class="prompt-view__log-pulse"></span>Engine Log
        </div>
        <div class="prompt-view__log-body" ref="logBody">
          <div v-for="(line, i) in logLines" :key="i" class="prompt-view__log-line font-mono">
            <span class="prompt-view__log-ts">{{ line.ts }}</span>
            <span :class="line.type === 'error' ? 'prompt-view__log-err' : ''">{{ line.msg }}</span>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { uploadProject } from '../api.js'

const router = useRouter()
const logBody = ref(null)
const refInput = ref(null)

const pendingFiles = ref([])
const prompt = ref('')
const isLoading = ref(false)
const isGenerating = ref(false)
const errorMsg = ref('')
const loadingMsg = ref('Uploading…')
const logLines = ref([])

const suggestionChips = [
  'Modern skyscraper',
  'Cinematic lighting',
  'Photorealistic texture',
  'Brutalist concrete',
  'Public opinion shift',
  'Social media cascade',
]

const canSubmit = computed(() => prompt.value.trim().length >= 5)

onMounted(() => {
  // Retrieve files passed from Home.vue
  if (window.__predlyPendingFiles?.length) {
    pendingFiles.value = [...window.__predlyPendingFiles]
  }
})

function goBack() {
  router.push({ name: 'Home' })
}

function appendChip(chip) {
  if (prompt.value && !prompt.value.endsWith(' ')) prompt.value += ', '
  prompt.value += chip
}

function triggerRefFile() {
  refInput.value?.click()
}

function addRefFile(e) {
  const newFiles = Array.from(e.target.files)
  pendingFiles.value = [...pendingFiles.value, ...newFiles]
  // Update global store too
  window.__predlyPendingFiles = pendingFiles.value
}

function addLog(msg, type = 'info') {
  const now = new Date()
  const ts = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}`
  logLines.value.push({ ts, msg, type })
  nextTick(() => {
    if (logBody.value) logBody.value.scrollTop = logBody.value.scrollHeight
  })
}

/**
 * Generate a simulation prompt using the backend LLM based on uploaded documents.
 * Sends files as multipart so the backend can extract real text content.
 */
async function generateAIPrompt() {
  if (isGenerating.value || !pendingFiles.value.length) return

  isGenerating.value = true
  errorMsg.value = ''

  try {
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:10000/api'

    const form = new FormData()
    // Include all files so the backend can extract actual text
    pendingFiles.value.forEach(f => form.append('files', f))
    // Also send names as fallback in case a file type can't be parsed
    form.append('file_names', pendingFiles.value.map(f => f.name).join(','))

    const response = await fetch(`${BASE_URL}/graph/prompt/generate`, {
      method: 'POST',
      body: form,
    })

    const data = await response.json()
    if (!response.ok || !data.success) throw new Error(data.error || 'AI generation failed')

    const generated = data.data?.prompt || ''
    if (generated) {
      prompt.value = generated.trim()
    } else {
      throw new Error('No response from AI')
    }
  } catch (e) {
    errorMsg.value = `AI generation error: ${e.message}`
  } finally {
    isGenerating.value = false
  }
}

async function submitPrompt() {
  if (!canSubmit.value || isLoading.value) return

  isLoading.value = true
  errorMsg.value = ''
  logLines.value = []

  try {
    loadingMsg.value = 'Uploading files…'
    addLog(`Uploading ${pendingFiles.value.length} file(s)…`)

    const uploadResult = await uploadProject(pendingFiles.value, prompt.value)

    if (!uploadResult.success) throw new Error(uploadResult.error || 'Upload failed')

    const projectId = uploadResult.data?.project_id
    if (!projectId) throw new Error('Backend did not return a project_id')

    addLog(`Project created — ID: ${projectId}`)
    loadingMsg.value = 'Ontology generated — loading workspace…'
    addLog('Ontology generation complete ✓')
    addLog('Redirecting to workspace…')

    // Clear global file store
    window.__predlyPendingFiles = null

    await router.push({ name: 'Main', params: { projectId } })
  } catch (e) {
    errorMsg.value = e.message
    addLog(e.message, 'error')
  } finally {
    isLoading.value = false
    loadingMsg.value = 'Uploading…'
  }
}
</script>

<style scoped>
.prompt-view {
  min-height: 100vh;
  background: #0a0c0f;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow-x: hidden;
}

/* Grid */
.prompt-view__grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 181, 158, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 181, 158, 0.025) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* Orbs */
.prompt-view__orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.prompt-view__orb--orange {
  width: 600px; height: 600px;
  top: -250px; right: -150px;
  background: radial-gradient(circle, rgba(255, 90, 31, 0.28) 0%, transparent 70%);
}
.prompt-view__orb--blue {
  width: 500px; height: 500px;
  bottom: -150px; left: -150px;
  background: radial-gradient(circle, rgba(14, 63, 174, 0.25) 0%, transparent 70%);
}

/* Top bar */
.prompt-view__topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 1rem 2rem;
}
.prompt-view__topbar-inner {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.prompt-view__back {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: none;
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: 999px;
  padding: 0.375rem 0.875rem;
  color: var(--text-muted);
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.15s;
  backdrop-filter: blur(8px);
  background: rgba(16, 20, 25, 0.7);
}
.prompt-view__back:hover {
  color: var(--text-primary);
  border-color: rgba(171, 137, 127, 0.35);
}
.prompt-view__logo {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.prompt-view__logo-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--primary-container);
}
.prompt-view__files-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: rgba(14, 63, 174, 0.15);
  border: 1px solid rgba(14, 63, 174, 0.3);
  border-radius: 999px;
  padding: 0.375rem 0.875rem;
  font-size: 0.6875rem;
  color: var(--secondary);
  backdrop-filter: blur(8px);
}

/* Main */
.prompt-view__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 1.5rem 4rem;
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  gap: 1rem;
}

/* File pills */
.prompt-view__file-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  width: 100%;
}
.prompt-view__file-pill {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: rgba(14, 63, 174, 0.1);
  border: 1px solid rgba(14, 63, 174, 0.2);
  border-radius: var(--radius-full);
  padding: 0.3rem 0.75rem;
  color: var(--text-secondary);
}

/* Card */
.prompt-view__card {
  width: 100%;
  background: rgba(18, 22, 28, 0.85);
  border: 1px solid rgba(171, 137, 127, 0.15);
  border-radius: var(--radius-xl);
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 181, 158, 0.03);
}

/* Card header */
.prompt-view__card-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.25rem 1.5rem;
}
.prompt-view__card-icon {
  width: 40px; height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #FF5A1F, #FF8C5A);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(255, 90, 31, 0.3);
}
.prompt-view__card-title-group { flex: 1; }
.prompt-view__card-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.125rem;
}
.prompt-view__card-sub { color: var(--text-muted); }
.prompt-view__close-hint {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 0.25rem;
  display: flex;
  align-items: center;
  border-radius: var(--radius-sm);
  transition: color 0.15s;
  flex-shrink: 0;
}
.prompt-view__close-hint:hover { color: var(--text-secondary); }

.prompt-view__divider {
  height: 1px;
  background: rgba(171, 137, 127, 0.1);
}

/* Textarea */
.prompt-view__textarea-wrap {
  position: relative;
  padding: 1.25rem 1.5rem 0.75rem;
}
.prompt-view__textarea {
  width: 100%;
  min-height: 180px;
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: var(--radius-md);
  padding: 1rem 1.125rem;
  color: var(--text-primary);
  font-size: 0.9375rem;
  line-height: 1.7;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.prompt-view__textarea::placeholder { color: var(--text-muted); }
.prompt-view__textarea:focus {
  border-color: rgba(255, 90, 31, 0.3);
  background: rgba(255, 90, 31, 0.02);
}
.prompt-view__textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.prompt-view__generating-badge {
  position: absolute;
  bottom: 1.5rem;
  right: 2.125rem;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: rgba(16, 20, 25, 0.9);
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: 999px;
  padding: 0.25rem 0.625rem;
  backdrop-filter: blur(8px);
}

/* Chips */
.prompt-view__chips-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding: 0 1.5rem 1rem;
}
.prompt-view__chip {
  font-size: 0.75rem;
  color: var(--text-muted);
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: 999px;
  padding: 0.3rem 0.75rem;
  cursor: pointer;
  transition: all 0.15s;
  font-family: var(--font-body);
}
.prompt-view__chip:hover:not(:disabled) {
  border-color: rgba(255, 90, 31, 0.3);
  color: var(--primary);
  background: rgba(255, 90, 31, 0.05);
}
.prompt-view__chip:disabled { opacity: 0.5; cursor: not-allowed; }

/* Bottom bar */
.prompt-view__bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.5rem;
  flex-wrap: wrap;
}

.prompt-view__bottom-left {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  flex-wrap: wrap;
}

/* AI generate button */
.prompt-view__ai-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 90, 31, 0.08);
  border: 1px solid rgba(255, 90, 31, 0.22);
  border-radius: var(--radius-md);
  padding: 0.5rem 0.875rem;
  color: var(--primary);
  font-size: 0.8125rem;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.15s;
}
.prompt-view__ai-btn:hover:not(:disabled) {
  background: rgba(255, 90, 31, 0.14);
  border-color: rgba(255, 90, 31, 0.35);
}
.prompt-view__ai-btn:disabled { opacity: 0.45; cursor: not-allowed; }

/* Ref button */
.prompt-view__ref-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 0.8125rem;
  cursor: pointer;
  padding: 0.5rem 0.625rem;
  border-radius: var(--radius-md);
  transition: color 0.15s;
  font-family: var(--font-body);
}
.prompt-view__ref-btn:hover:not(:disabled) { color: var(--text-secondary); }
.prompt-view__ref-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Generate button */
.prompt-view__generate-btn {
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #FF5A1F 0%, #FF8C5A 100%);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-family: var(--font-headline);
  font-size: 0.9375rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(255, 90, 31, 0.3);
  white-space: nowrap;
}
.prompt-view__generate-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(255, 90, 31, 0.4);
}
.prompt-view__generate-btn:disabled {
  background: var(--surface-container-high);
  color: var(--text-muted);
  box-shadow: none;
  cursor: not-allowed;
  transform: none;
}
.prompt-view__btn-row {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

/* Spinners */
.prompt-view__spinner {
  width: 13px; height: 13px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.prompt-view__gen-spinner {
  width: 11px; height: 11px;
  border: 1.5px solid rgba(255, 181, 158, 0.3);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.prompt-view__gen-spinner--btn {
  border-top-color: var(--primary-container);
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Error */
.prompt-view__error {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(239, 68, 68, 0.07);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius-md);
  color: #f87171;
  font-size: 0.8125rem;
}

/* Log */
.prompt-view__log {
  width: 100%;
  background: rgba(10, 12, 15, 0.8);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.prompt-view__log-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(171, 137, 127, 0.1);
  color: var(--text-muted);
  letter-spacing: 0.08em;
}
.prompt-view__log-pulse {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--primary-container);
  animation: pulse-p 1s ease-in-out infinite;
}
@keyframes pulse-p {
  0%,100% { opacity: 1; }
  50%      { opacity: 0.4; }
}
.prompt-view__log-body {
  max-height: 100px;
  overflow-y: auto;
  padding: 0.5rem 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.prompt-view__log-line {
  display: flex;
  gap: 0.75rem;
  font-size: 0.6875rem;
  line-height: 1.5;
  color: var(--text-secondary);
}
.prompt-view__log-ts { color: var(--text-muted); flex-shrink: 0; opacity: 0.6; }
.prompt-view__log-err { color: #f87171; }

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.55s cubic-bezier(0.4,0,0.2,1) both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .prompt-view__bottom-bar { flex-direction: column; align-items: stretch; }
  .prompt-view__generate-btn { width: 100%; justify-content: center; }
}
</style>
