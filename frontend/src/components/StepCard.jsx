import MathRenderer from './MathRenderer'

export default function StepCard({ steps, answer, type, source }) {
  const badgeColor = {
    algebra: 'bg-blue-600',
    calculus: 'bg-purple-600',
    geometry: 'bg-green-600',
    arithmetic: 'bg-yellow-600',
    trigonometry: 'bg-pink-600',
    llm: 'bg-orange-600',
    cache: 'bg-gray-500',
  }

  return (
    <div className="mt-6 bg-slate-800 rounded-2xl p-6 shadow-lg">
      <div className="flex items-center gap-3 mb-4">
        <span className={`text-xs font-semibold px-3 py-1 rounded-full text-white ${badgeColor[type] ?? 'bg-slate-600'}`}>
          {type}
        </span>
        {source === 'cache' && (
          <span className="text-xs text-slate-400 italic">⚡ from cache</span>
        )}
        {source === 'llm' && (
          <span className="text-xs text-slate-400 italic">🤖 AI assisted</span>
        )}
      </div>

      <h2 className="text-slate-300 text-sm font-semibold uppercase tracking-widest mb-3">
        Step-by-Step Solution
      </h2>

      <ol className="space-y-2">
        {steps.map((step, i) => (
          <li key={i} className="flex gap-3 text-sm">
            <span className="text-slate-500 w-5 shrink-0">{i + 1}.</span>
            <span className="text-slate-200"><MathRenderer text={step} /></span>
          </li>
        ))}
      </ol>

      <div className="mt-5 pt-4 border-t border-slate-700">
        <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">Answer</p>
        <p className="text-2xl font-bold text-emerald-400"><MathRenderer text={answer} /></p>
      </div>
    </div>
  )
}
