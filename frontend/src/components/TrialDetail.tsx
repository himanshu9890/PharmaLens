import { useQuery } from '@tanstack/react-query'
import { getTrial } from '../api/trials'
import { ScoreBadge } from './ScoreBadge'

interface Props {
  nctId: string
  onClose: () => void
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="border-t border-gray-100 pt-4">
      <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-gray-500">{title}</h3>
      {children}
    </div>
  )
}

function Tag({ label }: { label: string }) {
  return (
    <span className="inline-block rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
      {label}
    </span>
  )
}

export function TrialDetail({ nctId, onClose }: Props) {
  const { data: trial, isLoading, error } = useQuery({
    queryKey: ['trial', nctId],
    queryFn: () => getTrial(nctId),
  })

  return (
    <div className="fixed inset-0 z-40 flex justify-end">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/30 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative z-50 flex h-full w-full max-w-2xl flex-col overflow-hidden bg-white shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-gray-200 bg-gray-50 px-6 py-4">
          <div>
            <p className="font-mono text-xs font-semibold text-blue-600">{nctId}</p>
            {trial && (
              <h2 className="mt-1 text-base font-semibold leading-snug text-gray-900 line-clamp-3">
                {trial.title}
              </h2>
            )}
          </div>
          <button
            onClick={onClose}
            className="ml-4 mt-0.5 flex-shrink-0 rounded-md p-1.5 text-gray-400 hover:bg-gray-200 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-6 py-5">
          {isLoading && (
            <div className="flex items-center justify-center py-16 text-gray-400">
              Loading trial data…
            </div>
          )}

          {error && (
            <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">
              Failed to load trial details.
            </div>
          )}

          {trial && (
            <div className="space-y-5">
              {/* Score row */}
              <div className="flex flex-wrap gap-4">
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-500">BD Score</span>
                  <ScoreBadge score={trial.composite_score} size="md" />
                </div>
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-500">Phase</span>
                  <span className="text-sm font-medium text-gray-800">{trial.phase ?? '—'}</span>
                </div>
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-500">Status</span>
                  <span className="text-sm font-medium text-gray-800">
                    {trial.status?.replace(/_/g, ' ') ?? '—'}
                  </span>
                </div>
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-500">Enrollment</span>
                  <span className="text-sm font-medium text-gray-800">
                    {trial.enrollment?.toLocaleString() ?? '—'}
                    {trial.enrollment_type && (
                      <span className="ml-1 text-xs text-gray-400">({trial.enrollment_type})</span>
                    )}
                  </span>
                </div>
              </div>

              {/* Sponsor */}
              <Section title="Sponsor">
                <p className="text-sm text-gray-800">{trial.sponsor_name ?? '—'}</p>
                {trial.sponsor_type && (
                  <p className="mt-0.5 text-xs text-gray-500 capitalize">{trial.sponsor_type}</p>
                )}
              </Section>

              {/* Conditions */}
              {trial.conditions.length > 0 && (
                <Section title="Conditions / Indications">
                  <div className="flex flex-wrap gap-2">
                    {trial.conditions.map((c) => (
                      <Tag key={c} label={c} />
                    ))}
                  </div>
                </Section>
              )}

              {/* Interventions */}
              {trial.interventions && (trial.interventions as []).length > 0 && (
                <Section title="Interventions">
                  <div className="space-y-1.5">
                    {(trial.interventions as Array<{ type: string | null; name: string | null; other_names: string[] }>).map(
                      (iv, i) => (
                        <div key={i} className="text-sm text-gray-800">
                          <span className="font-medium">{iv.name}</span>
                          {iv.type && (
                            <span className="ml-2 text-xs text-gray-400">({iv.type})</span>
                          )}
                          {iv.other_names?.length > 0 && (
                            <span className="ml-1 text-xs text-gray-400">
                              aka {iv.other_names.join(', ')}
                            </span>
                          )}
                        </div>
                      )
                    )}
                  </div>
                </Section>
              )}

              {/* Dates & geography */}
              <Section title="Dates & Geography">
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <p className="text-xs text-gray-500">Start date</p>
                    <p className="text-gray-800">{trial.start_date ?? '—'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Primary completion</p>
                    <p className="text-gray-800">{trial.primary_completion_date ?? '—'}</p>
                  </div>
                  <div className="col-span-2">
                    <p className="text-xs text-gray-500">Countries</p>
                    <p className="text-gray-800">
                      {trial.countries.length > 0 ? trial.countries.join(', ') : '—'}
                    </p>
                  </div>
                </div>
              </Section>

              {/* Brief summary */}
              {trial.brief_summary && (
                <Section title="Study Summary">
                  <p className="text-sm leading-relaxed text-gray-700">{trial.brief_summary}</p>
                </Section>
              )}

              {/* Primary outcomes */}
              {trial.primary_outcomes.length > 0 && (
                <Section title="Primary Outcomes">
                  <ul className="space-y-1.5">
                    {trial.primary_outcomes.map((o: { measure?: string }, i: number) => (
                      <li key={i} className="text-sm text-gray-700">
                        • {o.measure ?? JSON.stringify(o)}
                      </li>
                    ))}
                  </ul>
                </Section>
              )}

              {/* ClinicalTrials.gov link */}
              <div className="pt-2">
                <a
                  href={`https://clinicaltrials.gov/study/${nctId}`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 text-sm text-blue-600 hover:underline"
                >
                  View on ClinicalTrials.gov ↗
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
