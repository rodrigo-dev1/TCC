import { useEffect, useState } from 'react'
import api from '../services/api'

export default function SettingsPage() {
  const [company, setCompany] = useState({ name: '', segment: '' })

  useEffect(() => { api.get('/company').then((r) => setCompany({ name: r.data.name, segment: r.data.segment })) }, [])

  const save = async (e) => {
    e.preventDefault()
    await api.put('/company', company)
    alert('Configurações salvas')
  }

  return (
    <form onSubmit={save} className="bg-white rounded shadow p-4 space-y-3 max-w-xl">
      <h2 className="text-xl font-semibold">Configurações da Empresa</h2>
      <input className="w-full border p-2 rounded" placeholder="Nome" value={company.name} onChange={(e) => setCompany({ ...company, name: e.target.value })} />
      <input className="w-full border p-2 rounded" placeholder="Segmento" value={company.segment} onChange={(e) => setCompany({ ...company, segment: e.target.value })} />
      <button className="bg-slate-900 text-white px-4 py-2 rounded">Salvar</button>
    </form>
  )
}
