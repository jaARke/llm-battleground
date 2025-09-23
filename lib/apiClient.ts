import axios from 'axios'
import { getSession } from 'next-auth/react'

const apiClient = axios.create()

apiClient.interceptors.request.use(
  async (config) => {
    const session = await getSession()
    console.log('Current session in interceptor:', session)
    if (session?.accessToken) {
      config.headers.Authorization = `Bearer ${session.accessToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default apiClient
