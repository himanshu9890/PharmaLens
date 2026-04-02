import { useEffect, useRef, useState } from 'react'
import { getMeshSuggestions } from '../api/trials'
import type { MeshSuggestion } from '../types/trial'

interface Props {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export function MeshAutocomplete({ value, onChange, placeholder }: Props) {
  const [suggestions, setSuggestions] = useState<MeshSuggestion[]>([])
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const debounce = useRef<ReturnType<typeof setTimeout> | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (debounce.current) clearTimeout(debounce.current)
    if (value.length < 2) {
      setSuggestions([])
      setOpen(false)
      return
    }
    debounce.current = setTimeout(async () => {
      setLoading(true)
      try {
        const results = await getMeshSuggestions(value)
        setSuggestions(results)
        setOpen(results.length > 0)
      } catch {
        setSuggestions([])
      } finally {
        setLoading(false)
      }
    }, 300)
  }, [value])

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  return (
    <div ref={containerRef} className="relative">
      <div className="relative">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => suggestions.length > 0 && setOpen(true)}
          placeholder={placeholder ?? 'e.g. Breast Neoplasms, Diabetes Mellitus'}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        {loading && (
          <span className="absolute right-3 top-2.5 text-xs text-gray-400">Loading…</span>
        )}
      </div>

      {open && (
        <ul className="absolute z-20 mt-1 max-h-56 w-full overflow-auto rounded-md border border-gray-200 bg-white py-1 shadow-lg text-sm">
          {suggestions.map((s) => (
            <li
              key={s.ui}
              onMouseDown={() => {
                onChange(s.label)
                setOpen(false)
              }}
              className="cursor-pointer px-3 py-2 hover:bg-blue-50"
            >
              <span className="font-medium">{s.label}</span>
              <span className="ml-2 text-xs text-gray-400">{s.ui}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
