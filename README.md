# Astrooverz Numerology Website

A numerology analysis website built with FastAPI backend and React frontend.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd astrooverz
   ```

2. **Create environment file**
   ```bash
   cp config.env config.env.example
   # Edit config.env with your actual values
   ```

3. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

4. **Check status**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

## Architecture

- **Frontend**: React + Vite, served by Nginx
- **Backend**: FastAPI + Uvicorn
- **Database**: PostgreSQL
- **Reverse Proxy**: Caddy
- **Containerization**: Docker + Docker Compose

## Troubleshooting 502 Errors

If you're getting 502 errors:

1. **Check container status**:
   ```bash
   docker-compose ps
   ```

2. **Check logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   docker-compose logs caddy
   ```

3. **Verify ports**:
   - Backend: 8000
   - Frontend: 80 (nginx)
   - Caddy: 80, 443

4. **Check environment variables**:
   - Ensure `config.env` file exists
   - Verify database credentials

5. **Rebuild containers**:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

## API Endpoints

- `GET /` - Root endpoint
- `GET /healthz` - Health check
- `GET /api/healthz` - API health check
- `POST /api/analyze_name` - Analyze name (POST)
- `GET /api/analyze_name/{name}` - Analyze name (GET)

## Development

- Frontend dev server: `npm run dev` (port 5173)
- Backend dev server: `uvicorn numerology_app.api:app --reload` (port 8000)

## Deployment

Use the provided deployment scripts:
- **Windows**: `deploy.bat`
- **Linux/Mac**: `./deploy.sh`

