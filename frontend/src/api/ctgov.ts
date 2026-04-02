/**
 * Direct ClinicalTrials.gov v2 browser client.
 * Browsers receive Access-Control-Allow-Origin: * so no proxy needed.
 * Server-side calls (from Render/Railway) get 403 due to IP blocking,
 * which is why this client runs in the browser instead.
 */
import axios from 'axios'
import type { MeshSuggestion, SearchParams, TrialDetail, TrialSearchResult, TrialSummary } from '../types/trial'

const CT_BASE = 'https://clinicaltrials.gov/api/v2'
const MESH_BASE = 'https://id.nlm.nih.gov/mesh'

const PHASE_MAP: Record<string, string> = {
  early1: 'EARLY_PHASE1',
  '1': 'PHASE1',
  '2': 'PHASE2',
  '3': 'PHASE3',
  '4': 'PHASE4',
}

const STATUS_MAP: Record<string, string> = {
  recruiting: 'RECRUITING',
  active: 'ACTIVE_NOT_RECRUITING',
  completed: 'COMPLETED',
}

function parseDate(val: string | undefined): string | null {
  if (!val) return null
  if (val.length === 10 && val[4] === '-') return val
  try {
    const d = new Date(val)
    if (!isNaN(d.getTime())) return d.toISOString().slice(0, 10)
  } catch { /* ignore */ }
  return val
}

function normaliseStudy(study: Record<string, unknown>): TrialSummary & Partial<TrialDetail> {
  const proto = (study.protocolSection ?? {}) as Record<string, unknown>

  const ident = (proto.identificationModule ?? {}) as Record<string, unknown>
  const statusMod = (proto.statusModule ?? {}) as Record<string, unknown>
  const sponsorMod = (proto.sponsorCollaboratorsModule ?? {}) as Record<string, unknown>
  const designMod = (proto.designModule ?? {}) as Record<string, unknown>
  const condMod = (proto.conditionsModule ?? {}) as Record<string, unknown>
  const locMod = (proto.contactsLocationsModule ?? {}) as Record<string, unknown>
  const descMod = (proto.descriptionModule ?? {}) as Record<string, unknown>
  const outcomesMod = (proto.outcomesModule ?? {}) as Record<string, unknown>
  const armsMod = (proto.armsInterventionsModule ?? {}) as Record<string, unknown>
  const eligMod = (proto.eligibilityModule ?? {}) as Record<string, unknown>

  const leadSponsor = (sponsorMod.leadSponsor ?? {}) as Record<string, unknown>
  const phases = (designMod.phases ?? []) as string[]
  const enrollInfo = (designMod.enrollmentInfo ?? {}) as Record<string, unknown>

  const meshConds = (condMod.meshes ?? []) as Array<Record<string, unknown>>
  const conditions = meshConds.length
    ? meshConds.map((m) => String(m.term ?? ''))
    : ((condMod.conditions ?? []) as string[])

  const locations = (locMod.locations ?? []) as Array<Record<string, unknown>>
  const countries = [...new Set(locations.map((l) => String(l.country ?? '')).filter(Boolean))]

  const interventions = ((armsMod.interventions ?? []) as Array<Record<string, unknown>>).map((iv) => ({
    type: String(iv.type ?? ''),
    name: String(iv.name ?? ''),
    other_names: (iv.otherNames ?? []) as string[],
  }))

  const primaryOutcomes = (outcomesMod.primaryOutcomes ?? []) as Array<Record<string, unknown>>

  let phase: string | null = null
  if (phases.length) {
    const raw = phases[0]
    phase = raw === 'EARLY_PHASE1' ? 'Early Phase 1' : raw.replace('PHASE', 'Phase ')
  }

  const sponsorClass = String(leadSponsor.class ?? '').toUpperCase()
  const sponsorType = sponsorClass === 'INDUSTRY' ? 'industry'
    : ['NIH', 'FED'].includes(sponsorClass) ? 'nih'
    : 'academic'

  const startDateStruct = (statusMod.startDateStruct ?? {}) as Record<string, unknown>
  const completionStruct = (statusMod.primaryCompletionDateStruct ?? {}) as Record<string, unknown>

  return {
    nct_id: String(ident.nctId ?? ''),
    title: String(ident.briefTitle ?? ident.officialTitle ?? ''),
    sponsor_name: String(leadSponsor.name ?? '') || null,
    sponsor_type: sponsorType,
    phase,
    status: String(statusMod.overallStatus ?? '') || null,
    conditions,
    countries,
    enrollment: (enrollInfo.count as number) ?? null,
    enrollment_type: String(enrollInfo.type ?? '') || null,
    start_date: parseDate(startDateStruct.date as string),
    primary_completion_date: parseDate(completionStruct.date as string),
    composite_score: null,
    interventions,
    brief_summary: String(descMod.briefSummary ?? '') || null,
    primary_outcomes: primaryOutcomes,
    trial_promise_score: null,
    drug_profile_score: null,
    kol_sentiment_score: null,
    competitive_score: null,
  }
}

export async function searchTrialsDirect(params: SearchParams): Promise<TrialSearchResult> {
  const p: Record<string, string> = {
    format: 'json',
    pageSize: String(params.per_page ?? 25),
  }

  if (params.therapy_area) p['query.cond'] = params.therapy_area
  if (params.phase?.length) {
    p['filter.phase'] = params.phase.map((ph) => PHASE_MAP[ph] ?? ph).join('|')
  }
  if (params.status && params.status !== 'all') {
    const mapped = STATUS_MAP[params.status]
    if (mapped) p['filter.overallStatus'] = mapped
  }
  if (params.country) p['query.locn'] = params.country

  const { data } = await axios.get(`${CT_BASE}/studies`, { params: p })

  const trials = ((data.studies ?? []) as Array<Record<string, unknown>>).map(normaliseStudy) as TrialSummary[]

  return {
    trials,
    total_count: data.totalCount ?? trials.length,
    page: params.page ?? 1,
    per_page: params.per_page ?? 25,
    next_page_token: data.nextPageToken ?? null,
  }
}

export async function getTrialDirect(nctId: string): Promise<TrialDetail | null> {
  try {
    const { data } = await axios.get(`${CT_BASE}/studies/${nctId}`, {
      params: { format: 'json' },
    })
    return normaliseStudy(data) as TrialDetail
  } catch {
    return null
  }
}

export async function getMeshSuggestionsDirect(q: string): Promise<MeshSuggestion[]> {
  if (q.length < 2) return []
  try {
    const { data } = await axios.get(`${MESH_BASE}/lookup/descriptor`, {
      params: { label: q, limit: 10, match: 'contains' },
    })
    return (data as Array<Record<string, unknown>>).map((item) => ({
      label: String(item.label ?? ''),
      ui: String(item.resource ?? '').split('/').at(-1) ?? '',
    }))
  } catch {
    return []
  }
}
