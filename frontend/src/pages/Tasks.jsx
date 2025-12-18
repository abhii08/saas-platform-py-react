import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import TaskModal from '../components/TaskModal'
import api from '../api/axios'
import { CheckSquare, Edit, Trash2 } from 'lucide-react'

const Tasks = () => {
  const navigate = useNavigate()
  const { isManager, role } = useAuth()
  const [tasks, setTasks] = useState([])
  const [projects, setProjects] = useState([])
  const [boards, setBoards] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTask, setSelectedTask] = useState(null)
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
  const [filterStatus, setFilterStatus] = useState('all')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [projectsRes, usersRes] = await Promise.all([
        api.get('/projects'),
        api.get('/users')
      ])
      
      const projectsList = projectsRes.data.items || []
      setProjects(projectsList)
      setUsers(usersRes.data.items || [])

      const allBoards = []
      const allTasks = []

      for (const project of projectsList) {
        try {
          const boardsRes = await api.get(`/boards/project/${project.id}`)
          const projectBoards = boardsRes.data || []
          allBoards.push(...projectBoards)

          for (const board of projectBoards) {
            try {
              const tasksRes = await api.get(`/tasks/board/${board.id}`)
              const boardTasks = (tasksRes.data || []).map(task => ({
                ...task,
                boardName: board.name,
                projectName: project.name,
                projectId: project.id
              }))
              allTasks.push(...boardTasks)
            } catch (error) {
              console.error(`Error fetching tasks for board ${board.id}:`, error)
            }
          }
        } catch (error) {
          console.error(`Error fetching boards for project ${project.id}:`, error)
        }
      }

      setBoards(allBoards)
      setTasks(allTasks)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateTask = async (formData) => {
    await api.put(`/tasks/${selectedTask.id}`, formData)
    fetchData()
    setSelectedTask(null)
  }

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await api.delete(`/tasks/${taskId}`)
        fetchData()
      } catch (error) {
        console.error('Error deleting task:', error)
      }
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      TODO: 'bg-gray-100 text-gray-800',
      IN_PROGRESS: 'bg-blue-100 text-blue-800',
      IN_REVIEW: 'bg-yellow-100 text-yellow-800',
      DONE: 'bg-green-100 text-green-800',
      BLOCKED: 'bg-red-100 text-red-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getPriorityColor = (priority) => {
    const colors = {
      LOW: 'bg-gray-100 text-gray-600',
      MEDIUM: 'bg-blue-100 text-blue-600',
      HIGH: 'bg-orange-100 text-orange-600',
      URGENT: 'bg-red-100 text-red-600'
    }
    return colors[priority] || 'bg-gray-100 text-gray-600'
  }

  const filteredTasks = filterStatus === 'all' 
    ? tasks 
    : tasks.filter(task => task.status === filterStatus)

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          <div className="flex gap-2">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="all">All Tasks</option>
              <option value="TODO">To Do</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="IN_REVIEW">In Review</option>
              <option value="DONE">Done</option>
              <option value="BLOCKED">Blocked</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <CheckSquare className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
            <p className="mt-1 text-sm text-gray-500">Tasks will appear here once you create them in projects.</p>
          </div>
        ) : (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="divide-y divide-gray-200">
              {filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className="p-4 hover:bg-gray-50 cursor-pointer"
                  onClick={() => {
                    setSelectedTask(task)
                    setIsTaskModalOpen(true)
                  }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-medium text-gray-900">{task.title}</h3>
                        <span className={`px-2 py-1 text-xs rounded ${getStatusColor(task.status)}`}>
                          {task.status.replace('_', ' ')}
                        </span>
                        <span className={`px-2 py-1 text-xs rounded ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                      </div>
                      {task.description && (
                        <p className="text-sm text-gray-600 mb-2">{task.description}</p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span 
                          className="hover:text-primary cursor-pointer"
                          onClick={(e) => {
                            e.stopPropagation()
                            navigate(`/projects/${task.projectId}`)
                          }}
                        >
                          📁 {task.projectName}
                        </span>
                        <span>📋 {task.boardName}</span>
                        {task.due_date && (
                          <span>📅 {new Date(task.due_date).toLocaleDateString()}</span>
                        )}
                      </div>
                    </div>
                    {isManager && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteTask(task.id)
                        }}
                        className="text-red-600 hover:text-red-800 ml-4"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <TaskModal
        isOpen={isTaskModalOpen}
        onClose={() => {
          setIsTaskModalOpen(false)
          setSelectedTask(null)
        }}
        onSubmit={handleUpdateTask}
        task={selectedTask}
        boards={boards}
        users={users}
      />
    </Layout>
  )
}

export default Tasks
