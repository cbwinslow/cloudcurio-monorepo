import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Configuration() {
  const [config, setConfig] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    // Load configuration
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      // In a real implementation, this would fetch from an API
      // For now, we'll use a mock configuration
      const mockConfig = {
        platform: {
          name: "OSINT Platform",
          version: "1.0.0",
          environment: "production"
        },
        network: {
          domain: "osint.local",
          ssl_enabled: true,
          lets_encrypt_email: "admin@osint.local"
        },
        databases: {
          supabase: {
            host: "supabase-db",
            port: 5432,
            database: "supabase",
            username: "supabase",
            password: "supabase123"
          },
          neo4j: {
            host: "neo4j",
            port: 7687,
            username: "neo4j",
            password: "neo4j123"
          }
        }
      }
      setConfig(mockConfig)
      setLoading(false)
    } catch (error) {
      console.error('Error loading configuration:', error)
      setLoading(false)
    }
  }

  const saveConfig = async () => {
    setSaving(true)
    try {
      // In a real implementation, this would save to an API
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSaving(false)
      alert('Configuration saved successfully!')
    } catch (error) {
      console.error('Error saving configuration:', error)
      setSaving(false)
      alert('Error saving configuration')
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-xl">Loading configuration...</div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Configuration - OSINT Platform</title>
        <meta name="description" content="Configure your OSINT Platform" />
      </Head>
      <div className="min-h-screen bg-gray-100 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h1 className="text-2xl font-bold text-gray-900">Platform Configuration</h1>
              <p className="mt-1 text-sm text-gray-500">
                Configure your OSINT platform settings
              </p>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-8">
                {/* Platform Settings */}
                <div>
                  <h2 className="text-lg font-medium text-gray-900">Platform Settings</h2>
                  <div className="mt-4 space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Platform Name</label>
                      <input
                        type="text"
                        value={config?.platform?.name || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          platform: {
                            ...config?.platform,
                            name: e.target.value
                          }
                        })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Environment</label>
                      <select
                        value={config?.platform?.environment || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          platform: {
                            ...config?.platform,
                            environment: e.target.value
                          }
                        })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      >
                        <option value="development">Development</option>
                        <option value="staging">Staging</option>
                        <option value="production">Production</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Network Settings */}
                <div>
                  <h2 className="text-lg font-medium text-gray-900">Network Settings</h2>
                  <div className="mt-4 space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Domain</label>
                      <input
                        type="text"
                        value={config?.network?.domain || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          network: {
                            ...config?.network,
                            domain: e.target.value
                          }
                        })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      />
                    </div>
                    <div className="flex items-center">
                      <input
                        id="ssl-enabled"
                        type="checkbox"
                        checked={config?.network?.ssl_enabled || false}
                        onChange={(e) => setConfig({
                          ...config,
                          network: {
                            ...config?.network,
                            ssl_enabled: e.target.checked
                          }
                        })}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <label htmlFor="ssl-enabled" className="ml-2 block text-sm text-gray-900">
                        Enable SSL
                      </label>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Let's Encrypt Email</label>
                      <input
                        type="email"
                        value={config?.network?.lets_encrypt_email || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          network: {
                            ...config?.network,
                            lets_encrypt_email: e.target.value
                          }
                        })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      />
                    </div>
                  </div>
                </div>

                {/* Database Settings */}
                <div>
                  <h2 className="text-lg font-medium text-gray-900">Database Settings</h2>
                  <div className="mt-4 space-y-6">
                    {/* Supabase */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-md font-medium text-gray-900">Supabase</h3>
                      <div className="mt-3 space-y-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Host</label>
                          <input
                            type="text"
                            value={config?.databases?.supabase?.host || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                supabase: {
                                  ...config?.databases?.supabase,
                                  host: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Port</label>
                          <input
                            type="number"
                            value={config?.databases?.supabase?.port || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                supabase: {
                                  ...config?.databases?.supabase,
                                  port: parseInt(e.target.value)
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Database</label>
                          <input
                            type="text"
                            value={config?.databases?.supabase?.database || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                supabase: {
                                  ...config?.databases?.supabase,
                                  database: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Username</label>
                          <input
                            type="text"
                            value={config?.databases?.supabase?.username || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                supabase: {
                                  ...config?.databases?.supabase,
                                  username: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Password</label>
                          <input
                            type="password"
                            value={config?.databases?.supabase?.password || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                supabase: {
                                  ...config?.databases?.supabase,
                                  password: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Neo4j */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-md font-medium text-gray-900">Neo4j</h3>
                      <div className="mt-3 space-y-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Host</label>
                          <input
                            type="text"
                            value={config?.databases?.neo4j?.host || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                neo4j: {
                                  ...config?.databases?.neo4j,
                                  host: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Port</label>
                          <input
                            type="number"
                            value={config?.databases?.neo4j?.port || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                neo4j: {
                                  ...config?.databases?.neo4j,
                                  port: parseInt(e.target.value)
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Username</label>
                          <input
                            type="text"
                            value={config?.databases?.neo4j?.username || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                neo4j: {
                                  ...config?.databases?.neo4j,
                                  username: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Password</label>
                          <input
                            type="password"
                            value={config?.databases?.neo4j?.password || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              databases: {
                                ...config?.databases,
                                neo4j: {
                                  ...config?.databases?.neo4j,
                                  password: e.target.value
                                }
                              }
                            })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-8 flex justify-end">
                <button
                  type="button"
                  onClick={saveConfig}
                  disabled={saving}
                  className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Configuration'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}