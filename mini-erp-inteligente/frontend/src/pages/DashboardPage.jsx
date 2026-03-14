import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import KpiCard from '../components/KpiCard'
import api from '../services/api'

export default function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [charts, setCharts] = useState({ monthly_revenue: [], cash_flow: [] })
  const [insights, setInsights] = useState([])

  useEffect(() => {
    Promise.all([api.get('/dashboard/summary'), api.get('/dashboard/charts'), api.get('/insights')])
      .then(([s, c, i]) => {
        setSummary(s.data)
        setCharts(c.data)
        setInsights(i.data.slice(0, 3))
      })
  }, [])

  if (!summary) return <p>Carregando...</p>

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard title="Faturamento" value={`R$ ${summary.total_revenue.toFixed(2)}`} />
        <KpiCard title="Despesas" value={`R$ ${summary.total_expenses.toFixed(2)}`} />
        <KpiCard title="Saldo" value={`R$ ${summary.current_balance.toFixed(2)}`} />
        <KpiCard title="Ticket Médio" value={`R$ ${summary.average_ticket.toFixed(2)}`} />
        <KpiCard title="Clientes" value={summary.total_clients} />
        <KpiCard title="Vendas" value={summary.total_sales} />
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white rounded shadow p-4 h-72">
          <h3 className="font-semibold mb-2">Faturamento Mensal</h3>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={charts.monthly_revenue}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="month" /><YAxis /><Tooltip /><Line dataKey="revenue" stroke="#0891b2" /></LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded shadow p-4 h-72">
          <h3 className="font-semibold mb-2">Entradas x Saídas</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={charts.cash_flow}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="month" /><YAxis /><Tooltip /><Legend /><Bar dataKey="income" fill="#16a34a" /><Bar dataKey="expense" fill="#dc2626" /></BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <h3 className="font-semibold mb-2">Insights recentes</h3>
        {insights.map((ins) => <p key={ins.id} className="text-sm mb-2">• {ins.title}: {ins.description}</p>)}
      </div>
    </div>
  )
}
