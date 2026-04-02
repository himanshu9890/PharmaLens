import axios from 'axios'
import type { MeshSuggestion, SearchParams, TrialDetail, TrialSearchResult } from '../types/trial'

// In dev: Vite proxies /api → localhost:8000 (no env var needed).
// In production (Vercel): set VITE_API_URL=https://your-app.onrender.com/api/v1
const BASE = import.meta.env.VITE_API_URL ?? '/api/v1'
const api = axios.create({ baseURL: BASE })

export async function searchTrials(params: SearchParams): Promise<TrialSearchResult> {
  const cleaned: Record<string, string | string[] | number | undefined> = {}
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '' && v !== null) {
      cleaned[k] = v as string | string[] | number
    }
  }
  const { data } = await api.get<TrialSearchResult>('/trials/search', { params: cleaned })
  return data
}

export async function getTrial(nctId: string): Promise<TrialDetail> {
  const { data } = await api.get<TrialDetail>(`/trials/${nctId}`)
  return data
}

export async function getMeshSuggestions(q: string): Promise<MeshSuggestion[]> {
  if (q.length < 2) return []
  const { data } = await api.get<MeshSuggestion[]>('/trials/mesh-autocomplete', {
    params: { q },
  })
  return data
}

export function buildCsvExportUrl(params: SearchParams): string {
  const qs = new URLSearchParams()
  if (params.therapy_area) qs.set('therapy_area', params.therapy_area)
  if (params.status) qs.set('status', params.status)
  if (params.country) qs.set('country', params.country)
  if (params.phase) params.phase.forEach((p) => qs.append('phase', p))
  return `${BASE}/trials/export/csv?${qs.toString()}`
}
