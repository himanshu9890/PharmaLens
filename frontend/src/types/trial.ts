export interface TrialSummary {
  nct_id: string
  title: string
  sponsor_name: string | null
  sponsor_type: string | null
  phase: string | null
  status: string | null
  conditions: string[]
  countries: string[]
  enrollment: number | null
  start_date: string | null
  primary_completion_date: string | null
  composite_score: number | null
}

export interface TrialSearchResult {
  trials: TrialSummary[]
  total_count: number
  page: number
  per_page: number
  next_page_token: string | null
}

export interface PrimaryOutcome {
  measure?: string
  description?: string
  timeFrame?: string
}

export interface Intervention {
  type: string | null
  name: string | null
  other_names: string[]
}

export interface TrialDetail extends TrialSummary {
  enrollment_type: string | null
  interventions: Intervention[] | null
  brief_summary: string | null
  primary_outcomes: PrimaryOutcome[]
  trial_promise_score: number | null
  drug_profile_score: number | null
  kol_sentiment_score: number | null
  competitive_score: number | null
}

export interface SearchParams {
  therapy_area?: string
  phase?: string[]
  status?: string
  country?: string
  drug_type?: string
  sponsor_type?: string
  start_date_from?: string
  start_date_to?: string
  min_score?: number
  sort_by?: string
  sort_order?: string
  page?: number
  per_page?: number
}

export interface MeshSuggestion {
  label: string
  ui: string
}
