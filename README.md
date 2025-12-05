# SQL Agent - Agentic AI Example

A comprehensive example application demonstrating Agentic AI concepts using LangChain, React, FastAPI, and SQLite. This project teaches how to build an intelligent SQL agent that can answer natural language questions about a sales database.

## Features

- 🤖 **LangChain SQL Agent**: Uses LangChain to create an intelligent agent that translates natural language to SQL queries
- 🎨 **Modern React Frontend**: Beautiful, responsive UI built with React and Vite
- 🚀 **FastAPI Backend**: High-performance Python API with async support
- 💾 **Pre-filled SQLite Database**: Sample sales data with sales people and daily sales records
- ⚙️ **Fully Configurable**: All components (database, LLM endpoint, models) are configurable via environment variables
- 🐳 **Dockerized**: Complete Docker setup with docker-compose for easy deployment

## Architecture

```
┌─────────────┐
│   React     │  Frontend (Port 3000)
│   Frontend  │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   FastAPI   │  Backend (Port 8000)
│   Backend   │
└──────┬──────┘
       │
       ├──► LangChain SQL Agent
       │
       └──► SQLite Database (sales.db)
```

## Prerequisites

- Docker and Docker Compose
- OpenAI API key (or compatible endpoint)
- Python 3.12+ (for local development)
- Node.js 20+ (for local development)

## Quick Start with Docker

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your-api-key-here
   OPENAI_BASE_URL=https://api.openai.com/v1  # Optional, for custom endpoints
   OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
   ```

3. **Start the services**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**

   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Local Development

### Backend Setup

1. **Install dependencies**

   ```bash
   pip install uv
   uv pip install -e .
   ```

2. **Set environment variables**

   Create a `.env` file in the `backend/` directory:
   ```bash
   DATABASE_URL=sqlite:///./sales.db
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

3. **Run the backend**

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Install dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Run the frontend**

   ```bash
   npm run dev
   ```

## Configuration

All components are configurable via environment variables:

### Database Configuration

- `DATABASE_URL`: SQLite database URL (default: `sqlite:///./sales.db`)
  - Example: `sqlite:///./data/sales.db`

### LLM Configuration

- `LLM_PROVIDER`: LLM provider (default: `openai`)
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_BASE_URL`: Custom OpenAI-compatible endpoint (optional)
  - Example: `https://api.openai.com/v1` or `http://localhost:1234/v1`
- `OPENAI_MODEL`: Model name (default: `gpt-4o-mini`)
  - Examples: `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`
- `OPENAI_TEMPERATURE`: Model temperature (default: `0.0`)

### API Configuration

- `API_HOST`: API host (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)
- `CORS_ORIGINS`: Allowed CORS origins (JSON array)

## Database Schema

The application includes a pre-filled SQLite database with the following schema:

### `sales_people` Table

| Column      | Type    | Description                    |
|-------------|---------|--------------------------------|
| id          | INTEGER | Primary key                    |
| name        | TEXT    | Sales person name              |
| email       | TEXT    | Email address (unique)         |
| region      | TEXT    | Sales region (North/South/East/West) |
| hire_date   | DATE    | Date hired                     |
| quota       | REAL    | Sales quota                    |

### `sales` Table

| Column           | Type    | Description                    |
|------------------|---------|--------------------------------|
| id               | INTEGER | Primary key                    |
| sales_person_id  | INTEGER | Foreign key to sales_people    |
| sale_date        | DATE    | Date of sale                   |
| amount           | REAL    | Sale amount                    |
| product_category | TEXT    | Product category               |
| customer_name    | TEXT    | Customer name                  |

## Example Queries

Try asking the agent questions like:

- "What are the total sales for each sales person?"
- "Who is the top performing sales person this month?"
- "Show me sales by region"
- "What is the average sale amount?"
- "Which product category has the most sales?"
- "Show me sales trends over the last 30 days"
- "How many sales did Alice Johnson make in the last week?"

## API Endpoints

### `GET /`

Health check endpoint.

### `GET /health`

Detailed health check including agent initialization status.

### `GET /config`

Get current configuration (database URL, LLM settings, etc.).

### `POST /query`

Execute a natural language query.

**Request:**
```json
{
  "query": "What are the total sales for each sales person?"
}
```

**Response:**
```json
{
  "success": true,
  "result": "The total sales for each sales person are:\n- Alice Johnson: $125,430.50\n- Bob Smith: $142,890.25\n...",
  "intermediate_steps": [...]
}
```

## Project Structure

```
SQLAgent/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── agent.py         # LangChain SQL agent setup
│   ├── database.py      # Database initialization
│   ├── config.py        # Configuration management
│   └── Dockerfile       # Backend Docker image
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React component
│   │   ├── App.css      # Styles
│   │   └── main.jsx     # React entry point
│   ├── package.json     # Frontend dependencies
│   └── Dockerfile       # Frontend Docker image
├── data/                # Database storage (created at runtime)
├── docker-compose.yml   # Docker orchestration
├── pyproject.toml       # Python dependencies
└── README.md           # This file
```

## Teaching Points

This project demonstrates several key Agentic AI concepts:

1. **Natural Language to SQL Translation**: The agent understands natural language and converts it to SQL queries
2. **Tool Use**: The agent uses SQL tools to interact with the database
3. **Memory**: The agent maintains conversation context across queries
4. **Error Handling**: Graceful handling of parsing errors and invalid queries
5. **Modular Architecture**: Separated concerns (frontend, backend, agent, database)

## Troubleshooting

### Agent not initializing

- Check that `OPENAI_API_KEY` is set correctly
- Verify the API endpoint is accessible
- Check backend logs for detailed error messages

### Database not found

- The database is automatically created on first startup
- Ensure the `data/` directory is writable
- Check `DATABASE_URL` configuration

### CORS errors

- Verify `CORS_ORIGINS` includes your frontend URL
- Check that both services are running

## License

This project is provided as an educational example.

## Contributing

This is an educational project. Feel free to fork and modify for your teaching needs!

