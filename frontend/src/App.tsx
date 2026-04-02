import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { searchTrials } from './api/trials'
import { SearchForm } from './components/SearchForm'
import { TrialsTable } from './components/TrialsTable'
import { TrialDetail } from './components/TrialDetail'
import type { SearchParams } from './types/trial'

export default function App() {
  const [searchParams, setSearchParams] = useState<SearchParams>({})
  const [hasSearched, setHasSearched] = useState(false)
  const [selectedNctId, setSelectedNctId] = useState<string | null>(null)
  const [page, setPage] = useState(1)

  const { data, isFetching, error } = useQuery({
    queryKey: ['trials', searchParams, page],
    queryFn: () => searchTrials({ ...searchParams, page }),
    enabled: hasSearched,
    staleTime: 1000 * 60 * 5,
  })

  function handleSearch(params: SearchParams) {
    setPage(1)
    setSearchParams(params)
    setHasSearched(true)
  }

  function handlePageChange(newPage: number) {
    setPage(newPage)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Nav */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-screen-xl items-center gap-3 px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="h-5 w-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <span className="text-xl font-bold text-gray-900">PharmaLens</span>
          </div>
          <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
            Phase 1 — MVP
          </span>
          <div className="ml-auto flex items-center gap-4 text-sm text-gray-500">
            <a
              href="https://clinicaltrials.gov"
              target="_blank"
              rel="noreferrer"
              className="hover:text-gray-700"
            >
              ClinicalTrials.gov
            </a>
            <a
              href="/docs"
              target="_blank"
              rel="noreferrer"
              className="hover:text-gray-700"
            >
              API docs
            </a>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-screen-xl px-6 py-8">
        {/* Hero */}
        {!hasSearched && (
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">
              Pharma BD Intelligence Platform
            </h1>
            <p className="mt-3 text-base text-gray-500 max-w-2xl mx-auto">
              Search and rank clinical trial licensing opportunities from{' '}
              <span className="font-medium text-gray-700">ClinicalTrials.gov</span> — powered by
              AI scoring. Free, open-source.
            </p>
          </div>
        )}

        <SearchForm onSearch={handleSearch} loading={isFetching} />

        {error && (
          <div className="mt-6 rounded-md bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
            Failed to fetch trials. Please check that the backend is running and try again.
          </div>
        )}

        {hasSearched && data && (
          <TrialsTable
            trials={data.trials}
            totalCount={data.total_count}
            page={page}
            perPage={data.per_page}
            onPageChange={handlePageChange}
            onRowClick={(nctId) => setSelectedNctId(nctId)}
            searchParams={searchParams}
          />
        )}

        {hasSearched && isFetching && !data && (
          <div className="mt-10 flex items-center justify-center gap-3 text-gray-400">
            <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
            </svg>
            Fetching trials from ClinicalTrials.gov…
          </div>
        )}
      </main>

      {/* Trial detail panel */}
      {selectedNctId && (
        <TrialDetail nctId={selectedNctId} onClose={() => setSelectedNctId(null)} />
      )}
    </div>
  )
}
