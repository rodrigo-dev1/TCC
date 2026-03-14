import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
})

api.interceptors.request.use((config) => {
  const user = JSON.parse(localStorage.getItem('mini-erp-user') || '{}')
  config.headers['X-User-Id'] = user.id || 1
  return config
})

export default api
