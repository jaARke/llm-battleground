import axios from 'axios'
import { getSession } from 'next-auth/react'

const fastApiClient = axios.create({ baseURL: '/api/py' })

fastApiClient.interceptors.request.use(
  async (config) => {
    const session = await getSession()
    if (session?.fastApiToken) {
      config.headers.Authorization = `Bearer ${session.fastApiToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default fastApiClient
