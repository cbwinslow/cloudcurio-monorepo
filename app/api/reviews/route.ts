import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { validateRequest, reviewJobSchema } from '@/lib/validation';
import { rateLimit } from '@/lib/rate-limit';

export const runtime = 'nodejs';

// Rate limit: 10 requests per minute per IP
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10
});

export async function POST(req: Request) {
  // Apply rate limiting
  const rateLimitCheck = await limiter(req);
  if (rateLimitCheck.limited) {
    return rateLimitCheck.response;
  }

  const session = await getServerSession(authOptions);
  if (!session || (session.user as any)?.role !== 'admin') 
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });

  const body = await req.json();
  const validation = validateRequest(reviewJobSchema, body);
  
  if (!validation.success) {
    return validation.error;
  }
  
  const { repoUrl, klass } = validation.data;

  const job = await prisma.reviewJob.create({ 
    data: { 
      repoUrl, 
      meta: { class: klass } 
    } 
  });
  
  const response = NextResponse.json({ job });
  
  // Add rate limit headers to response
  if (rateLimitCheck.headers) {
    Object.entries(rateLimitCheck.headers).forEach(([key, value]) => {
      response.headers.set(key, value);
    });
  }
  
  return response;
}

export async function GET() {
  const jobs = await prisma.reviewJob.findMany({ 
    orderBy: { createdAt: 'desc' }, 
    take: 50 
  });
  
  return NextResponse.json({ jobs });
}
