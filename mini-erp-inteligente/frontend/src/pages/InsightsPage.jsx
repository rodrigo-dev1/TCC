import { useEffect, useState } from 'react'
import api from '../services/api'

const colors = { low: 'bg-slate-100', medium: 'bg-amber-100', high: 'bg-red-100' }

export default function InsightsPage() {
  const [insights, setInsights] = useState([])

  const load = async () => {
    const { data } = await api.get('/insights')
    setInsights(data)
  }

  useEffect(() => { load() }, [])

  const generate = async () => {
    await api.post('/insights/generate')
    load()
  }

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-semibold">Insights com IA</h2>
        <button onClick={generate} className="bg-indigo-600 text-white px-3 py-2 rounded">Gerar novos insights</button>
      </div>
      <div className="space-y-3">
        {insights.map((i) => <div key={i.id} className={`rounded shadow p-4 ${colors[i.severity] || colors.low}`}><h3 className="font-semibold">{i.title}</h3><p className="text-sm">{i.description}</p></div>)}
      </div>
    </div>
  )
}
