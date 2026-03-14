import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function LoginPage() {
  const navigate = useNavigate()

  const handleLogin = async () => {
    const payload = { google_id: 'dev-google-id', email: 'admin@mini-erp.com', name: 'Admin' }
    const { data } = await api.post('/auth/google', payload)
    localStorage.setItem('mini-erp-user', JSON.stringify(data.user))
    localStorage.setItem('mini-erp-token', data.token)
    navigate('/dashboard')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-cyan-500 to-indigo-700 p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-sm text-center">
        <h1 className="text-2xl font-bold mb-2">Mini ERP Inteligente</h1>
        <p className="text-slate-500 mb-6">Gestão e insights para pequenos negócios</p>
        <button onClick={handleLogin} className="w-full bg-slate-900 text-white py-2 rounded">Entrar com Google</button>
      </div>
    </div>
  )
}
