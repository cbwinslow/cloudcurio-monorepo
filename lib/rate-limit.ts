import { NextResponse } from 'next/server';

// Simple in-memory store for rate limiting
// In production, you would use Redis or another distributed store
const rateLimitStore = new Map<string, { count: number; resetTime: number }>();

export interface RateLimitOptions {
  windowMs: number; // Time window in milliseconds
  max: number;      // Maximum requests in the window
  keyGenerator?: (req: Request) => string; // Function to generate a key
}

export function rateLimit(options: RateLimitOptions) {
  const { windowMs, max, keyGenerator } = options;

  return async function (req: Request) {
    // Generate key based on IP address or custom function
    const key = keyGenerator 
      ? keyGenerator(req) 
      : req.headers.get('x-forwarded-for') || 'anonymous';

    const now = Date.now();
    const windowStart = now - windowMs;

    // Get or create rate limit info for this key
    let rateLimitInfo = rateLimitStore.get(key);
    
    if (!rateLimitInfo || rateLimitInfo.resetTime <= now) {
      // Reset the counter if window has passed
      rateLimitInfo = { count: 0, resetTime: now + windowMs };
    }

    // Increment the counter
    rateLimitInfo.count++;

    // Store the updated info
    rateLimitStore.set(key, rateLimitInfo);

    // Check if limit is exceeded
    if (rateLimitInfo.count > max) {
      return {
        limited: true,
        response: NextResponse.json(
          { error: 'Too many requests' },
          { status: 429 }
        )
      };
    }

    // Add rate limit headers
    const headers = {
      'X-RateLimit-Limit': max.toString(),
      'X-RateLimit-Remaining': Math.max(0, max - rateLimitInfo.count).toString(),
      'X-RateLimit-Reset': new Date(rateLimitInfo.resetTime).toUTCString()
    };

    return {
      limited: false,
      headers
    };
  };
}