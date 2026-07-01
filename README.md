# Ganitha - Offline AI Math Solver

**Ganitha** is a production-grade, offline mathematics problem solver supporting Class 1–12 level problems across all syllabi (CBSE, ICSE, IB, State boards). It provides step-by-step solutions using a hybrid approach: structured symbolic math engines (SymPy) for speed and accuracy, with local LLM fallback for complex problems.

---

## Features

✅ **Fully Offline** — No external API calls after setup  
✅ **Multi-Domain Support** — Algebra, Calculus, Geometry, Arithmetic, Trigonometry  
✅ **Step-by-Step Solutions** — Not just answers, full explanations  
✅ **PostgreSQL Caching** — Instant responses for repeated questions  
✅ **LLM Fallback** — Ollama integration for complex/ambiguous problems  
✅ **Modern React UI** — Dark theme, responsive, example chips  
✅ **Docker Ready** — One-command deployment  

---

## Architecture

```
┌─────────────┐
│   React UI  │  (Vite + Tailwind)
└──────┬──────┘
       │ HTTP
┌──────▼──────────────────────────────────────┐
│          FastAPI Backend                    │
│  ┌────────────────────────────────────┐    │
│  │  Parser → Dispatcher → Solver      │    │
│  │  ├─ Algebra                        │    │
│  │  ├─ Calculus                       │    │
│  │  ├─ Geometry                       │    │
│  │  ├─ Arithmetic                     │    │
│  │  ├─ Trigonometry                   │    │
│  │  └─ LLM Fallback (Ollama)          │    │
│  └────────────────────────────────────┘    │
└──────┬──────────────────────┬───────────────┘
       │                      │
┌──────▼──────┐      ┌────────▼────────┐
│ PostgreSQL  │      │  Ollama (LLM)   │
│   (Cache)   │      │ qwen2.5-math    │
└─────────────┘      └─────────────────┘
```

**Request Flow:**
1. User submits question via React UI
2. Backend checks PostgreSQL cache
3. If not cached → Parser detects problem type
4. Dispatcher routes to appropriate solver
5. Solver generates step-by-step solution
6. If solver fails → Ollama LLM fallback
7. Result cached in PostgreSQL
8. Response sent to frontend

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Axios |
| Backend | FastAPI, Python 3.11+ |
| Math Engine | SymPy (symbolic math) |
| Database | PostgreSQL 16 (async via asyncpg) |
| LLM | Ollama (qwen2.5-math:1.5b) |
| Containerization | Docker, Docker Compose |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 20+, PostgreSQL 16, Ollama

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone <repo-url>
cd ganitha

# Start everything
docker-compose up --build

# Wait for Ollama to download the model (~1GB, first time only)
# Then open http://localhost:3000
```

**Services:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`
- Ollama: `localhost:11434`

### Option 2: Manual Setup

**1. Backend**
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://ganitha:ganitha@localhost:5432/ganitha"

# Start PostgreSQL (via Docker or local install)
docker run -d -p 5432:5432 -e POSTGRES_USER=Ganitha -e POSTGRES_PASSWORD=Ganitha -e POSTGRES_DB=ganitha postgres:16-alpine

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Ollama (LLM)**
```bash
# Install from https://ollama.com
ollama serve

# Pull math model (in another terminal)
ollama pull qwen2.5-math:1.5b
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`

---

## Usage Examples

### Algebra
```
Input:  2x + 3 = 7
Output: x = 2
Steps:  Given equation: 2*x+3 = 7
        Rearranging: 2*x - 4 = 0
        This is a linear equation. Isolating x.
        Solving for x:
          x = 2
```

### Calculus
```
Input:  derivative of x^3 + 2x
Output: 3*x**2 + 2
Steps:  Given expression: f(x) = x**3 + 2*x
        Applying differentiation rules:
        Differentiating each term separately:
          d/dx(x**3) = 3*x**2
          d/dx(2*x) = 2
        f'(x) = 3*x**2 + 2
```

### Geometry
```
Input:  area of circle radius 5
Output: 78.5398
Steps:  Given: radius r = 5
        Formula: Area = π × r²
        Area = π × 5²
        Area = π × 25
        Area = 78.5398
```

### Trigonometry
```
Input:  sin 30 degrees
Output: 1/2 ≈ 0.500000
Steps:  Given: sin(30°)
        Converting to radians: 30° × (π/180) = 0.523599 rad
        From standard values table: sin(30°) = 1/2
        Decimal approximation: 0.500000
```

