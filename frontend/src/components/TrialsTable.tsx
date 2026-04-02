import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table'
import { useState } from 'react'
import type { SearchParams, TrialSummary } from '../types/trial'
import { buildCsvExportUrl } from '../api/trials'
import { ScoreBadge } from './ScoreBadge'

const helper = createColumnHelper<TrialSummary>()

const STATUS_COLORS: Record<string, string> = {
  RECRUITING: 'bg-green-100 text-green-700',
  ACTIVE_NOT_RECRUITING: 'bg-blue-100 text-blue-700',
  COMPLETED: 'bg-gray-100 text-gray-600',
  TERMINATED: 'bg-red-100 text-red-700',
  WITHDRAWN: 'bg-red-100 text-red-600',
  ENROLLING_BY_INVITATION: 'bg-purple-100 text-purple-700',
}

function StatusBadge({ status }: { status: string | null }) {
  if (!status) return null
  const label = status.replace(/_/g, ' ')
  const cls = STATUS_COLORS[status] ?? 'bg-gray-100 text-gray-600'
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${cls}`}>
      {label}
    </span>
  )
}

interface Props {
  trials: TrialSummary[]
  totalCount: number
  page: number
  perPage: number
  onPageChange: (page: number) => void
  onRowClick: (nctId: string) => void
  searchParams: SearchParams
}

export function TrialsTable({
  trials,
  totalCount,
  page,
  perPage,
  onPageChange,
  onRowClick,
  searchParams,
}: Props) {
  const [sorting, setSorting] = useState<SortingState>([])

  const columns = [
    helper.accessor('composite_score', {
      header: 'BD Score',
      cell: (info) => <ScoreBadge score={info.getValue()} />,
      size: 80,
    }),
    helper.accessor('nct_id', {
      header: 'NCT ID',
      cell: (info) => (
        <a
          href={`https://clinicaltrials.gov/study/${info.getValue()}`}
          target="_blank"
          rel="noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="font-mono text-xs text-blue-600 hover:underline"
        >
          {info.getValue()}
        </a>
      ),
      size: 120,
    }),
    helper.accessor('title', {
      header: 'Trial title',
      cell: (info) => (
        <span className="line-clamp-2 text-sm text-gray-800">{info.getValue()}</span>
      ),
    }),
    helper.accessor('sponsor_name', {
      header: 'Sponsor',
      cell: (info) => <span className="text-sm text-gray-700">{info.getValue() ?? '—'}</span>,
      size: 160,
    }),
    helper.accessor('phase', {
      header: 'Phase',
      cell: (info) => (
        <span className="whitespace-nowrap text-sm text-gray-700">{info.getValue() ?? '—'}</span>
      ),
      size: 100,
    }),
    helper.accessor('status', {
      header: 'Status',
      cell: (info) => <StatusBadge status={info.getValue()} />,
      size: 160,
    }),
    helper.accessor('conditions', {
      header: 'Indication',
      cell: (info) => {
        const conds = info.getValue()
        return (
          <span className="text-sm text-gray-700">
            {conds.length > 0 ? conds.slice(0, 2).join(', ') : '—'}
            {conds.length > 2 && (
              <span className="ml-1 text-xs text-gray-400">+{conds.length - 2}</span>
            )}
          </span>
        )
      },
    }),
    helper.accessor('enrollment', {
      header: 'Enrollment',
      cell: (info) => (
        <span className="text-sm text-gray-700">
          {info.getValue()?.toLocaleString() ?? '—'}
        </span>
      ),
      size: 100,
    }),
    helper.accessor('primary_completion_date', {
      header: 'Completion',
      cell: (info) => (
        <span className="whitespace-nowrap text-sm text-gray-700">
          {info.getValue() ?? '—'}
        </span>
      ),
      size: 110,
    }),
  ]

  const table = useReactTable({
    data: trials,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    manualPagination: true,
  })

  const totalPages = Math.ceil(totalCount / perPage)
  const csvUrl = buildCsvExportUrl(searchParams)

  return (
    <div className="mt-6">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm text-gray-500">
          <span className="font-semibold text-gray-800">{totalCount.toLocaleString()}</span> trials
          found
        </p>
        <a
          href={csvUrl}
          download="pharmalens_trials.csv"
          className="flex items-center gap-1.5 rounded-md border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-600 hover:border-gray-400 hover:text-gray-800"
        >
          ↓ Export CSV
        </a>
      </div>

      <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
        <table className="w-full text-left">
          <thead className="border-b border-gray-200 bg-gray-50">
            {table.getHeaderGroups().map((hg) => (
              <tr key={hg.id}>
                {hg.headers.map((header) => (
                  <th
                    key={header.id}
                    onClick={header.column.getToggleSortingHandler()}
                    className={`px-4 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500 ${
                      header.column.getCanSort() ? 'cursor-pointer select-none hover:text-gray-700' : ''
                    }`}
                    style={{ width: header.getSize() !== 150 ? header.getSize() : undefined }}
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                    {header.column.getIsSorted() === 'asc'
                      ? ' ↑'
                      : header.column.getIsSorted() === 'desc'
                        ? ' ↓'
                        : ''}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-gray-100">
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                onClick={() => onRowClick(row.original.nct_id)}
                className="cursor-pointer hover:bg-blue-50/40 transition-colors"
              >
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-4 py-3 align-top">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
            {trials.length === 0 && (
              <tr>
                <td colSpan={columns.length} className="px-4 py-12 text-center text-sm text-gray-400">
                  No trials found. Try adjusting your search filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
          <span>
            Page {page} of {totalPages}
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1}
              className="rounded-md border border-gray-300 px-3 py-1.5 text-xs hover:bg-gray-50 disabled:opacity-40"
            >
              Previous
            </button>
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages}
              className="rounded-md border border-gray-300 px-3 py-1.5 text-xs hover:bg-gray-50 disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
