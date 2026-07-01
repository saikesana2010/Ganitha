import { useEffect, useRef } from 'react'
import katex from 'katex'
import 'katex/dist/katex.min.css'

// Patterns that look like LaTeX / math expressions
const MATH_PATTERN = /(\*\*|\^|\\frac|\\sqrt|\\int|\\sum|\\pi|[α-ωΑ-Ω])/

export default function MathRenderer({ text }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!ref.current) return
    if (!MATH_PATTERN.test(text)) {
      ref.current.textContent = text
      return
    }

    // Convert common SymPy notation to LaTeX
    const latex = toLatex(text)

    try {
      katex.render(latex, ref.current, {
        throwOnError: false,
        displayMode: false,
      })
    } catch {
      ref.current.textContent = text
    }
  }, [text])

  return <span ref={ref} />
}

function toLatex(text) {
  return text
    .replace(/\*\*/g, '^')           // x**2 → x^2
    .replace(/\*/g, ' \\cdot ')      // x*y → x·y
    .replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')
    .replace(/pi/g, '\\pi')
}
