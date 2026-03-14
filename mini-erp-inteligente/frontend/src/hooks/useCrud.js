import { useEffect, useState } from 'react'
import api from '../services/api'

export function useCrud(endpoint) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const response = await api.get(endpoint)
      setData(response.data)
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [endpoint])

  return { data, setData, loading, error, reload: load }
}
