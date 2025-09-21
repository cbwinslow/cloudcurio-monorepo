# CloudCurio API Documentation

## Authentication

Most API endpoints require authentication via NextAuth. Admin endpoints require the user to have an admin role.

Worker endpoints require a valid `WORKER_TOKEN` to be passed in the `x-worker-token` header.

## Reviews API

### Create a Review Job
**POST** `/api/reviews`

Creates a new review job for a repository.

**Request Body:**
```json
{
  "repoUrl": "https://github.com/user/repo",
  "klass": "quick" // Optional, defaults to "quick"
}
```

**Response:**
```json
{
  "job": {
    "id": "job-id",
    "repoUrl": "https://github.com/user/repo",
    "status": "queued",
    // ... other job properties
  }
}
```

**Rate Limit:** 10 requests per minute per IP

### Get All Review Jobs
**GET** `/api/reviews`

Retrieves a list of all review jobs, ordered by creation date (newest first), limited to 50.

**Response:**
```json
{
  "jobs": [
    {
      "id": "job-id",
      "repoUrl": "https://github.com/user/repo",
      "status": "queued",
      // ... other job properties
    }
    // ... more jobs
  ]
}
```

### Claim a Review Job
**POST** `/api/reviews/claim`

Allows a worker to claim a review job for processing.

**Headers:**
- `x-worker-token`: Worker authentication token

**Request Body:**
```json
{
  "gpu": "rtx3060", // Optional
  "classes": ["quick", "heavy"] // Optional
}
```

**Response:**
```json
{
  "job": {
    "id": "job-id",
    "repoUrl": "https://github.com/user/repo",
    "status": "queued",
    // ... other job properties
  }
}
```

### Complete a Review Job
**POST** `/api/reviews/[id]/complete`

Allows a worker to submit the results of a review job.

**Headers:**
- `x-worker-token`: Worker authentication token

**Request Body:**
```json
{
  "status": "done", // or "error"
  "content": "<html>...</html>", // Optional, review results
  "error": "Error message", // Optional, only if status is "error"
  "gpu": "rtx3060" // GPU that processed the job
}
```

**Response:**
```json
{
  "ok": true
}
```