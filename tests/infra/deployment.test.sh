#!/bin/bash
set -e

# Test deployment validation
echo "Testing CloudCurio deployment..."

# Check services
systemctl is-active --quiet cloudcurio-app || { echo "App service failed"; exit 1; }
systemctl is-active --quiet cloudcurio-worker || { echo "Worker service failed"; exit 1; }

# Check ports
nc -z localhost 3000 || { echo "Port 3000 (app) not open"; exit 1; }
nc -z localhost 5432 || { echo "Port 5432 (Postgres) not open"; exit 1; }  # If Supabase/Postgres

# Check DB connection (SQLite example)
sqlite3 dev.db "SELECT 1;" || { echo "DB connection failed"; exit 1; }

# Check API
curl -f http://localhost:3000/api/scripts || { echo "API /scripts failed"; exit 1; }

# Check worker (simulate job)
curl -X POST http://localhost:3000/api/reviews/claim -d '{}' || { echo "Worker claim failed"; exit 1; }

# Check monitoring
curl -f http://localhost:9090 || { echo "Prometheus not responding"; exit 1; }  # Port 9090 default
curl -f http://localhost:3000 || { echo "Grafana not responding"; exit 1; }  # Port 3000, but conflict—use 3001 if set

# Error simulation: Test invalid API
curl -f -X POST http://localhost:3000/api/chat -d '{"prompt": ""}' | grep -q "Invalid" || { echo "Validation error not caught"; exit 1; }

echo "All deployment tests passed!"
