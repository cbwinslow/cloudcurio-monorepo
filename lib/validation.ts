import { z } from 'zod';
import { NextResponse } from 'next/server';

// Validation schemas
export const reviewJobSchema = z.object({
  repoUrl: z.string().url(),
  klass: z.string().optional().default('quick')
});

export const claimJobSchema = z.object({
  gpu: z.string().nullable(),
  classes: z.array(z.string()).optional().default([])
});

export const completeJobSchema = z.object({
  status: z.string().optional(),
  content: z.string().optional(),
  error: z.string().optional(),
  gpu: z.string().nullable()
});

// Validation function
export function validateRequest<T>(
  schema: z.Schema<T>,
  data: unknown
): { success: true; data: T } | { success: false; error: NextResponse } {
  try {
    const result = schema.parse(data);
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: NextResponse.json(
          { error: 'Validation failed', issues: error.errors },
          { status: 400 }
        )
      };
    }
    return {
      success: false,
      error: NextResponse.json(
        { error: 'Invalid request data' },
        { status: 400 }
      )
    };
  }
}