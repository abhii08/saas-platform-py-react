import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LayoutDashboard, FolderKanban, CheckSquare, LogOut, Menu } from 'lucide-react'
import { useState } from 'react'

const Layout = ({ children }) => {
  const { user, logout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#EEF1F5' }}>
      <nav className="bg-white border-b border-gray-200 fixed w-full z-30 top-0">
        <div className="px-3 py-3 lg:px-5 lg:pl-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center justify-start">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 text-gray-600 rounded cursor-pointer lg:hidden hover:text-gray-900 hover:bg-gray-100"
              >
                <Menu className="w-6 h-6" />
              </button>
              <Link to="/dashboard" className="flex ml-2 md:mr-24">
                <span className="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap text-primary">
                  SaaS Platform
                </span>
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-700">
                <span className="font-medium">{user?.email}</span>
                <span className="ml-2 px-2 py-1 text-xs bg-primary/10 text-primary rounded">
                  {user?.role}
                </span>
              </div>
              <button
                onClick={logout}
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <aside
        className={`fixed top-0 left-0 z-20 w-64 h-screen pt-20 transition-transform ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } border-r border-gray-200 lg:translate-x-0`}
        style={{ backgroundColor: '#F7F9FC' }}
      >
        <div className="h-full px-3 pb-4 overflow-y-auto" style={{ backgroundColor: '#F7F9FC' }}>
          <ul className="space-y-2 font-medium">
            <li>
              <Link
                to="/dashboard"
                className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              >
                <LayoutDashboard className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
                <span className="ml-3">Dashboard</span>
              </Link>
            </li>
            <li>
              <Link
                to="/projects"
                className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              >
                <FolderKanban className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
                <span className="ml-3">Projects</span>
              </Link>
            </li>
            <li>
              <Link
                to="/tasks"
                className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              >
                <CheckSquare className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
                <span className="ml-3">Tasks</span>
              </Link>
            </li>
          </ul>
        </div>
      </aside>

      <div className={`p-4 ${sidebarOpen ? 'lg:ml-64' : ''} mt-14`}>
        <div className="p-4 rounded-lg">
          {children}
        </div>
      </div>
    </div>
  )
}

export default Layout
