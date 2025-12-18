import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      const userData = JSON.parse(localStorage.getItem('user') || '{}')
      setUser(userData)
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })
      const { access_token, refresh_token } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      const payload = JSON.parse(atob(access_token.split('.')[1]))
      const userData = {
        user_id: payload.user_id,
        email: payload.email,
        first_name: payload.first_name,
        last_name: payload.last_name,
        organization_id: payload.organization_id,
        role: payload.role
      }
      
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      
      navigate('/dashboard')
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const register = async (data) => {
    try {
      const response = await api.post('/auth/register', data)
      const { access_token, refresh_token, user_id, organization_id } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      const payload = JSON.parse(atob(access_token.split('.')[1]))
      const userData = {
        user_id: payload.user_id,
        email: payload.email,
        first_name: payload.first_name,
        last_name: payload.last_name,
        organization_id: payload.organization_id,
        role: payload.role
      }
      
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      
      navigate('/dashboard')
      return { success: true }
    } catch (error) {
      let errorMessage = 'Registration failed'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => err.msg).join(', ')
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      return { 
        success: false, 
        error: errorMessage
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    setUser(null)
    navigate('/login')
  }

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) throw new Error('No refresh token')
      
      const response = await api.post('/auth/refresh', { refresh_token: refresh })
      const { access_token } = response.data
      
      localStorage.setItem('access_token', access_token)
      return access_token
    } catch (error) {
      logout()
      throw error
    }
  }

  const value = {
    user,
    login,
    register,
    logout,
    refreshToken,
    loading,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'ORG_ADMIN',
    isManager: user?.role === 'PROJECT_MANAGER' || user?.role === 'ORG_ADMIN'
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
