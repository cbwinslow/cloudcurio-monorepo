import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from sqlalchemy.orm import Session

# Add the project root to the Python path to resolve imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import sys
import os

# Add the project root to the Python path to resolve imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from crew.mcp_server.database import get_db, CrewRun
from crew.main import code_review_crew  # Import the existing crew
# Additional crews will be imported as they're created
from crew.documentation_crew import create_documentation_crew
from crew.vulnerability_assessment_crew import create_vulnerability_assessment_crew
from crew.mcp_server.config import MCPConfig
from crew.ai_tools.config_manager import global_config_manager


# Set up logging
logging.basicConfig(level=getattr(logging, MCPConfig.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CloudCurio MCP Server",
    description="Model Context Protocol server for managing CrewAI crews",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure this properly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class CrewRequest(BaseModel):
    crew_type: str
    config: Optional[Dict] = {}
    input_data: Optional[Dict] = {}

class CrewStatus(BaseModel):
    crew_id: str
    crew_type: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

# Generate unique ID for crews
def generate_crew_id():
    import uuid
    return str(uuid.uuid4())

@app.get("/")
async def root():
    return {"message": "CloudCurio MCP Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/crews/start")
async def start_crew(crew_request: CrewRequest, db: Session = Depends(get_db)):
    """Start a new crew with the specified configuration"""
    crew_id = generate_crew_id()
    
    # Validate crew_type
    valid_crew_types = ["code_review", "documentation", "vulnerability_assessment"]
    if crew_request.crew_type not in valid_crew_types:
        raise HTTPException(status_code=400, detail=f"Invalid crew type. Valid types are: {', '.join(valid_crew_types)}")
    
    # Create crew record in database
    crew_run = CrewRun(
        crew_id=crew_id,
        crew_type=crew_request.crew_type,
        status="pending",
        config=crew_request.config,
        input_data=crew_request.input_data,
        created_at=datetime.utcnow()
    )
    
    db.add(crew_run)
    db.commit()
    db.refresh(crew_run)
    
    # Run the crew in the background
    asyncio.create_task(run_crew_async(crew_id, crew_request, crew_run.created_at))
    
    return {"crew_id": crew_id, "message": "Crew started successfully"}

async def run_crew_async(crew_id: str, crew_request: CrewRequest, created_at: datetime):
    """Run the crew asynchronously"""
    # Need to create a new database session for the background task
    from crew.mcp_server.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Update the crew status to running
        crew_run = db.query(CrewRun).filter(CrewRun.crew_id == crew_id).first()
        if crew_run:
            crew_run.status = "running"
            crew_run.started_at = datetime.utcnow()
            db.commit()
        
        # Execute the appropriate crew based on type
        if crew_request.crew_type == "code_review":
            # For now, run the existing code review crew
            result = code_review_crew.kickoff()
        elif crew_request.crew_type == "documentation":
            # Create and run the documentation crew
            doc_crew = create_documentation_crew()
            result = doc_crew.kickoff()
        elif crew_request.crew_type == "vulnerability_assessment":
            # Create and run the vulnerability assessment crew
            vuln_crew = create_vulnerability_assessment_crew()
            result = vuln_crew.kickoff()
        else:
            # Placeholder for other crew types
            result = f"Executed {crew_request.crew_type} crew with config: {crew_request.config}"
        
        # Update the crew status to completed
        if crew_run:
            crew_run.status = "completed"
            crew_run.completed_at = datetime.utcnow()
            crew_run.result = str(result)
            db.commit()
        
        logger.info(f"Crew {crew_id} completed successfully")
    except Exception as e:
        # Update the crew status to failed
        crew_run = db.query(CrewRun).filter(CrewRun.crew_id == crew_id).first()
        if crew_run:
            crew_run.status = "failed"
            crew_run.completed_at = datetime.utcnow()
            crew_run.error = str(e)
            db.commit()
        
        logger.error(f"Crew {crew_id} failed: {str(e)}")
    finally:
        db.close()

@app.get("/crews/{crew_id}")
async def get_crew_status(crew_id: str, db: Session = Depends(get_db)):
    """Get the status of a specific crew"""
    crew_run = db.query(CrewRun).filter(CrewRun.crew_id == crew_id).first()
    
    if not crew_run:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    # Convert the database object to the response model
    return CrewStatus(
        crew_id=crew_run.crew_id,
        crew_type=crew_run.crew_type,
        status=crew_run.status,
        created_at=crew_run.created_at,
        started_at=crew_run.started_at,
        completed_at=crew_run.completed_at,
        result={"output": crew_run.result} if crew_run.result else None,
        error=crew_run.error
    )

@app.get("/crews")
async def list_crews(db: Session = Depends(get_db)):
    """List all crews"""
    crew_runs = db.query(CrewRun).all()
    
    return [
        CrewStatus(
            crew_id=crew_run.crew_id,
            crew_type=crew_run.crew_type,
            status=crew_run.status,
            created_at=crew_run.created_at,
            started_at=crew_run.started_at,
            completed_at=crew_run.completed_at,
            result={"output": crew_run.result} if crew_run.result else None,
            error=crew_run.error
        )
        for crew_run in crew_runs
    ]

@app.delete("/crews/{crew_id}")
async def delete_crew(crew_id: str, db: Session = Depends(get_db)):
    """Delete a specific crew"""
    crew_run = db.query(CrewRun).filter(CrewRun.crew_id == crew_id).first()
    
    if not crew_run:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    db.delete(crew_run)
    db.commit()
    
    return {"message": "Crew deleted successfully"}

# Placeholder for additional endpoints as needed
@app.post("/crews/stop/{crew_id}")
async def stop_crew(crew_id: str, db: Session = Depends(get_db)):
    """Stop a running crew (not implemented yet)"""
    crew_run = db.query(CrewRun).filter(CrewRun.crew_id == crew_id).first()
    
    if not crew_run:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    if crew_run.status == "running":
        # In a real implementation, you would cancel the running crew
        # For now, just mark it as stopped
        crew_run.status = "stopped"
        crew_run.completed_at = datetime.utcnow()
        db.commit()
    
    return {"message": "Crew stop request processed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)