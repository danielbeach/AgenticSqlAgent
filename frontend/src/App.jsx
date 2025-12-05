import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [config, setConfig] = useState(null)
  const [showConfig, setShowConfig] = useState(false)
  const [configForm, setConfigForm] = useState({
    database_url: '',
    llm_provider: 'openai',
    openai_model: '',
    openai_temperature: 0.0,
    openai_api_key: '',
    openai_base_url: ''
  })

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/config`)
      setConfig(response.data)
      setConfigForm({
        database_url: response.data.database_url,
        llm_provider: response.data.llm_provider,
        openai_model: response.data.openai_model,
        openai_temperature: response.data.openai_temperature,
        openai_api_key: '',
        openai_base_url: ''
      })
    } catch (error) {
      console.error('Error fetching config:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/query`, { query })
      setResults(prev => [{
        query,
        result: response.data.result,
        success: response.data.success,
        error: response.data.error,
        timestamp: new Date().toLocaleTimeString()
      }, ...prev])
      setQuery('')
    } catch (error) {
      setResults(prev => [{
        query,
        result: null,
        success: false,
        error: error.response?.data?.detail || error.message,
        timestamp: new Date().toLocaleTimeString()
      }, ...prev])
    } finally {
      setLoading(false)
    }
  }

  const exampleQueries = [
    "What are the total sales for each sales person?",
    "Who is the top performing sales person this month?",
    "Show me sales by region",
    "What is the average sale amount?",
    "Which product category has the most sales?",
    "Show me sales trends over the last 30 days"
  ]

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>🤖 SQL Agent</h1>
          <p className="subtitle">An Agentic AI Example - Query your sales database in natural language</p>
          <button 
            className="config-button"
            onClick={() => setShowConfig(!showConfig)}
          >
            {showConfig ? 'Hide' : 'Show'} Configuration
          </button>
        </header>

        {showConfig && config && (
          <div className="config-panel">
            <h2>Current Configuration</h2>
            <div className="config-grid">
              <div className="config-item">
                <label>Database URL:</label>
                <code>{config.database_url}</code>
              </div>
              <div className="config-item">
                <label>LLM Provider:</label>
                <code>{config.llm_provider}</code>
              </div>
              <div className="config-item">
                <label>Model:</label>
                <code>{config.openai_model}</code>
              </div>
              <div className="config-item">
                <label>Temperature:</label>
                <code>{config.openai_temperature}</code>
              </div>
            </div>
            <p className="config-note">
              💡 Configuration is managed via environment variables. 
              Update the .env file or docker-compose.yml to change settings.
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="query-form">
          <div className="input-group">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about your sales data... (e.g., 'What are the total sales for each sales person?')"
              rows={3}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !query.trim()}>
              {loading ? 'Querying...' : 'Query'}
            </button>
          </div>
        </form>

        <div className="examples">
          <h3>Example Queries:</h3>
          <div className="example-buttons">
            {exampleQueries.map((example, idx) => (
              <button
                key={idx}
                className="example-button"
                onClick={() => setQuery(example)}
                disabled={loading}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        <div className="results">
          <h2>Query Results</h2>
          {results.length === 0 ? (
            <div className="empty-state">
              <p>No queries yet. Try asking a question above!</p>
            </div>
          ) : (
            results.map((result, idx) => (
              <div key={idx} className={`result-card ${result.success ? 'success' : 'error'}`}>
                <div className="result-header">
                  <span className="timestamp">{result.timestamp}</span>
                  <span className={`status ${result.success ? 'success' : 'error'}`}>
                    {result.success ? '✓' : '✗'}
                  </span>
                </div>
                <div className="result-query">
                  <strong>Query:</strong> {result.query}
                </div>
                {result.success ? (
                  <div className="result-content">
                    <strong>Result:</strong>
                    <pre>{result.result}</pre>
                  </div>
                ) : (
                  <div className="result-error">
                    <strong>Error:</strong>
                    <pre>{result.error}</pre>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default App

