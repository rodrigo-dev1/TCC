import { Link, Outlet } from 'react-router-dom'

const links = [
  ['Dashboard', '/dashboard'],
  ['Clientes', '/clients'],
  ['Produtos', '/products'],
  ['Vendas', '/sales'],
  ['Fluxo de Caixa', '/cash-flow'],
  ['Insights', '/insights'],
  ['Configurações', '/settings']
]

export default function AppLayout() {
  return (
    <div className="min-h-screen flex">
      <aside className="w-60 bg-slate-900 text-white p-4 hidden md:block">
        <h1 className="text-lg font-bold mb-6">Mini ERP</h1>
        <nav className="flex flex-col gap-2">
          {links.map(([label, href]) => <Link key={href} to={href} className="hover:text-cyan-300">{label}</Link>)}
        </nav>
      </aside>
      <main className="flex-1 p-4">
        <header className="mb-4 bg-white rounded shadow p-3">Mini ERP Inteligente</header>
        <Outlet />
      </main>
    </div>
  )
}
