import { z } from 'zod';

const envSchema = z.object({
  // Site
  NEXT_PUBLIC_SITE_URL: z.string().url(),
  NEXTAUTH_URL: z.string().url(),
  
  // Auth.js (NextAuth)
  GITHUB_ID: z.string().min(1),
  GITHUB_SECRET: z.string().min(1),
  NEXTAUTH_SECRET: z.string().min(1),
  
  // Database
  DATABASE_URL: z.string().min(1),
  
  // Stripe
  STRIPE_SECRET_KEY: z.string().min(1),
  STRIPE_WEBHOOK_SECRET: z.string().min(1),
  STRIPE_PRICE_PRO: z.string().min(1),
  STRIPE_PRICE_FREE: z.string().min(1),
  
  // Worker coordination
  WORKER_TOKEN: z.string().min(1),
  
  // GitHub / GitLab webhooks
  GITHUB_WEBHOOK_SECRET: z.string().min(1),
  GITLAB_WEBHOOK_TOKEN: z.string().min(1),
});

export const validateEnv = () => {
  try {
    envSchema.parse(process.env);
    return { success: true, error: null };
  } catch (error) {
    if (error instanceof z.ZodError) {
      const missingVars = error.errors.map(e => e.path.join('.'));
      return { 
        success: false, 
        error: `Missing or invalid environment variables: ${missingVars.join(', ')}` 
      };
    }
    return { success: false, error: 'Unknown error validating environment variables' };
  }
};