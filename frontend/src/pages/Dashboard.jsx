import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import ProjectModal from '../components/ProjectModal'
import TaskModal from '../components/TaskModal'
import api from '../api/axios'
import { FolderKanban, CheckSquare, Users } from 'lucide-react'

const Dashboard = () => {
  const { user, isManager } = useAuth()
  const [stats, setStats] = useState({
    projects: 0,
    tasks: 0,
    members: 0
  })
  const [loading, setLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
  const [boards, setBoards] = useState([])
  const [users, setUsers] = useState([])

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const [projectsRes, usersRes] = await Promise.all([
        api.get('/projects?page=1&page_size=1'),
        api.get('/users?page=1&page_size=100')
      ])
      
      const projectsList = await api.get('/projects?page=1&page_size=100')
      const allProjects = projectsList.data.items || []

      let totalTasks = 0
      const allBoards = []

      for (const project of allProjects) {
        try {
          const boardsRes = await api.get(`/boards/project/${project.id}`)
          const projectBoards = boardsRes.data || []
          allBoards.push(...projectBoards)

          for (const board of projectBoards) {
            try {
              const tasksRes = await api.get(`/tasks/board/${board.id}`)
              const activeTasks = (tasksRes.data || []).filter(task => 
                task.status !== 'DONE'
              )
              totalTasks += activeTasks.length
            } catch (error) {
              console.error(`Error fetching tasks for board ${board.id}:`, error)
            }
          }
        } catch (error) {
          console.error(`Error fetching boards for project ${project.id}:`, error)
        }
      }

      setBoards(allBoards)
      setUsers(usersRes.data.items || [])
      setStats({
        projects: projectsRes.data.total || 0,
        tasks: totalTasks,
        members: usersRes.data.total || 0
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (formData) => {
    await api.post('/projects', formData)
    fetchStats()
  }

  const handleCreateTask = async (formData) => {
    await api.post('/tasks', formData)
    fetchStats()
  }

  const statCards = [
    { title: 'Total Projects', value: stats.projects, icon: FolderKanban, color: 'bg-blue-500' },
    { title: 'Active Tasks', value: stats.tasks, icon: CheckSquare, color: 'bg-green-500' },
    { title: 'Team Members', value: stats.members, icon: Users, color: 'bg-purple-500' }
  ]

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Welcome back, <span className="font-bold">{user?.first_name && user?.last_name 
              ? `${user.first_name} ${user.last_name}` 
              : user?.email}</span>
          </p>
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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {isManager && (
              <button 
                onClick={() => setIsModalOpen(true)}
                className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary/90"
              >
                Create New Project
              </button>
            )}
            <button 
              onClick={() => setIsTaskModalOpen(true)}
              disabled={boards.length === 0}
              className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              title={boards.length === 0 ? 'Create a project and board first' : 'Add a new task'}
            >
              Add Task
            </button>
          </div>
        </div>
      </div>

      <ProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateProject}
      />

      <TaskModal
        isOpen={isTaskModalOpen}
        onClose={() => setIsTaskModalOpen(false)}
        onSubmit={handleCreateTask}
        task={null}
        boards={boards}
        users={users}
      />
    </Layout>
  )
}

export default Dashboard
