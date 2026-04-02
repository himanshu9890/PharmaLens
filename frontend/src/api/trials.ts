import axios from 'axios'
import type { MeshSuggestion, SearchParams, TrialDetail, TrialSearchResult } from '../types/trial'
import {
  searchTrialsDirect,
  getTrialDirect,
  getMeshSuggestionsDirect,
} from './ctgov'

// If VITE_API_URL is set (production), call ClinicalTrials.gov directly from
// the browser — it returns Access-Control-Allow-Origin: * for browser requests.
// In local dev (no VITE_API_URL), the Vite proxy routes /api → localhost:8000.
const USE_DIRECT = Boolean(import.meta.env.VITE_API_URL)
const BASE = import.meta.env.VITE_API_URL ?? '/api/v1'
const api = axios.create({ baseURL: BASE })

export async function searchTrials(params: SearchParams): Promise<TrialSearchResult> {
  if (USE_DIRECT) return searchTrialsDirect(params)
  const cleaned: Record<string, string | string[] | number | undefined> = {}
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '' && v !== null) cleaned[k] = v as string
  }
  const { data } = await api.get<TrialSearchResult>('/trials/search', { params: cleaned })
  return data
}

export async function getTrial(nctId: string): Promise<TrialDetail> {
  if (USE_DIRECT) {
    const trial = await getTrialDirect(nctId)
    if (!trial) throw new Error(`Trial ${nctId} not found`)
    return trial
  }
  const { data } = await api.get<TrialDetail>(`/trials/${nctId}`)
  return data
}

export async function getMeshSuggestions(q: string): Promise<MeshSuggestion[]> {
  if (USE_DIRECT) return getMeshSuggestionsDirect(q)
  if (q.length < 2) return []
  const { data } = await api.get<MeshSuggestion[]>('/trials/mesh-autocomplete', { params: { q } })
  return data
}

export function buildCsvExportUrl(params: SearchParams): string {
  // CSV export always goes through the backend (server-side generation)
  const qs = new URLSearchParams()
  if (params.therapy_area) qs.set('therapy_area', params.therapy_area)
  if (params.status) qs.set('status', params.status)
  if (params.country) qs.set('country', params.country)
  if (params.phase) params.phase.forEach((p) => qs.append('phase', p))
  return `${BASE}/trials/export/csv?${qs.toString()}`
}
