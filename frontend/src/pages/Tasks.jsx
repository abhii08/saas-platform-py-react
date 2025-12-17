import Layout from '../components/Layout'
import { CheckSquare } from 'lucide-react'

const Tasks = () => {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
        </div>

        <div className="text-center py-12 bg-white rounded-lg shadow">
          <CheckSquare className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Tasks will appear here once you create them in projects.</p>
        </div>
      </div>
    </Layout>
  )
}

export default Tasks
