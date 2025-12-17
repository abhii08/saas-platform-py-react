import { useState, useEffect } from 'react'
import { X } from 'lucide-react'

const TaskModal = ({ isOpen, onClose, onSubmit, task = null, boards = [], users = [] }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    board_id: '',
    status: 'TODO',
    priority: 'MEDIUM',
    assigned_to: '',
    due_date: '',
    position: 0
  })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        board_id: task.board_id || '',
        status: task.status || 'TODO',
        priority: task.priority || 'MEDIUM',
        assigned_to: task.assigned_to || '',
        due_date: task.due_date ? task.due_date.split('T')[0] : '',
        position: task.position || 0
      })
    } else {
      setFormData({
        title: '',
        description: '',
        board_id: boards.length > 0 ? boards[0].id : '',
        status: 'TODO',
        priority: 'MEDIUM',
        assigned_to: '',
        due_date: '',
        position: 0
      })
    }
  }, [task, boards, isOpen])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}
    
    if (!formData.title.trim()) {
      newErrors.title = 'Task title is required'
    }
    
    if (!formData.board_id) {
      newErrors.board_id = 'Please select a board'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validate()) {
      return
    }

    try {
      // Build submit data, only including fields with actual values
      const submitData = {
        title: formData.title,
        description: formData.description || null,
        board_id: parseInt(formData.board_id),
        status: formData.status,
        priority: formData.priority,
        assigned_to: formData.assigned_to ? parseInt(formData.assigned_to) : null,
        due_date: formData.due_date ? `${formData.due_date}T00:00:00` : null,
        position: formData.position || 0
      }
      
      // Remove null/undefined values for update operations (when task exists)
      if (task) {
        Object.keys(submitData).forEach(key => {
          if (submitData[key] === null || submitData[key] === undefined || submitData[key] === '') {
            delete submitData[key]
          }
        })
      }
      
      console.log('Submitting task data:', submitData)
      await onSubmit(submitData)
      onClose()
    } catch (error) {
      console.error('Task submission error:', error)
      console.error('Error response data:', error.response?.data)
      let errorMessage = 'An error occurred. Please try again.'
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail
        console.log('Validation error detail:', detail)
        // Handle FastAPI validation errors (array of error objects)
        if (Array.isArray(detail)) {
          errorMessage = detail.map(err => err.msg || JSON.stringify(err)).join(', ')
        } else if (typeof detail === 'string') {
          errorMessage = detail
        } else if (typeof detail === 'object') {
          errorMessage = JSON.stringify(detail)
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      setErrors({ submit: errorMessage })
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onClick={onClose}></div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {task ? 'Edit Task' : 'Create New Task'}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Task Title *
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm sm:text-sm ${
                    errors.title
                      ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                      : 'border-gray-300 focus:border-primary focus:ring-primary'
                  }`}
                  placeholder="Design homepage mockup"
                />
                {errors.title && (
                  <p className="mt-1 text-sm text-red-600">{errors.title}</p>
                )}
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  rows="3"
                  value={formData.description}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  placeholder="Describe the task..."
                />
              </div>

              <div>
                <label htmlFor="board_id" className="block text-sm font-medium text-gray-700">
                  Board *
                </label>
                <select
                  id="board_id"
                  name="board_id"
                  value={formData.board_id}
                  onChange={handleChange}
                  className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm sm:text-sm ${
                    errors.board_id
                      ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                      : 'border-gray-300 focus:border-primary focus:ring-primary'
                  }`}
                >
                  <option value="">Select a board</option>
                  {boards.map(board => (
                    <option key={board.id} value={board.id}>
                      {board.name}
                    </option>
                  ))}
                </select>
                {errors.board_id && (
                  <p className="mt-1 text-sm text-red-600">{errors.board_id}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                    Status
                  </label>
                  <select
                    id="status"
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  >
                    <option value="TODO">To Do</option>
                    <option value="IN_PROGRESS">In Progress</option>
                    <option value="IN_REVIEW">In Review</option>
                    <option value="DONE">Done</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
                    Priority
                  </label>
                  <select
                    id="priority"
                    name="priority"
                    value={formData.priority}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  >
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                    <option value="URGENT">Urgent</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="assigned_to" className="block text-sm font-medium text-gray-700">
                  Assign To
                </label>
                <select
                  id="assigned_to"
                  name="assigned_to"
                  value={formData.assigned_to}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                >
                  <option value="">Unassigned</option>
                  {users.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.first_name} {user.last_name} ({user.email})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="due_date" className="block text-sm font-medium text-gray-700">
                  Due Date
                </label>
                <input
                  type="date"
                  id="due_date"
                  name="due_date"
                  value={formData.due_date}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                />
              </div>

              {errors.submit && (
                <div className="rounded-md bg-red-50 p-4">
                  <p className="text-sm text-red-800">{errors.submit}</p>
                </div>
              )}

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md hover:bg-primary/90"
                >
                  {task ? 'Update Task' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TaskModal
