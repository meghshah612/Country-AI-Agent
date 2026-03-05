# Quick Start Guide

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the UI:**
   - Open your browser to `http://localhost:8501`

## Docker Deployment

### Quick Start with Docker Compose

```bash
docker-compose up -d
```

### Manual Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t country-ai-agent:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8501:8501 --env-file .env --name country-ai-agent country-ai-agent:latest
   ```

3. **View logs:**
   ```bash
   docker logs -f country-ai-agent
   ```

4. **Stop the container:**
   ```bash
   docker stop country-ai-agent
   docker rm country-ai-agent
   ```

## Cloud Deployment Options

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `OPENAI_API_KEY` in secrets
5. Deploy

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variable: `heroku config:set OPENAI_API_KEY=your_key`
5. Deploy: `git push heroku main`

### AWS/Azure/GCP

Use the provided Dockerfile with your container registry and container service.

## Troubleshooting

**Issue: "OpenAI API key not configured"**
- Ensure `.env` file exists with `OPENAI_API_KEY=your_key`
- For Docker: Use `--env-file .env` flag
- For cloud: Set environment variable in platform settings

**Issue: Port already in use**
- Change port in `app.py` or use `--server.port` flag
- For Docker: Change port mapping `-p 8502:8501`

**Issue: Module not found**
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated

