import { describe, it, expect, vi } from 'vitest'
import { NextRequest } from 'next/server'
import { GET, POST } from '@/app/api/scripts/route'

vi.mock('@prisma/client', () => ({
  PrismaClient: vi.fn(() => ({
    script: {
      findMany: vi.fn(),
      upsert: vi.fn(),
    },
  })),
}))
vi.mock('next-auth/jwt', () => ({ decode: vi.fn() }))

describe('Scripts API', () => {
  it('GET should list scripts', async () => {
    const mockScripts = [{ slug: 'test', content: 'echo hi' }]
    vi.mocked((global as any).prisma.script.findMany).mockResolvedValue(mockScripts)
    const req = new NextRequest('http://localhost/api/scripts', { method: 'GET' }) as any
    const res = await GET(req)

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data).toHaveLength(1)
  })

  it('POST should create script (admin)', async () => {
    vi.mocked(decode).mockResolvedValue({ role: 'admin' })
    const req = new NextRequest('http://localhost/api/scripts', {
      method: 'POST',
      body: JSON.stringify({ slug: 'test', content: 'echo hi' }),
    }) as any
    const res = await POST(req)

    expect(res.status).toBe(201)
  })

  it('POST should reject non-admin', async () => {
    vi.mocked(decode).mockResolvedValue({ role: 'member' })
    const req = new NextRequest('http://localhost/api/scripts', {
      method: 'POST',
      body: JSON.stringify({ slug: 'test', content: 'echo hi' }),
    }) as any
    const res = await POST(req)

    expect(res.status).toBe(403)
  })
})
