import { useEffect, useState } from 'react'
import api from '../services/api'

export default function SalesPage() {
  const [sales, setSales] = useState([])
  const [products, setProducts] = useState([])

  const load = async () => {
    const [s, p] = await Promise.all([api.get('/sales'), api.get('/products')])
    setSales(s.data)
    setProducts(p.data)
  }

  useEffect(() => { load() }, [])

  const createSampleSale = async () => {
    if (!products.length) return
    await api.post('/sales', {
      payment_method: 'pix',
      status: 'completed',
      items: [{ product_id: products[0].id, quantity: 1 }]
    })
    load()
  }

  const remove = async (id) => { await api.delete(`/sales/${id}`); load() }

  return (
    <div className="space-y-4">
      <div className="flex justify-between">
        <h2 className="text-xl font-semibold">Vendas</h2>
        <button onClick={createSampleSale} className="bg-cyan-600 text-white px-3 py-2 rounded">Nova venda rápida</button>
      </div>
      <div className="bg-white rounded shadow overflow-auto">
        <table className="w-full text-sm">
          <thead className="bg-slate-50"><tr><th className="p-2">ID</th><th>Total</th><th>Pagamento</th><th>Data</th><th>Ação</th></tr></thead>
          <tbody>
            {sales.map((s) => (
              <tr key={s.id} className="border-t"><td className="p-2">{s.id}</td><td>R$ {s.total_amount}</td><td>{s.payment_method}</td><td>{new Date(s.sale_date).toLocaleDateString()}</td><td><button className="text-red-600" onClick={() => remove(s.id)}>Excluir</button></td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
