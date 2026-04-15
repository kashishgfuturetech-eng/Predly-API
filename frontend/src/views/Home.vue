<template>
  <div class="landing">
    <!-- Background grid -->
    <div class="landing__grid-bg"></div>
    <!-- Orbs -->
    <div class="landing__orb landing__orb--orange"></div>
    <div class="landing__orb landing__orb--blue"></div>
    <div class="landing__orb landing__orb--center"></div>

    <!-- Top bar -->
    <header class="landing__topbar">
      <div class="landing__topbar-inner">
        <div class="landing__logo font-headline">
          <span class="landing__logo-dot"></span>Predly
        </div>
        <div class="landing__status-badge">
          <span class="landing__status-dot"></span>
          <span class="font-mono" style="font-size:0.6875rem;letter-spacing:0.1em;color:var(--text-muted)">ENGINE STATUS: V2.4 ACTIVE</span>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <main class="landing__main">
      <section class="landing__hero">

        <div class="landing__engine-tag animate-fade-up" style="animation-delay:0ms">
          <span class="landing__engine-dot"></span>
          <span class="font-mono" style="font-size:0.6875rem;letter-spacing:0.12em">ENGINE STATUS: V2.4 ACTIVE</span>
        </div>

        <h1 class="landing__headline animate-fade-up" style="animation-delay:80ms">Predly</h1>
        <h2 class="landing__subheadline animate-fade-up" style="animation-delay:140ms">Predict What Happens Next.</h2>

        <p class="landing__desc animate-fade-up" style="animation-delay:200ms">
          Architectural Multi-Agent Systems designed for predictive logic and local context simulation.
        </p>

        <!-- Drop Zone -->
        <div
          class="landing__dropzone animate-fade-up"
          style="animation-delay:280ms"
          @dragover.prevent="dragging = true"
          @dragleave="dragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
          :class="{ 'landing__dropzone--drag': dragging, 'landing__dropzone--filled': files.length }"
        >
          <input ref="fileInput" type="file" multiple accept=".pdf,.md,.txt,.json,.xlsx" style="display:none" @change="handleFileSelect" />

          <div v-if="!files.length" class="landing__drop-empty">
            <div class="landing__drop-icon">
              <span class="material-symbols-outlined" style="font-size:26px">upload_file</span>
            </div>
            <div class="landing__drop-title">Drop Reality Seeds</div>
            <div class="landing__drop-hint">PDF, MD, i Xi , or JSON sources for local context extraction</div>
            <div class="landing__drop-tags">
              <span class="landing__drop-tag font-mono">context.pdf</span>
              <span class="landing__drop-tag font-mono">logic_branch.json</span>
              <span class="landing__drop-tag font-mono">manifesto.md</span>
            </div>
          </div>

          <div v-else class="landing__file-list">
            <div v-for="(f, i) in files" :key="i" class="landing__file-item">
              <span class="material-symbols-outlined" style="font-size:14px;color:var(--secondary)">description</span>
              <span class="landing__file-name font-mono">{{ f.name }}</span>
              <span class="landing__file-size">{{ formatSize(f.size) }}</span>
              <button class="landing__file-remove" @click.stop="removeFile(i)">
                <span class="material-symbols-outlined" style="font-size:14px">close</span>
              </button>
            </div>
            <button class="landing__add-more" @click.stop="triggerFileInput">
              <span class="material-symbols-outlined" style="font-size:13px">add</span> Add more files
            </button>
          </div>
        </div>

        <!-- Error -->
        <div v-if="errorMsg" class="landing__error animate-fade-up">
          <span class="material-symbols-outlined" style="font-size:14px">error_outline</span>
          {{ errorMsg }}
        </div>

        <!-- CTA -->
        <button
          class="landing__cta animate-fade-up"
          style="animation-delay:360ms"
          :disabled="!canStart || isLoading"
          @click="goToPrompt"
        >
          <span v-if="isLoading" class="landing__cta-row">
            <span class="landing__spinner"></span>{{ loadingMsg }}
          </span>
          <span v-else class="landing__cta-row">
            Start Predicting
            <span class="material-symbols-outlined" style="font-size:18px">bolt</span>
          </span>
        </button>

      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref(null)

const files = ref([])
const dragging = ref(false)
const isLoading = ref(false)
const errorMsg = ref('')
const loadingMsg = ref('Processing…')

const canStart = computed(() => files.value.length > 0)

function triggerFileInput() {
  if (!isLoading.value) fileInput.value?.click()
}

function handleFileSelect(e) {
  files.value = [...files.value, ...Array.from(e.target.files)]
}

function handleDrop(e) {
  if (isLoading.value) return
  dragging.value = false
  const dropped = Array.from(e.dataTransfer.files).filter(f =>
    ['.pdf', '.md', '.txt', '.json', '.xlsx'].some(ext => f.name.toLowerCase().endsWith(ext))
  )
  files.value = [...files.value, ...dropped]
}

function removeFile(i) {
  if (!isLoading.value) files.value.splice(i, 1)
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes}B`
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)}KB`
  return `${(bytes / 1048576).toFixed(1)}MB`
}

