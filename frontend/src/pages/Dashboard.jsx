import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'
import { FolderKanban, CheckSquare, Users, TrendingUp } from 'lucide-react'

const Dashboard = () => {
  const { user, isManager } = useAuth()
  const [stats, setStats] = useState({
    projects: 0,
    tasks: 0,
    members: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [projectsRes] = await Promise.all([
          api.get('/projects?page=1&page_size=1')
        ])
        
        setStats({
          projects: projectsRes.data.total || 0,
          tasks: 0,
          members: 0
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  const statCards = [
    { title: 'Total Projects', value: stats.projects, icon: FolderKanban, color: 'bg-blue-500' },
    { title: 'Active Tasks', value: stats.tasks, icon: CheckSquare, color: 'bg-green-500' },
    { title: 'Team Members', value: stats.members, icon: Users, color: 'bg-purple-500' },
    { title: 'Completion Rate', value: '0%', icon: TrendingUp, color: 'bg-orange-500' }
  ]

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">Welcome back, {user?.email}</p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {statCards.map((stat, index) => (
            <div key={index} className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className={`flex-shrink-0 ${stat.color} rounded-md p-3`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.title}
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        {loading ? '...' : stat.value}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className={`grid grid-cols-1 gap-4 ${isManager ? 'sm:grid-cols-3' : 'sm:grid-cols-2'}`}>
            {isManager && (
              <button className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary/90">
                Create New Project
              </button>
            )}
            <button className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Add Task
            </button>
            {isManager && (
              <button className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Invite Team Member
              </button>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
