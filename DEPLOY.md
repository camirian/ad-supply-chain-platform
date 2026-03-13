# Quickstart: Deploying A&D Supply Chain Agent

This platform is configured for **Google Cloud Run** scale-to-zero deployments, ensuring absolutely no continuous billing when idle.

## 1. Environment Setup

### Prerequisites
You will need an active API key for Google Gemini (used by the text-to-SQL logic block) and the `gcloud` CLI installed.

### Local Development
Clone your repository to your local machine:
```bash
git clone https://github.com/YOUR_USERNAME/ad-supply-chain-platform.git
cd ad-supply-chain-platform
```

Create a virtual environment and start the FastAPI Backend:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/db_init.py  # Initialize SQLite
export GOOGLE_API_KEY="your_gemini_key_here"
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Start the Vite React Frontend in a separate terminal:
```bash
cd web
npm install
npm run dev
```

## 2. Cloud Run Deployment

Deployment is managed via standard Google Cloud Buildpacks/Dockerfiles using the scale-to-zero architecture constraints.

### Deploy Backend
```bash
gcloud run deploy ad-supply-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --port 8000 \
  --set-env-vars="GOOGLE_API_KEY=YOUR_GEMINI_KEY"
```

### Deploy Frontend
When deploying the frontend, ensure the HTTP requests point to your new backend URL. You can swap `http://localhost:8000` in `web/src/App.jsx` with your Cloud Run backend URL prior to deployment.
```bash
gcloud run deploy ad-supply-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --port 8080
```

Once deployed, Google Cloud Run will natively spin down all containers to zero after a few minutes of inactivity.
