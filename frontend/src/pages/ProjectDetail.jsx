import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import ProjectModal from '../components/ProjectModal'
import TaskModal from '../components/TaskModal'
import api from '../api/axios'
import { Edit, Trash2, Plus, CheckSquare } from 'lucide-react'

const ProjectDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isManager } = useAuth()
  const [project, setProject] = useState(null)
  const [boards, setBoards] = useState([])
  const [tasks, setTasks] = useState({})
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState(null)
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
  const [selectedTask, setSelectedTask] = useState(null)

  useEffect(() => {
    fetchProject()
    fetchBoards()
    fetchUsers()
  }, [id])

  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${id}`)
      setProject(response.data)
    } catch (error) {
      console.error('Error fetching project:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchBoards = async () => {
    try {
      const response = await api.get(`/boards/project/${id}`)
      setBoards(response.data)
      response.data.forEach(board => {
        fetchTasksForBoard(board.id)
      })
    } catch (error) {
      console.error('Error fetching boards:', error)
    }
  }

  const fetchTasksForBoard = async (boardId) => {
    try {
      const response = await api.get(`/tasks/board/${boardId}`)
      setTasks(prev => ({ ...prev, [boardId]: response.data }))
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users')
      setUsers(response.data.items || [])
    } catch (error) {
      console.error('Error fetching users:', error)
    }
  }

  const handleUpdateProject = async (formData) => {
    await api.put(`/projects/${id}`, formData)
    fetchProject()
  }

  const handleDeleteProject = async () => {
    setIsDeleting(true)
    setDeleteError(null)
    try {
      await api.delete(`/projects/${id}`)
      navigate('/projects')
    } catch (error) {
      console.error('Error deleting project:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete project. Please try again.'
      setDeleteError(errorMessage)
      setIsDeleting(false)
    }
  }

  const handleCreateTask = async (formData) => {
    await api.post('/tasks', formData)
    fetchTasksForBoard(formData.board_id)
  }

  const handleUpdateTask = async (formData) => {
    await api.put(`/tasks/${selectedTask.id}`, formData)
    fetchTasksForBoard(formData.board_id)
    setSelectedTask(null)
  }

  const handleDeleteTask = async (taskId, boardId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await api.delete(`/tasks/${taskId}`)
        fetchTasksForBoard(boardId)
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
      DONE: 'bg-green-100 text-green-800'
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

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </Layout>
    )
  }

  if (!project) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">Project not found</h3>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
            <p className="mt-2 text-gray-600">{project.description}</p>
          </div>
          {isManager && (
            <div className="flex gap-2">
              <button
                onClick={() => setIsEditModalOpen(true)}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <Edit className="w-4 h-4" />
                Edit
              </button>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700"
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </div>
          )}
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Details</h2>
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {project.is_active ? 'Active' : 'Inactive'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Created</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {new Date(project.created_at).toLocaleDateString()}
              </dd>
            </div>
          </dl>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Tasks</h2>
            <button
              onClick={() => {
                console.log('Opening task modal, boards:', boards)
                console.log('Boards length:', boards.length)
                setSelectedTask(null)
                setIsTaskModalOpen(true)
              }}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-primary/90"
            >
              <Plus className="w-4 h-4" />
              New Task
            </button>
          </div>

          {boards.length === 0 ? (
            <div className="text-center py-8">
              <CheckSquare className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-500">No boards found. Create boards to organize tasks.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {boards.map(board => (
                <div key={board.id} className="border rounded-lg p-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">{board.name}</h3>
                  {board.description && (
                    <p className="text-sm text-gray-500 mb-3">{board.description}</p>
                  )}
                  <div className="space-y-2">
                    {tasks[board.id]?.length > 0 ? (
                      tasks[board.id].map(task => (
                        <div
                          key={task.id}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer"
                          onClick={() => {
                            setSelectedTask(task)
                            setIsTaskModalOpen(true)
                          }}
                        >
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <h4 className="text-sm font-medium text-gray-900">{task.title}</h4>
                              <span className={`px-2 py-1 text-xs rounded ${getStatusColor(task.status)}`}>
                                {task.status.replace('_', ' ')}
                              </span>
                              <span className={`px-2 py-1 text-xs rounded ${getPriorityColor(task.priority)}`}>
                                {task.priority}
                              </span>
                            </div>
                            {task.description && (
                              <p className="text-xs text-gray-500 mt-1">{task.description}</p>
                            )}
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              handleDeleteTask(task.id, board.id)
                            }}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500 text-center py-4">No tasks in this board</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <ProjectModal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        onSubmit={handleUpdateProject}
        project={project}
      />

      <TaskModal
        isOpen={isTaskModalOpen}
        onClose={() => {
          setIsTaskModalOpen(false)
          setSelectedTask(null)
        }}
        onSubmit={selectedTask ? handleUpdateTask : handleCreateTask}
        task={selectedTask}
        boards={boards}
        users={users}
      />

      {showDeleteConfirm && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onClick={() => setShowDeleteConfirm(false)}></div>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                    <Trash2 className="h-6 w-6 text-red-600" />
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                      Delete Project
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        Are you sure you want to delete "{project.name}"? This action cannot be undone.
                      </p>
                      {deleteError && (
                        <div className="mt-3 rounded-md bg-red-50 p-3">
                          <p className="text-sm text-red-800">{deleteError}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={handleDeleteProject}
                  disabled={isDeleting}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed sm:ml-3 sm:w-auto sm:text-sm"
                >
                  {isDeleting ? 'Deleting...' : 'Delete'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowDeleteConfirm(false)
                    setDeleteError(null)
                  }}
                  disabled={isDeleting}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}

export default ProjectDetail
