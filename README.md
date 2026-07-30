# Wine Quality Predictor (FastAPI + React)

This project now includes:

- **Backend:** FastAPI API with prediction and history endpoints.
- **Frontend:** React + Vite + TypeScript app integrated with backend APIs.
- **Deployment target:** Vercel (frontend) + Render (backend).

## Backend API

- `GET /health` - health check
- `POST /predict` - save and return a wine quality prediction
- `GET /predictions` - list saved predictions

## Local setup

### 1. Backend

```bash
python -m pip install -r requirements.txt
python create_table.py
uvicorn app:app --reload
```

Backend runs on `http://127.0.0.1:8000`.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Environment variables

### Backend

- `FRONTEND_ORIGINS` - comma-separated allowed origins for CORS  
  Example:
  - local: `http://localhost:5173,http://127.0.0.1:5173`
  - production: `https://your-frontend.vercel.app`

### Frontend

- `VITE_API_BASE_URL` - backend API base URL  
  Example production value: `https://your-backend.onrender.com`

## Deploy

### Backend on Render

1. Push repository to GitHub.
2. Create a new **Web Service** on Render from this repo.
3. Render will detect `render.yaml`.
4. Add environment variable:
   - `FRONTEND_ORIGINS=https://your-frontend.vercel.app`

### Frontend on Vercel

1. Import `frontend` directory as a Vercel project.
2. Add environment variable:
   - `VITE_API_BASE_URL=https://your-backend.onrender.com`
3. Deploy.
