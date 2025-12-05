"""FastAPI backend for SQL Agent."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from config import settings
from database import init_database, get_database_path
from agent import create_sql_agent_executor, query_database

app = FastAPI(title="SQL Agent API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent executor (initialized on startup)
agent_executor: Optional[object] = None


class QueryRequest(BaseModel):
    """Request model for SQL queries."""
    query: str


class QueryResponse(BaseModel):
    """Response model for SQL queries."""
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    intermediate_steps: Optional[list] = None


class ConfigResponse(BaseModel):
    """Response model for configuration."""
    database_url: str
    llm_provider: str
    openai_model: str
    openai_temperature: float


@app.on_event("startup")
async def startup_event():
    """Initialize database and agent on startup."""
    global agent_executor
    
    # Initialize database
    db_path = get_database_path(settings.database_url)
    init_database(db_path)
    
    # Create agent executor
    try:
        agent_executor = create_sql_agent_executor(settings.database_url)
        print("SQL Agent initialized successfully")
    except Exception as e:
        print(f"Error initializing SQL Agent: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "SQL Agent API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "agent_initialized": agent_executor is not None}


@app.get("/config", response_model=ConfigResponse)
async def get_config():
    """Get current configuration."""
    return ConfigResponse(
        database_url=settings.database_url,
        llm_provider=settings.llm_provider,
        openai_model=settings.openai_model,
        openai_temperature=settings.openai_temperature
    )


@app.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables (API key masked)."""
    import os
    api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY", "NOT_SET")
    api_key_display = f"{api_key[:10]}..." if api_key and api_key != "NOT_SET" and len(api_key) > 10 else "NOT_SET"
    
    return {
        "openai_api_key_from_settings": api_key_display,
        "openai_api_key_set": bool(api_key and api_key != "NOT_SET"),
        "openai_base_url": settings.openai_base_url,
        "openai_model": settings.openai_model,
        "env_openai_api_key": "SET" if os.getenv("OPENAI_API_KEY") else "NOT_SET",
        "settings_openai_api_key": "SET" if settings.openai_api_key else "NOT_SET"
    }


@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute a natural language query using the SQL agent."""
    if agent_executor is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    result = query_database(agent_executor, request.query)
    
    if result["success"]:
        return QueryResponse(
            success=True,
            result=result["result"],
            intermediate_steps=result.get("intermediate_steps")
        )
    else:
        return QueryResponse(
            success=False,
            error=result["error"]
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

