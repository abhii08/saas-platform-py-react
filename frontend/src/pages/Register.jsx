import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { UserPlus } from 'lucide-react'
import api from '../api/axios'

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    organization_id: '',
    role: ''
  })
  const [organizations, setOrganizations] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingOrgs, setLoadingOrgs] = useState(true)
  const { register } = useAuth()

  useEffect(() => {
    const fetchOrganizations = async () => {
      try {
        const response = await api.get('/organizations/public')
        setOrganizations(response.data)
      } catch (err) {
        setError('Failed to load organizations. Please refresh the page.')
      } finally {
        setLoadingOrgs(false)
      }
    }
    fetchOrganizations()
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!formData.organization_id) {
      setError('Please select an organization')
      return
    }
    
    if (!formData.role) {
      setError('Please select a role')
      return
    }
    
    setLoading(true)

    const result = await register({
      ...formData,
      organization_id: parseInt(formData.organization_id)
    })
    
    if (!result.success) {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2 bg-white">
      <div className="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Create your account
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-primary hover:text-primary/80">
                Sign in
              </Link>
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md bg-red-50 p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <input
                  name="first_name"
                  type="text"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="appearance-none relative block w-full px-3 py-2 border border-slate-700 placeholder-slate-300 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="First name"
                />
                <input
                  name="last_name"
                  type="text"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="appearance-none relative block w-full px-3 py-2 border border-slate-700 placeholder-slate-300 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Last name"
                />
              </div>
              <input
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-slate-700 placeholder-slate-300 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Email address"
              />
              <input
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-2 border border-slate-700 placeholder-slate-300 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Password (min 8 characters)"
              />
              <div>
                <label htmlFor="organization_id" className="block text-sm font-medium text-gray-700 mb-1">
                  Organization
                </label>
                <select
                  name="organization_id"
                  id="organization_id"
                  required
                  value={formData.organization_id}
                  onChange={handleChange}
                  disabled={loadingOrgs}
                  className="appearance-none relative block w-full px-3 py-2 border border-slate-700 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm placeholder-slate-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <option value="">Select an organization</option>
                  {organizations.map((org) => (
                    <option key={org.id} value={org.id}>
                      {org.name}
                    </option>
                  ))}
                </select>
                {loadingOrgs && (
                  <p className="text-xs text-gray-500 mt-1">Loading organizations...</p>
                )}
              </div>
              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">
                  Role
                </label>
                <select
                  name="role"
                  id="role"
                  required
                  value={formData.role}
                  onChange={handleChange}
                  className="appearance-none relative block w-full px-3 py-2 border border-slate-700 text-slate-100 bg-slate-700 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm placeholder-slate-300"
                >
                  <option value="">Select your role</option>
                  <option value="MEMBER">Member</option>
                  <option value="PROJECT_MANAGER">Project Manager</option>
                  <option value="ORG_ADMIN">Organization Admin</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  {formData.role === 'MEMBER' && 'View and contribute to assigned tasks'}
                  {formData.role === 'PROJECT_MANAGER' && 'Manage projects and teams'}
                  {formData.role === 'ORG_ADMIN' && 'Full access to organization settings'}
                  {!formData.role && 'Choose the role that best fits your responsibilities'}
                </p>
              </div>
            </div>

            <button
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-slate-900 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-800 disabled:opacity-50"
            >
              <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                <UserPlus className="h-5 w-5 text-primary-foreground" />
              </span>
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </form>
        </div>
      </div>
      <aside className="hidden md:flex items-center justify-center bg-slate-200 p-8 md:border-l md:border-slate-200">
        <div className="max-w-xl mx-auto px-6">
          <p className="text-slate-800 text-2xl md:text-3xl font-bold leading-snug">
            “Designed for multi-tenant SaaS environments, this platform ensures secure organizational separation while delivering powerful tools for tasks, roles, boards, and project operations.”
          </p>
          <div className="mt-6">
            <p className="text-slate-800 font-medium">Abhinav Sharma</p>
            <p className="text-slate-500 text-sm">CEO | TenantWorks</p>
          </div>
        </div>
      </aside>
    </div>
  )
}

export default Register
