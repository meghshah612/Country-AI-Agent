# Country Information AI Agent

An AI agent built with LangGraph that answers questions about countries using the REST Countries API. Features a production-ready Streamlit web interface.

## Features

- Three-step agent workflow using LangGraph:
  1. Intent/Field Identification: Extracts country name and requested fields from user queries (using structured output)
  2. Tool Invocation: Fetches country data from REST Countries API
  3. Answer Synthesis: Generates natural language answers from extracted data

- Production-ready design with error handling and graceful degradation
- Modern Streamlit web interface with chat functionality
- Docker containerization for easy deployment
- Handles invalid inputs and partial data gracefully
- Structured and maintainable codebase

## Requirements

- Python 3.11+
- OpenAI API key
- Docker (for containerized deployment)

## Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Option 1: Streamlit Web UI (Recommended)

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Option 2: Command Line Interface

Run the agent in terminal:
```bash
python main.py
```

The agent will start in an interactive loop. Ask questions about countries:
- "What is the population of Germany?"
- "What currency does Japan use?"
- "What is the capital and population of Brazil?"

Type `quit` or `exit` to stop the agent.

## Deployment

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t country-ai-agent:latest .
```

2. Run the container:
```bash
docker run -d -p 8501:8501 --env-file .env --name country-ai-agent country-ai-agent:latest
```

Or use docker-compose:
```bash
docker-compose up -d
```

### Using Deployment Scripts

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows (PowerShell):**
```powershell
.\deploy.ps1
```

### Cloud Deployment

The application can be deployed to various cloud platforms:

**Streamlit Cloud:**
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Set `OPENAI_API_KEY` in the secrets section
4. Deploy

**AWS/Azure/GCP:**
- Use the provided Dockerfile to build and push to container registry
- Deploy using container services (ECS, Container Instances, Cloud Run, etc.)
- Ensure port 8501 is exposed and environment variables are set

**Heroku:**
- Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Set environment variables in Heroku dashboard

## Project Structure

```
.
├── app.py              # Streamlit web application
├── main.py             # Command line interface
├── agent.py            # LangGraph agent implementation
├── tools.py            # REST Countries API integration
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose configuration
├── deploy.sh           # Linux/Mac deployment script
├── deploy.ps1          # Windows deployment script
├── .streamlit/         # Streamlit configuration
│   ├── config.toml     # Streamlit settings
│   └── secrets.toml.example
└── README.md           # This file
```

## Technical Details

- Built with LangGraph for multi-step agent workflow
- Uses OpenAI GPT models with structured output for intent identification
- Integrates with REST Countries API (https://restcountries.com/v3.1)
- Streamlit for modern web interface
- Docker containerization for production deployment
- No authentication, database, embeddings, or RAG required
- Handles errors gracefully with informative messages

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Health Check

The application includes a health check endpoint at `/_stcore/health` for monitoring and load balancers.