function goToPrompt() {
  if (!canStart.value || isLoading.value) return
  // Store files globally so PromptView can access them
  window.__predlyPendingFiles = files.value
  router.push({ name: 'Prompt' })
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: #0a0c0f;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* Grid background */
.landing__grid-bg {
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
.landing__orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.landing__orb--orange {
  width: 700px; height: 700px;
  top: -280px; right: -180px;
  background: radial-gradient(circle, rgba(255, 90, 31, 0.35) 0%, transparent 70%);
}
.landing__orb--blue {
  width: 600px; height: 600px;
  bottom: -180px; left: -180px;
  background: radial-gradient(circle, rgba(14, 63, 174, 0.3) 0%, transparent 70%);
}
.landing__orb--center {
  width: 500px; height: 500px;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255, 181, 158, 0.04) 0%, transparent 70%);
}

/* Top bar */
.landing__topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 1.125rem 2rem;
}
.landing__topbar-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.landing__logo {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.landing__logo-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--primary-container);
}
.landing__status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(16, 20, 25, 0.85);
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: 999px;
  padding: 0.375rem 0.875rem;
  backdrop-filter: blur(10px);
}
.landing__status-dot {
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

/* Main */
.landing__main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 1.5rem 4rem;
  position: relative;
  z-index: 1;
  width: 100%;
}

/* Hero */
.landing__hero {
  max-width: 620px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.25rem;
}

/* Engine tag */
.landing__engine-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(16, 20, 25, 0.9);
  border: 1px solid rgba(171, 137, 127, 0.22);
  border-radius: 999px;
  padding: 0.375rem 0.875rem;
  color: var(--text-muted);
  backdrop-filter: blur(8px);
}
.landing__engine-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--primary-container);
  box-shadow: 0 0 6px var(--primary-container);
}

/* Headline */
.landing__headline {
  font-family: var(--font-headline);
  font-size: clamp(4.5rem, 12vw, 7rem);
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.03em;
  margin: 0;
  text-shadow: 0 0 100px rgba(255, 181, 158, 0.12);
}
.landing__subheadline {
  font-family: var(--font-headline);
  font-size: clamp(1.625rem, 4vw, 2.375rem);
  font-weight: 700;
  background: linear-gradient(135deg, #FFB59E 0%, #FF5A1F 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
}
.landing__desc {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  line-height: 1.75;
  max-width: 460px;
  margin: 0;
}

/* Drop zone */
.landing__dropzone {
  width: 100%;
  background: rgba(16, 20, 25, 0.55);
  border: 1.5px dashed rgba(171, 137, 127, 0.22);
  border-radius: var(--radius-xl);
  padding: 2.5rem 2rem;
  cursor: pointer;
  transition: all 0.25s ease;
  backdrop-filter: blur(14px);
  min-height: 190px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.landing__dropzone::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 50%, rgba(255, 90, 31, 0.03) 0%, transparent 70%);
  pointer-events: none;
}
.landing__dropzone:hover,
.landing__dropzone--drag {
  border-color: rgba(255, 90, 31, 0.45);
  background: rgba(255, 90, 31, 0.03);
  box-shadow: 0 0 40px rgba(255, 90, 31, 0.07);
}
.landing__dropzone--filled {
  align-items: flex-start;
  border-style: solid;
  border-color: rgba(171, 137, 127, 0.18);
  padding: 1.25rem 1.5rem;
}

.landing__drop-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
.landing__drop-icon {
  width: 52px; height: 52px;
  border-radius: var(--radius-lg);
  background: rgba(255, 90, 31, 0.1);
  border: 1px solid rgba(255, 90, 31, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-container);
}
.landing__drop-title {
  font-weight: 700;
  font-size: 0.9375rem;
  color: var(--text-primary);
}
.landing__drop-hint {
  font-size: 0.8125rem;
  color: var(--text-muted);
}
.landing__drop-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0.25rem;
}
.landing__drop-tag {
  font-size: 0.6875rem;
  color: rgba(154, 164, 178, 0.6);
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: var(--radius-sm);
  padding: 0.25rem 0.625rem;
  background: rgba(255,255,255,0.02);
}

.landing__file-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.landing__file-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255,255,255,0.03);
  border-radius: var(--radius-md);
  border: 1px solid rgba(171,137,127,0.1);
}
.landing__file-name {
  flex: 1;
  font-size: 0.8125rem;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.landing__file-size {
  color: var(--text-muted);
  font-size: 0.6875rem;
  font-family: var(--font-mono);
  flex-shrink: 0;
}
.landing__file-remove {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 0.125rem;
  display: flex;
  align-items: center;
  border-radius: var(--radius-sm);
  transition: color 0.15s;
}
.landing__file-remove:hover { color: #f87171; }
.landing__add-more {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-md);
  transition: color 0.15s;
}
.landing__add-more:hover { color: var(--primary); }

/* CTA */
.landing__cta {
  width: 100%;
  padding: 1rem 1.75rem;
  background: linear-gradient(135deg, #FF5A1F 0%, #FF8C5A 100%);
  border: none;
  border-radius: var(--radius-lg);
  color: white;
  font-family: var(--font-headline);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.35);
  letter-spacing: 0.01em;
}
.landing__cta:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 30px rgba(255, 90, 31, 0.45);
}
.landing__cta:disabled {
  background: var(--surface-container-high);
  color: var(--text-muted);
  box-shadow: none;
  cursor: not-allowed;
}
.landing__cta-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.landing__spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Error */
.landing__error {
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

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.55s cubic-bezier(0.4,0,0.2,1) both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .landing__headline { font-size: 3.5rem; }
  .landing__subheadline { font-size: 1.4rem; }
  .landing__drop-tags { display: none; }
}
</style>
