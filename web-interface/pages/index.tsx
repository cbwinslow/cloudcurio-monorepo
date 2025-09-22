import { Inter } from 'next/font/google'
import Head from 'next/head'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>OSINT Platform Configuration</title>
        <meta name="description" content="Configure your OSINT Platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={inter.className}>
        <div className="flex min-h-screen flex-col items-center justify-center p-24">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-6">OSINT Platform Configuration</h1>
            <p className="text-lg mb-8">Manage your comprehensive OSINT platform</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold mb-3">Services</h2>
                <p>Manage all platform services</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold mb-3">Configuration</h2>
                <p>Edit platform settings and secrets</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold mb-3">Monitoring</h2>
                <p>View platform status and logs</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}