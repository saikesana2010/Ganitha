import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const solveMath = (question) =>
  api.post('/solve', { question }).then(r => r.data)

export const getHistory = (limit = 10) =>
  api.get(`/history?limit=${limit}`).then(r => r.data)
