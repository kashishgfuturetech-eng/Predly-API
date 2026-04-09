<template>
  <div class="main-view">
    <TopNav show-links :project-id="projectId" active-step="Graph Build" />
    <SideNav :current-step="currentStep" :completed-steps="completedSteps" @navigate="navigateTo" />

    <div class="main-view__content">
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
        <!-- Step 1: Graph Build -->
        <Step1GraphBuild
          v-if="currentStep === 'graph'"
          :project-data="projectData"
          @completed="onStepCompleted('graph', $event)"
        />

        <!-- Step 2: Env Setup -->
        <Step2EnvSetup
          v-else-if="currentStep === 'env'"
          :project-data="projectData"
          @completed="onStepCompleted('env', $event)"
        />

        <!--
          Step 3: Simulation
          Props:
            simulation-id  — sim_xxxx created by Step 2 (/api/simulation/create)
            project-id     — fallback if sim ID not yet set (Step3 can create it)
          Emits:
            completed      — moves user to Step 4 / Report
        -->
        <Step3Simulation
          v-else-if="currentStep === 'simulation'"
          :simulation-id="projectData.simulation_id || null"
          :project-id="projectData.project_id"
          @completed="onStepCompleted('simulation', {})"
        />

        <!--
          Step 4: Report
          Props:
            simulation-id  — required so backend can look up simulation data
            report-id      — display fallback before real ID is returned by API
          Emits:
            completed      — moves user to Step 5 / Interaction
        -->
        <Step4Report
          v-else-if="currentStep === 'report'"
          :simulation-id="projectData.simulation_id || null"
          :report-id="projectData.report_id || 'REF-PENDING'"
          @completed="onStepCompleted('report', {})"
        />

        <!--
          Step 5: Interaction
          Props:
            report-id      — passed so the chat panel can reference the correct report
        -->
        <Step5Interaction
          v-else-if="currentStep === 'interaction'"
          :report-id="projectData.report_id || 'REF-PENDING'"
          :simulation-id="projectData.simulation_id || null"
        />

        <!-- Fallback placeholder -->
        <div v-else class="main-view__placeholder">
          <span class="material-symbols-outlined" style="font-size:48px;color:var(--text-muted)">account_tree</span>
          <p class="main-view__placeholder-text">Select a step from the sidebar to begin</p>
          <button class="btn-primary" @click="navigateTo('graph')">
            Begin Graph Build
            <span class="material-symbols-outlined" style="font-size:18px">arrow_forward</span>
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TopNav from '../components/TopNav.vue'
import SideNav from '../components/SideNav.vue'
import Step1GraphBuild from '../components/Step1GraphBuild.vue'
import Step2EnvSetup from '../components/Step2EnvSetup.vue'
import Step3Simulation from '../components/Step3Simulation.vue'
import Step4Report from '../components/Step4Report.vue'
import Step5Interaction from '../components/Step5Interaction.vue'  // ← NEW

const props = defineProps({ projectId: String })
const router = useRouter()

const currentStep = ref('graph')
const completedSteps = ref([])

/*
  projectData is the shared state that flows down through all steps.
  Each step's @completed event merges its returned data here.

  Key fields populated by each step:
    graph step   → graph_id, project_id (from Step1GraphBuild)
    env step     → simulation_id        (from Step2EnvSetup after /api/simulation/create)
    simulation   → (no new data needed — simulation_id already set)
    report       → report_id            (Step4Report sets this internally via API)
    interaction  → (no new data needed — report_id already set)
*/
const projectData = ref({
  project_id:    props.projectId || null,
  graph_id:      null,
  simulation_id: null,
  report_id:     null,
  ontology:      null,
})

const stepOrder = ['graph', 'env', 'simulation', 'report', 'interaction']  // ← added 'interaction'
const stepIndex = computed(() => stepOrder.indexOf(currentStep.value))

const stepTitles = {
  graph:       'Graph Build & Ontology',
  env:         'Environment Configuration',
  simulation:  'Simulation Run',
  report:      'Report Generation',
  interaction: 'AI Interaction',             // ← NEW
}
const stepHeadings = {
  graph:       'Graph Build',
  env:         'Env Setup',
  simulation:  'Simulation',
  report:      'Report',
  interaction: 'Interaction',                // ← NEW
}
const stepSubtitles = {
  graph:       'Extract ontology structures, entity types, and relationships from your reality seeds.',
  env:         'Define simulation parameters, agent personas, and recommendation logic.',
  simulation:  'Launch parallel autonomous agents across Info Plaza and Topic Community.',
  report:      'Generate AI-powered predictive intelligence from simulation data.',
  interaction: 'Query the Simulation Oracle to explore agent behaviors, emergent patterns, and hypothetical scenarios.',  // ← NEW
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
  // Merge any new IDs returned by the step
  if (data) Object.assign(projectData.value, data)

  // Auto-advance to next step
  const next = stepOrder[stepOrder.indexOf(step) + 1]
  if (next) {
    currentStep.value = next
  }
}

onMounted(() => {
  currentStep.value = 'graph'
})
</script>

<style scoped>
.main-view {
  min-height: 100vh;
  background: var(--surface);
}

.main-view__content {
  margin-left: 240px;
  padding-top: 60px;
  min-height: 100vh;
  padding: 100px 2.5rem 4rem;
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

/* Step transitions */
.step-enter-active, .step-leave-active { transition: opacity 200ms ease, transform 200ms ease; }
.step-enter-from { opacity: 0; transform: translateX(12px); }
.step-leave-to   { opacity: 0; transform: translateX(-8px); }
</style>