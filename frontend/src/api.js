/**
 * api.js — Predly backend connector
 * All calls go to Flask on localhost:10000
 * Change BASE_URL here if your backend runs on a different port/host.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// ─────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────

async function post(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }))
    throw new Error(err.error || `HTTP ${res.status}`)
  }
  return res.json()
}

async function get(path) {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }))
    throw new Error(err.error || `HTTP ${res.status}`)
  }
  return res.json()
}

/**
 * Poll a background task until it reaches 'completed' or 'failed'.
 * Returns the task result data on success, throws on failure.
 *
 * @param {string} taskId
 * @param {number} intervalMs  — how often to poll (default 3s; increase on CPU)
 * @param {number} timeoutMs   — max total wait (default 10 min)
 */
export function pollTask(taskId, intervalMs = 3000, timeoutMs = 600000) {
  const start = Date.now()
  return new Promise((resolve, reject) => {
    const id = setInterval(async () => {
      if (Date.now() - start > timeoutMs) {
        clearInterval(id)
        reject(new Error('Task timed out — the model may still be loading. Check backend logs.'))
        return
      }
      try {
        const data = await get(`/graph/task/${taskId}`)
        const task = data.data
        if (task?.status === 'completed') { clearInterval(id); resolve(task) }
        if (task?.status === 'failed')    { clearInterval(id); reject(new Error(task.error || 'Task failed')) }
      } catch (e) {
        // network hiccup — keep polling
        console.warn('Poll error (will retry):', e.message)
      }
    }, intervalMs)
  })
}

// ─────────────────────────────────────────────
// Project / Upload
// ─────────────────────────────────────────────

/**
 * Upload files and create a project.
 * Returns { success, data: { project_id, ... } }
 */
export async function uploadProject(files, prompt = '') {
  const form = new FormData()
  files.forEach(f => form.append('files', f))
  form.append('simulation_requirement', prompt.trim() || 'Simulate public opinion.')

  // AbortController gives it a 3 minute max
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 180000)

  try {
    const res = await fetch(`${BASE_URL}/graph/ontology/generate`, {
      method: 'POST',
      body: form,
      signal: controller.signal,
    })
    clearTimeout(timeout)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: res.statusText }))
      throw new Error(err.error || `Upload failed: HTTP ${res.status}`)
    }
    return res.json()
  } catch (e) {
    clearTimeout(timeout)
    if (e.name === 'AbortError') throw new Error('Ontology generation timed out — try a shorter document or simpler prompt')
    throw e
  }
}

// ─────────────────────────────────────────────
// Step 1 — Graph Build
// ─────────────────────────────────────────────

export async function generateOntology(projectId) {
  // Ontology is already generated during uploadProject (ontology/generate)
  // This just fetches the existing project data
  return get(`/graph/project/${projectId}`)
}

export async function extractEntities(projectId) {
  return post('/graph/entities/extract', { project_id: projectId })
}

export async function storeGraph(projectId) {
  return post('/graph/store', { project_id: projectId })
}

// ─────────────────────────────────────────────
// Step 2 — Env Setup
// ─────────────────────────────────────────────

export async function createSimulation(projectId) {
  return post('/simulation/create', { project_id: projectId })
}

export async function prepareSimulation(simulationId, projectId) {
  return post('/simulation/prepare', { simulation_id: simulationId, project_id: projectId })
}

export async function configureSimulation(simulationId, config) {
  return post('/simulation/configure', { simulation_id: simulationId, ...config })
}

// ─────────────────────────────────────────────
// Step 3 — Simulation
// ─────────────────────────────────────────────

export async function startSimulation(simulationId) {
  return post('/simulation/start', { simulation_id: simulationId })
}

export async function getSimulationStatus(simulationId) {
  return get(`/simulation/${simulationId}/status`)
}

// ─────────────────────────────────────────────
// Step 4 — Report
// ─────────────────────────────────────────────

export async function generateReport(simulationId) {
  return post('/report/generate', { simulation_id: simulationId })
}

export async function getReport(simulationId) {
  return get(`/report/${simulationId}`)
}