### Arithmetic
```
Input:  25% of 200
Output: 50.0
Steps:  Find 25% of 200
        Formula: (percent / 100) × total
        = (25 / 100) × 200
        = 0.25 × 200
        = 50.0
```

---

## API Reference

### POST `/solve`
Solve a math problem with step-by-step explanation.

**Request:**
```json
{
  "question": "2x + 3 = 7"
}
```

**Response:**
```json
{
  "type": "algebra",
  "question": "2x + 3 = 7",
  "steps": ["Given equation: 2*x+3 = 7", "..."],
  "answer": "[2]",
  "source": "engine",
  "error": null
}
```

### GET `/history?limit=10`
Get recently solved questions from cache.

**Response:**
```json
[
  {
    "id": 1,
    "question": "2x + 3 = 7",
    "type": "algebra",
    "answer": "[2]",
    "source": "engine",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Project Structure

```
ganitha/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── parser.py          # Intent detection
│   │   │   └── dispatcher.py      # Routes to solvers
│   │   ├── solvers/
│   │   │   ├── base.py            # Abstract solver
│   │   │   ├── algebra.py         # Linear/quadratic
│   │   │   ├── calculus.py        # Derivatives/integrals
│   │   │   ├── geometry.py        # Area/perimeter/volume
│   │   │   ├── arithmetic.py      # BODMAS/fractions/%
│   │   │   └── trigonometry.py    # sin/cos/tan
│   │   ├── db/
│   │   │   ├── session.py         # SQLAlchemy setup
│   │   │   ├── models.py          # ORM models
│   │   │   └── cache.py           # Cache operations
│   │   ├── llm/
│   │   │   └── ollama_client.py   # LLM fallback
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic models
│   │   └── main.py                # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StepCard.jsx       # Solution display
│   │   │   └── HistoryPanel.jsx   # Recent questions
│   │   ├── api/
│   │   │   └── mathApi.js         # Backend client
│   │   ├── App.jsx                # Main component
│   │   └── main.jsx               # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml
```

---

## Configuration

### Environment Variables

**Backend** (`backend/.env`):
```bash
DATABASE_URL=postgresql+asyncpg://ganitha:ganitha@localhost:5432/ganitha
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5-math:1.5b
```

**Frontend** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000
```

---

## Supported Problem Types

| Type | Examples | Status |
|------|----------|--------|
| **Algebra** | Linear equations, quadratic equations | ✅ |
| **Calculus** | Derivatives, integrals | ✅ |
| **Geometry** | Area, perimeter, volume (circle, rectangle, triangle, square) | ✅ |
| **Arithmetic** | BODMAS, fractions, percentages | ✅ |
| **Trigonometry** | sin/cos/tan, inverse trig, identities | ✅ |
| **Statistics** | Mean, median, mode, standard deviation | 🔜 |
| **Matrices** | Addition, multiplication, determinant | 🔜 |
| **Probability** | Combinations, permutations | 🔜 |

---

## Performance

- **Structured solvers**: ~50-200ms (algebra, geometry, arithmetic)
- **SymPy-based solvers**: ~100-500ms (calculus, trigonometry)
- **LLM fallback**: ~2-5s (first call), ~1-2s (subsequent)
- **Cache hits**: ~10-30ms

---

## Troubleshooting

### Backend won't start
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check logs
docker-compose logs backend
```

### Ollama not responding
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Pull model manually
ollama pull qwen2.5-math:1.5b
```

### Frontend can't connect
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify proxy config in `frontend/vite.config.js`

---

## Development

### Run tests
```bash
cd backend
pytest tests/ -v
```

### Add a new solver
1. Create `backend/app/solvers/your_solver.py`
2. Inherit from `BaseSolver`
3. Implement `solve(question: str) -> SolveResponse`
4. Register in `core/dispatcher.py`
5. Add keywords to `core/parser.py`

### Database migrations
```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

---

## Roadmap

- [ ] Add statistics solver (mean, median, mode, std dev)
- [ ] Add matrix operations solver
- [ ] Add probability solver
- [ ] Implement fuzzy question matching (similar questions from cache)
- [ ] Add LaTeX rendering for math expressions
- [ ] Mobile app (React Native)
- [ ] Voice input support
- [ ] Multi-language support (Hindi, Spanish, etc.)
- [ ] Export solutions as PDF
- [ ] User accounts and saved history

---

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

---

## License

MIT License - see LICENSE file

---

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SymPy](https://www.sympy.org/)
- [Ollama](https://ollama.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## Support

For issues or questions:
- Open a GitHub issue
- Email: saikesana2010@gmail.com (placeholder)
