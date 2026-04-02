import { useState } from 'react'
import type { SearchParams } from '../types/trial'
import { MeshAutocomplete } from './MeshAutocomplete'

const PHASES = [
  { value: 'early1', label: 'Early Phase 1' },
  { value: '1', label: 'Phase 1' },
  { value: '2', label: 'Phase 2' },
  { value: '3', label: 'Phase 3' },
  { value: '4', label: 'Phase 4' },
]

const DRUG_TYPES = [
  { value: '', label: 'All' },
  { value: 'small_molecule', label: 'Small Molecule' },
  { value: 'biologic', label: 'Biologic' },
  { value: 'cell_therapy', label: 'Cell Therapy' },
  { value: 'gene_therapy', label: 'Gene Therapy' },
  { value: 'device', label: 'Device' },
]

const SPONSOR_TYPES = [
  { value: 'all', label: 'All' },
  { value: 'industry', label: 'Industry' },
  { value: 'academic', label: 'Academic / Other' },
  { value: 'nih', label: 'NIH / Federal' },
]

const STATUSES = [
  { value: 'recruiting', label: 'Recruiting' },
  { value: 'active', label: 'Active (not recruiting)' },
  { value: 'completed', label: 'Completed' },
  { value: 'all', label: 'All statuses' },
]

interface Props {
  onSearch: (params: SearchParams) => void
  loading: boolean
}

export function SearchForm({ onSearch, loading }: Props) {
  const [therapyArea, setTherapyArea] = useState('')
  const [phases, setPhases] = useState<string[]>([])
  const [status, setStatus] = useState('recruiting')
  const [country, setCountry] = useState('')
  const [drugType, setDrugType] = useState('')
  const [sponsorType, setSponsorType] = useState('all')
  const [startDateFrom, setStartDateFrom] = useState('')
  const [startDateTo, setStartDateTo] = useState('')

  function togglePhase(value: string) {
    setPhases((prev) =>
      prev.includes(value) ? prev.filter((p) => p !== value) : [...prev, value]
    )
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSearch({
      therapy_area: therapyArea || undefined,
      phase: phases.length > 0 ? phases : undefined,
      status: status !== 'all' ? status : undefined,
      country: country || undefined,
      drug_type: drugType || undefined,
      sponsor_type: sponsorType !== 'all' ? sponsorType : undefined,
      start_date_from: startDateFrom || undefined,
      start_date_to: startDateTo || undefined,
      page: 1,
      per_page: 25,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-5 text-lg font-semibold text-gray-800">Search Clinical Trials</h2>

      <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {/* Therapy area */}
        <div className="lg:col-span-2">
          <label className="mb-1.5 block text-sm font-medium text-gray-700">
            Therapy area / Indication
          </label>
          <MeshAutocomplete
            value={therapyArea}
            onChange={setTherapyArea}
            placeholder="e.g. Breast Neoplasms, Type 2 Diabetes…"
          />
        </div>

        {/* Status */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">Trial status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {STATUSES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>

        {/* Phases */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">
            Clinical phase
          </label>
          <div className="flex flex-wrap gap-2">
            {PHASES.map((p) => (
              <label
                key={p.value}
                className={`flex cursor-pointer items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
                  phases.includes(p.value)
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 bg-white text-gray-600 hover:border-gray-400'
                }`}
              >
                <input
                  type="checkbox"
                  className="hidden"
                  checked={phases.includes(p.value)}
                  onChange={() => togglePhase(p.value)}
                />
                {p.label}
              </label>
            ))}
          </div>
        </div>

        {/* Drug type */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">Drug / modality</label>
          <select
            value={drugType}
            onChange={(e) => setDrugType(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {DRUG_TYPES.map((d) => (
              <option key={d.value} value={d.value}>
                {d.label}
              </option>
            ))}
          </select>
        </div>

        {/* Sponsor type */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">Sponsor type</label>
          <select
            value={sponsorType}
            onChange={(e) => setSponsorType(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {SPONSOR_TYPES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>

        {/* Country */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">Country</label>
          <input
            type="text"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            placeholder="e.g. United States, Germany"
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {/* Date range */}
        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">
            Start date from
          </label>
          <input
            type="date"
            value={startDateFrom}
            onChange={(e) => setStartDateFrom(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="mb-1.5 block text-sm font-medium text-gray-700">Start date to</label>
          <input
            type="date"
            value={startDateTo}
            onChange={(e) => setStartDateTo(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="mt-5 flex items-center gap-3">
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? 'Searching…' : 'Search Trials'}
        </button>
        <button
          type="button"
          onClick={() => {
            setTherapyArea('')
            setPhases([])
            setStatus('recruiting')
            setCountry('')
            setDrugType('')
            setSponsorType('all')
            setStartDateFrom('')
            setStartDateTo('')
          }}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          Clear filters
        </button>
      </div>
    </form>
  )
}
