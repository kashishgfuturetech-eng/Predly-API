<template>
  <div class="main-view">
    <!-- Step 1 — Graph Build gets its own full-screen 3-column shell -->
    <Step1GraphBuild
      v-if="currentStep === 'graph'"
      :project-data="projectData"
      @completed="onStepCompleted('graph', $event)"
    />

    <!-- Steps 2-5 use the standard TopNav + SideNav + padded content layout -->
    <template v-else>
      <TopNav show-links :project-id="projectId" active-step="Graph Build" />
      <SideNav :current-step="currentStep" :completed-steps="completedSteps" @navigate="navigateTo" />

      <div ref="contentRef" class="main-view__content">
        <!-- Page Header -->
        <header class="main-view__header">
          <div class="main-view__breadcrumb">
            <span class="step-tag">Step 0{{ stepIndex + 1 }}</span>
            <span class="main-view__breadcrumb-sep">—</span>
            <span class="label-sm" style="color:var(--text-muted)">{{ stepTitles[currentStep] }}</span>
          </div>
          <h1 class="display-lg main-view__title">{{ stepHeadings[currentStep] }}</h1>
          <p class="main-view__subtitle">{{ stepSubtitles[currentStep] }}</p>
        </header>

        <!-- Step Components -->
        <transition name="step" mode="out-in">
          <!-- Step 2: Env Setup -->
          <Step2EnvSetup
            v-if="currentStep === 'env'"
            :project-data="projectData"
            @completed="onStepCompleted('env', $event)"
          />

          <Step3Simulation
            v-else-if="currentStep === 'simulation'"
            :simulation-id="projectData.simulation_id || null"
            :project-id="projectData.project_id"
            :max-rounds="projectData.max_rounds"
            :auto-mode="globalAutoMode"
            @completed="onStepCompleted('simulation', {})"
          />

          <Step4Report
            v-else-if="currentStep === 'report'"
            :simulation-id="projectData.simulation_id || null"
            :report-id="projectData.report_id || 'REF-PENDING'"
            :auto-mode="globalAutoMode"
            @completed="onStepCompleted('report', $event)"
          />

          <Step5Interaction
            v-else-if="currentStep === 'interaction'"
            :report-id="projectData.report_id || 'REF-PENDING'"
            :simulation-id="projectData.simulation_id || null"
          />

          <div v-else class="main-view__placeholder">
            <span class="material-symbols-outlined" style="font-size:48px;color:var(--text-muted)">account_tree</span>
            <p class="main-view__placeholder-text">Select a step from the sidebar to begin</p>
          </div>
        </transition>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import TopNav from '../components/TopNav.vue'
import SideNav from '../components/SideNav.vue'
import Step1GraphBuild from '../components/Step1GraphBuild.vue'
import Step2EnvSetup from '../components/Step2EnvSetup.vue'
import Step3Simulation from '../components/Step3Simulation.vue'
import Step4Report from '../components/Step4Report.vue'
import Step5Interaction from '../components/Step5Interaction.vue'
import { generateOntology } from '../api.js'

const props = defineProps({ projectId: String })
const router = useRouter()

const currentStep = ref('graph')
const completedSteps = ref([])
const globalAutoMode = ref(false)
const contentRef = ref(null)

// Auto-scroll content area to top whenever the active step changes in auto mode
watch(currentStep, () => {
  if (!globalAutoMode.value) return
  nextTick(() => {
    if (contentRef.value) contentRef.value.scrollTo({ top: 0, behavior: 'smooth' })
    else window.scrollTo({ top: 0, behavior: 'smooth' })
  })
})

const projectData = ref({
  project_id:    props.projectId || null,
  graph_id:      null,
  simulation_id: null,
  report_id:     null,
  ontology:      null,
  max_rounds:    10,
  autoMode:      false,
})

const stepOrder = ['graph', 'env', 'simulation', 'report', 'interaction']
const stepIndex = computed(() => stepOrder.indexOf(currentStep.value))

const stepTitles = {
  graph:       'Graph Build & Ontology',
  env:         'Environment Configuration',
  simulation:  'Simulation Run',
  report:      'Report Generation',
  interaction: 'AI Interaction',
}
const stepHeadings = {
  graph:       'Graph Build',
  env:         'Env Setup',
  simulation:  'Simulation',
  report:      'Report',
  interaction: 'Interaction',
}
const stepSubtitles = {
  graph:       'Extract ontology structures, entity types, and relationships from your reality seeds.',
  env:         'Define simulation parameters, agent personas, and recommendation logic.',
  simulation:  'Launch parallel autonomous agents across Info Plaza and Topic Community.',
  report:      'Generate AI-powered predictive intelligence from simulation data.',
  interaction: 'Query the Simulation Oracle to explore agent behaviors, emergent patterns, and hypothetical scenarios.',
}

function navigateTo(step) {
  if (
    step === currentStep.value ||
    completedSteps.value.includes(step) ||
    stepOrder.indexOf(step) <= stepOrder.indexOf(currentStep.value) + 1
  ) {
    currentStep.value = step
  }
}

function onStepCompleted(step, data) {
  if (!completedSteps.value.includes(step)) completedSteps.value.push(step)
  if (data) {
    if (data.autoMode !== undefined) globalAutoMode.value = data.autoMode
    Object.assign(projectData.value, data)
    projectData.value.autoMode = globalAutoMode.value
  }
  const next = stepOrder[stepOrder.indexOf(step) + 1]
  if (next) currentStep.value = next
}

onMounted(async () => {
  currentStep.value = 'graph'
  if (props.projectId) {
    try {
      const result = await generateOntology(props.projectId)
      const data = result?.data ?? result
      if (data?.ontology)  projectData.value.ontology  = data.ontology
      if (data?.files)     projectData.value.files     = data.files
      if (data?.graph_id)  projectData.value.graph_id  = data.graph_id
    } catch (e) {
      console.warn('Could not load project data:', e.message)
    }
  }
})
</script>

<style scoped>
.main-view {
  min-height: 100vh;
  background: var(--surface);
}

.main-view__content {
  margin-left: 240px;
  padding: 100px 2.5rem 4rem;
  min-height: 100vh;
}

.main-view__header { margin-bottom: 2.5rem; }

.main-view__breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.875rem;
}

.main-view__breadcrumb-sep { color: var(--text-muted); font-size: 0.75rem; }
.main-view__title { color: var(--text-primary); margin-bottom: 0.75rem; }
.main-view__subtitle { color: var(--text-muted); font-size: 0.9375rem; max-width: 640px; line-height: 1.7; }

.main-view__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1.25rem;
  background: var(--surface-container);
  border-radius: var(--radius-xl);
  border: 1px solid var(--ghost-border);
}
.main-view__placeholder-text { color: var(--text-muted); font-size: 0.9375rem; }

.step-enter-active, .step-leave-active { transition: opacity 200ms ease, transform 200ms ease; }
.step-enter-from { opacity: 0; transform: translateX(12px); }
.step-leave-to   { opacity: 0; transform: translateX(-8px); }
</style>