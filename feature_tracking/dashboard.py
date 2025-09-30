"""
CloudCurio Feature Tracking Dashboard

A simple web dashboard to visualize feature tracking data.
Built with FastAPI and basic HTML/CSS for easy deployment.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from feature_tracking.feature_tracker import FeatureTracker, FeatureCategory, FeatureStatus
from feature_tracking.config import config


app = FastAPI(title="CloudCurio Feature Tracking Dashboard")

# Mount static files if available
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static directory may not exist

# Global tracker instance
tracker = FeatureTracker(db_path=config.db_path)

# HTML templates for the dashboard
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudCurio Feature Tracking Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat-value { font-size: 2em; font-weight: bold; color: #1976d2; }
            .stat-label { color: #666; }
            .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            .success { color: #4caf50; }
            .failed { color: #f44336; }
            .partial { color: #ff9800; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CloudCurio Feature Tracking Dashboard</h1>
                <p>Monitor feature usage, performance, and effectiveness across the platform</p>
            </div>
            
            <div class="stats-grid" id="stats-container">
                <div class="stat-card">
                    <div class="stat-value" id="total-calls">0</div>
                    <div class="stat-label">Total Feature Calls</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="success-rate">0%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="avg-duration">0.0s</div>
                    <div class="stat-label">Avg Duration</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="avg-efficiency">0.0</div>
                    <div class="stat-label">Avg Efficiency</div>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>Feature Usage by Category</h2>
                <canvas id="categoryChart" width="400" height="200"></canvas>
            </div>
            
            <div class="chart-container">
                <h2>Top Features by Usage</h2>
                <canvas id="topFeaturesChart" width="400" height="200"></canvas>
            </div>
            
            <div class="section">
                <h2>Recent Feature Calls</h2>
                <table id="recent-calls-table">
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th>Category</th>
                            <th>Status</th>
                            <th>Duration</th>
                            <th>Efficiency</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody id="recent-calls-body">
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            // Function to load dashboard data
            async function loadDashboardData() {
                try {
                    // Load stats
                    const statsResponse = await fetch('/api/stats');
                    const stats = await statsResponse.json();
                    
                    document.getElementById('total-calls').textContent = stats.total_calls;
                    document.getElementById('success-rate').textContent = stats.success_rate.toFixed(1) + '%';
                    document.getElementById('avg-duration').textContent = stats.avg_duration.toFixed(3) + 's';
                    document.getElementById('avg-efficiency').textContent = stats.avg_efficiency.toFixed(3);
                    
                    // Load chart data
                    const chartDataResponse = await fetch('/api/chart-data');
                    const chartData = await chartDataResponse.json();
                    
                    // Create category chart
                    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
                    new Chart(categoryCtx, {
                        type: 'bar',
                        data: {
                            labels: chartData.categories.labels,
                            datasets: [{
                                label: 'Usage Count',
                                data: chartData.categories.data,
                                backgroundColor: 'rgba(25, 118, 210, 0.7)'
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                    
                    // Create top features chart
                    const featuresCtx = document.getElementById('topFeaturesChart').getContext('2d');
                    new Chart(featuresCtx, {
                        type: 'horizontalBar',
                        data: {
                            labels: chartData.top_features.labels,
                            datasets: [{
                                label: 'Usage Count',
                                data: chartData.top_features.data,
                                backgroundColor: 'rgba(76, 175, 80, 0.7)'
                            }]
                        },
                        options: {
                            responsive: true,
                            indexAxis: 'y',
                        }
                    });
                    
                    // Load recent calls
                    const recentResponse = await fetch('/api/recent-calls');
                    const recentCalls = await recentResponse.json();
                    
                    const tbody = document.getElementById('recent-calls-body');
                    tbody.innerHTML = '';
                    
                    recentCalls.forEach(call => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${call.feature_name}</td>
                            <td>${call.category}</td>
                            <td class="${call.status}">${call.status}</td>
                            <td>${call.duration.toFixed(3)}s</td>
                            <td>${call.efficiency_score ? call.efficiency_score.toFixed(3) : 'N/A'}</td>
                            <td>${new Date(call.start_time).toLocaleString()}</td>
                        `;
                        tbody.appendChild(row);
                    });
                    
                } catch (error) {
                    console.error('Error loading dashboard data:', error);
                }
            }
            
            // Load data on page load and refresh every 30 seconds
            loadDashboardData();
            setInterval(loadDashboardData, 30000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/stats")
async def get_stats():
    """Get overall statistics"""
    # Get top features to calculate overall stats
    top_features = tracker.get_top_features(100)  # Get all features to calculate total
    
    total_calls = sum(f['usage_count'] for f in top_features)
    success_count = sum(f['success_count'] for f in top_features)
    success_rate = (success_count / total_calls * 100) if total_calls > 0 else 0
    
    # Calculate average duration and efficiency from recent records
    recent_records = tracker.get_all_records(limit=1000)
    if recent_records:
        avg_duration = sum(r.duration for r in recent_records) / len(recent_records)
        avg_efficiency = sum(r.efficiency_score or 0 for r in recent_records) / len(recent_records)
    else:
        avg_duration = 0
        avg_efficiency = 0
    
    return {
        "total_calls": total_calls,
        "success_rate": success_rate,
        "avg_duration": avg_duration,
        "avg_efficiency": avg_efficiency
    }


@app.get("/api/chart-data")
async def get_chart_data():
    """Get data for charts"""
    # Get top features
    top_features = tracker.get_top_features(10)
    
    # Category usage
    category_counts = {}
    recent_records = tracker.get_all_records(limit=1000)
    for record in recent_records:
        category = record.category.value
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Prepare chart data
    chart_data = {
        "categories": {
            "labels": list(category_counts.keys()),
            "data": list(category_counts.values())
        },
        "top_features": {
            "labels": [f['feature_name'] for f in top_features],
            "data": [f['usage_count'] for f in top_features]
        }
    }
    
    return chart_data


@app.get("/api/recent-calls")
async def get_recent_calls(limit: int = 20):
    """Get recent feature calls"""
    records = tracker.get_all_records(limit=limit)
    return [
        {
            "feature_name": r.feature_name,
            "category": r.category.value,
            "status": r.status.value,
            "duration": r.duration,
            "efficiency_score": r.efficiency_score,
            "start_time": r.start_time.isoformat(),
            "user_id": r.user_id
        }
        for r in records
    ]


@app.get("/api/feature/{feature_name}")
async def get_feature_details(feature_name: str):
    """Get details for a specific feature"""
    stats = tracker.get_feature_stats(feature_name)
    recent_calls = tracker.get_all_records(feature_name=feature_name, limit=50)
    
    return {
        "feature_name": feature_name,
        "stats": stats,
        "recent_calls": [
            {
                "status": r.status.value,
                "duration": r.duration,
                "efficiency_score": r.efficiency_score,
                "start_time": r.start_time.isoformat(),
                "error_message": r.error_message
            }
            for r in recent_calls
        ]
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting CloudCurio Feature Tracking Dashboard...")
    print("Access the dashboard at: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)