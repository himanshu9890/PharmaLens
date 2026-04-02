interface Props {
  score: number | null
  size?: 'sm' | 'md'
}

export function ScoreBadge({ score, size = 'md' }: Props) {
  if (score === null) {
    return (
      <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-500">
        —
      </span>
    )
  }

  const color =
    score >= 75
      ? 'bg-emerald-100 text-emerald-800 ring-emerald-200'
      : score >= 50
        ? 'bg-amber-100 text-amber-800 ring-amber-200'
        : 'bg-gray-100 text-gray-600 ring-gray-200'

  const cls = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm font-semibold'

  return (
    <span className={`inline-flex items-center rounded-full ring-1 ${color} ${cls}`}>
      {Math.round(score)}
    </span>
  )
}
