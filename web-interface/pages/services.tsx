import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Services() {
  const [services, setServices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load services
    loadServices()
  }, [])

  const loadServices = async () => {
    try {
      // In a real implementation, this would fetch from an API
      // For now, we'll use mock data
      const mockServices = [
        { id: 1, name: 'Traefik', status: 'running', port: '80/443', description: 'Reverse Proxy' },
        { id: 2, name: 'Kong', status: 'running', port: '8000', description: 'API Gateway' },
        { id: 3, name: 'Supabase', status: 'running', port: '5432', description: 'PostgreSQL Database' },
        { id: 4, name: 'Neo4j', status: 'stopped', port: '7474', description: 'Graph Database' },
        { id: 5, name: 'Bitwarden', status: 'running', port: '8083', description: 'Secrets Management' },
        { id: 6, name: 'SearXNG', status: 'running', port: '8084', description: 'Metasearch Engine' },
        { id: 7, name: 'BeEF', status: 'running', port: '3002', description: 'Browser Exploitation Framework' },
        { id: 8, name: 'n8n', status: 'running', port: '5678', description: 'Workflow Automation' },
        { id: 9, name: 'LocalAI', status: 'running', port: '8081', description: 'Local AI Models' },
        { id: 10, name: 'OpenWebUI', status: 'running', port: '3000', description: 'AI Interface' },
      ]
      setServices(mockServices)
      setLoading(false)
    } catch (error) {
      console.error('Error loading services:', error)
      setLoading(false)
    }
  }

  const toggleService = (id: number) => {
    setServices(services.map(service => {
      if (service.id === id) {
        return { ...service, status: service.status === 'running' ? 'stopped' : 'running' }
      }
      return service
    }))
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-xl">Loading services...</div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Services - OSINT Platform</title>
        <meta name="description" content="Manage OSINT Platform Services" />
      </Head>
      <div className="min-h-screen bg-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h1 className="text-2xl font-bold text-gray-900">Platform Services</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage your OSINT platform services
              </p>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="flex flex-col">
                <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                  <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                    <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Service
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Description
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Port
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Status
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Actions
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {services.map((service) => (
                            <tr key={service.id}>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex items-center">
                                  <div className="ml-4">
                                    <div className="text-sm font-medium text-gray-900">{service.name}</div>
                                  </div>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="text-sm text-gray-900">{service.description}</div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {service.port}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${service.status === 'running' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                  {service.status}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button
                                  onClick={() => toggleService(service.id)}
                                  className="text-indigo-600 hover:text-indigo-900"
                                >
                                  {service.status === 'running' ? 'Stop' : 'Start'}
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}