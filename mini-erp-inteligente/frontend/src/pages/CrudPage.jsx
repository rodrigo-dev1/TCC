import { useMemo, useState } from 'react'
import DataTable from '../components/DataTable'
import FormModal from '../components/FormModal'
import { useCrud } from '../hooks/useCrud'
import api from '../services/api'

export default function CrudPage({ title, endpoint, fields }) {
  const { data, reload, loading } = useCrud(endpoint)
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({})

  const columns = useMemo(() => fields.slice(0, 4).map(([key, label]) => ({ key, label })), [fields])

  const toPayload = (obj) => {
    const parsed = { ...obj }
    if ('price' in parsed) parsed.price = Number(parsed.price || 0)
    if ('stock_quantity' in parsed) parsed.stock_quantity = Number(parsed.stock_quantity || 0)
    if ('amount' in parsed) parsed.amount = Number(parsed.amount || 0)
    if ('active' in parsed) parsed.active = parsed.active === 'true' || parsed.active === true
    return parsed
  }

  const submit = async (e) => {
    e.preventDefault()
    const payload = toPayload(form)
    if (editing) await api.put(`${endpoint}/${editing.id}`, payload)
    else await api.post(endpoint, payload)
    setOpen(false); setEditing(null); setForm({}); reload()
  }

  const remove = async (id) => { await api.delete(`${endpoint}/${id}`); reload() }

  return (
    <div className="space-y-4">
      <div className="flex justify-between"><h2 className="text-xl font-semibold">{title}</h2><button onClick={() => setOpen(true)} className="bg-cyan-600 text-white px-3 py-2 rounded">Novo</button></div>
      {loading ? <p>Carregando...</p> : <DataTable columns={columns} data={data} onEdit={(row) => { setEditing(row); setForm(row); setOpen(true) }} onDelete={remove} />}
      {open && (
        <FormModal title={editing ? `Editar ${title}` : `Novo ${title}`} onClose={() => { setOpen(false); setEditing(null) }}>
          <form onSubmit={submit} className="space-y-2">
            {fields.map(([key, label]) => <input key={key} className="w-full border p-2 rounded" placeholder={label} value={form[key] ?? ''} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />)}
            <button className="bg-slate-900 text-white px-4 py-2 rounded">Salvar</button>
          </form>
        </FormModal>
      )}
    </div>
  )
}
