# OSINT Extension API Documentation

## Overview

This document describes the API endpoints available in the OSINT extension for BeEF.

## Authentication

All API endpoints require authentication through the BeEF session. Ensure you're logged into BeEF before making API calls.

## Endpoints

### Get Target Information

```
GET /api/osint/target/:target_type/:target_id
```

Retrieve information about a specific target.

**Parameters:**
- `target_type`: Type of target (person, domain, ip, email)
- `target_id`: Identifier for the target

**Response:**
```json
{
  "status": "success",
  "data": {
    "target_type": "domain",
    "target_id": "example.com",
    "name": "Example Domain",
    "created_at": "2025-09-21T10:30:00Z"
  }
}
```

### Start Research

```
POST /api/osint/research/start
```

Initiate a research operation on a target.

**Request Body:**
```json
{
  "target_type": "domain",
  "target_id": "example.com",
  "research_type": "comprehensive"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Research started",
  "research_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Get Research Status

```
GET /api/osint/research/status/:research_id
```

Check the status of a research operation.

**Parameters:**
- `research_id`: UUID of the research operation

**Response:**
```json
{
  "status": "completed",
  "research_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress": 100,
  "results": {
    "findings": 15,
    "connections": 8
  }
}
```

### Get Knowledge Graph Data

```
GET /api/osint/graph/:target_id
```

Retrieve knowledge graph data for visualization.

**Parameters:**
- `target_id`: Identifier for the target

**Response:**
```json
{
  "status": "success",
  "nodes": [
    { "id": "1", "label": "Person", "title": "John Doe" },
    { "id": "2", "label": "Email", "title": "john@example.com" },
    { "id": "3", "label": "Domain", "title": "example.com" }
  ],
  "edges": [
    { "from": "1", "to": "2", "label": "EMAIL_ASSOCIATED_WITH" },
    { "from": "3", "to": "1", "label": "DOMAIN_REGISTERED_BY" }
  ]
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request
- `401`: Unauthorized
- `404`: Not found
- `500`: Internal server error

Error responses follow this format:
```json
{
  "status": "error",
  "message": "Description of the error"
}
```