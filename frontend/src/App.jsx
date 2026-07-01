import { useState, useEffect } from 'react'
import { solveMath, getHistory } from './api/mathApi'
import StepCard from './components/StepCard'
import HistoryPanel from './components/HistoryPanel'

const EXAMPLES = [
  '2x + 3 = 7',
  'derivative of x^3 + 2x',
  'area of circle radius 5',
  'sin 30 degrees',
  '25% of 200',
  'integrate x^2',
  'mean of 4, 8, 6, 5, 3',
  'determinant of [[1,2],[3,4]]',
  'combination 5 3',
  'standard deviation of 2, 4, 4, 4, 5, 5, 7, 9',
]

export default function App() {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(() => { loadHistory() }, [])

  async function loadHistory() {
    try {
      const data = await getHistory(8)
      setHistory(data)
    } catch { /* DB might not be running */ }
  }

  async function handleSolve(e) {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await solveMath(question)
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
        loadHistory()
      }
    } catch {
      setError('Could not connect to the backend. Make sure it is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-12">
      {/* Header */}
      <div className="mb-10 text-center">
        <h1 className="text-5xl font-extrabold tracking-tight text-white">
          Magi<span className="text-emerald-400">ne</span>
        </h1>
        <p className="text-slate-400 mt-2 text-sm">Offline AI Math Solver · Class 1–12</p>
      </div>

      {/* Input */}
      <form onSubmit={handleSolve} className="w-full max-w-2xl">
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="e.g. 2x + 3 = 7  or  derivative of x^2"
            className="flex-1 bg-slate-800 text-white placeholder-slate-500 rounded-xl 
                       px-5 py-4 text-sm outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white 
                       font-semibold px-6 py-4 rounded-xl transition text-sm"
          >
            {loading ? 'Solving…' : 'Solve'}
          </button>
        </div>

        {/* Example chips */}
        <div className="flex flex-wrap gap-2 mt-3">
          {EXAMPLES.map(ex => (
            <button
              key={ex}
              type="button"
              onClick={() => setQuestion(ex)}
              className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 
                         px-3 py-1 rounded-full transition"
            >
              {ex}
            </button>
          ))}
        </div>
      </form>

      {/* Result */}
      <div className="w-full max-w-2xl">
        {error && (
          <div className="mt-6 bg-red-900/40 border border-red-700 text-red-300 
                          rounded-xl px-5 py-4 text-sm">
            {error}
          </div>
        )}

        {result && (
          <StepCard
            steps={result.steps}
            answer={result.answer}
            type={result.type}
            source={result.source}
          />
        )}

        <HistoryPanel history={history} onSelect={q => setQuestion(q)} />
      </div>
    </div>
  )
}
