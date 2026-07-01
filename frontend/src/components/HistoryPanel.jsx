export default function HistoryPanel({ history, onSelect }) {
  if (!history.length) return null

  return (
    <div className="mt-8">
      <h2 className="text-slate-400 text-xs uppercase tracking-widest mb-3">Recent Questions</h2>
      <ul className="space-y-2">
        {history.map((item) => (
          <li
            key={item.id}
            onClick={() => onSelect(item.question)}
            className="flex justify-between items-center bg-slate-800 hover:bg-slate-700 
                       cursor-pointer rounded-xl px-4 py-3 transition"
          >
            <span className="text-sm text-slate-200 truncate max-w-xs">{item.question}</span>
            <div className="flex items-center gap-2 shrink-0 ml-3">
              <span className="text-xs text-emerald-400 font-semibold">{item.answer}</span>
              <span className="text-xs text-slate-500">{item.type}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
