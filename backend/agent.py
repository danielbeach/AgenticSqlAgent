"""LangChain SQL Agent setup."""
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from typing import Optional, Any
import os

try:
    from langchain_community.agent_toolkits import create_sql_agent
except ImportError:
    from langchain_experimental.agents import create_sql_agent

from config import settings


def create_sql_agent_executor(database_url: str) -> Any:
    """Create a SQL agent executor using LangChain."""
    # Initialize database
    db = SQLDatabase.from_uri(database_url)
    
    # Initialize LLM
    # ChatOpenAI can read OPENAI_API_KEY from environment automatically
    # But we'll pass it explicitly to be sure
    llm_kwargs = {
        "model": settings.openai_model,
        "temperature": settings.openai_temperature,
    }
    
    # Get API key from settings or environment variable
    # Pydantic Settings should have read it from OPENAI_API_KEY env var
    api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found! "
            "Please set it in your .env file or as an environment variable. "
            f"Settings has key: {bool(settings.openai_api_key)}, "
            f"Env var exists: {bool(os.getenv('OPENAI_API_KEY'))}"
        )
    
    llm_kwargs["api_key"] = api_key
    
    if settings.openai_base_url:
        llm_kwargs["base_url"] = settings.openai_base_url
    
    llm = ChatOpenAI(**llm_kwargs)
    
    # Create toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # Create agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        handle_parsing_errors=True,
    )
    
    return agent


def query_database(agent: Any, query: str) -> dict:
    """Execute a query using the SQL agent."""
    try:
        result = agent.invoke({"input": query})
        return {
            "success": True,
            "result": result.get("output", "No result returned"),
            "intermediate_steps": result.get("intermediate_steps", [])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "result": None
        }

