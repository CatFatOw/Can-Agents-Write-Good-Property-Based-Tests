# Deployment

This project is set up for:

- Neon: Postgres database
- Render: FastAPI backend
- Vercel: static frontend

## 1. Neon

Use the pooled or direct Neon Postgres connection string as `DATABASE_URL`.

For SQLAlchemy, prefer the normal Postgres URL form:

```text
postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require
```

## 2. Render Backend

Render's FastAPI guide uses:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

This repo uses `render.yaml` and `scripts/render-start.sh` instead, because the app lives at `app.main:app` and migrations should run before startup.

In Render:

1. Create a new Blueprint/Web Service from this repo.
2. Use root directory `PBT_Based_Documentation` if deploying from the larger repo.
3. Set these environment variables:

```text
DATABASE_URL=postgresql+psycopg://...neon.../...?sslmode=require
JWT_KEY=<long random secret>
FRONTEND_ORIGINS=https://YOUR-VERCEL-FRONTEND.vercel.app
```

The model provider, API key, model name, and optional base URL are provided by the user in the app UI. Only set provider-specific backend variables such as `OPENAI_API_KEY`, `OPENAI_MODEL`, `ANTHROPIC_API_KEY`, or `CMU_AI_GATEWAY_API_KEY` if you intentionally want server-side fallback defaults.

After deploy, copy the Render URL, for example:

```text
https://ibd-fastapi.onrender.com
```

## 3. Vercel Frontend

Vercel reads `vercel.json` for file-based project configuration. This frontend deploy builds `frontend-dist/` and serves it as static files.

In Vercel:

1. Create a new project from this repo.
2. Set root directory to `PBT_Based_Documentation` if deploying from the larger repo.
3. Vercel should read these settings from `vercel.json`:

```text
Build Command: ./scripts/build-frontend.sh
Output Directory: frontend-dist
```

4. Set this environment variable:

```text
API_BASE_URL=https://YOUR-RENDER-SERVICE.onrender.com
```

The build script writes that value into `frontend-dist/config.js`, and `app.js` uses it for API requests.

## 4. CORS

Once Vercel gives you its URL, add it to Render:

```text
FRONTEND_ORIGINS=https://YOUR-VERCEL-FRONTEND.vercel.app
```

For multiple frontends:

```text
FRONTEND_ORIGINS=https://one.example.com,https://two.example.com
```

## 5. Local Dev

Run the backend:

```bash
uvicorn app.main:app --reload --port 8011
```

Open `index.html` directly or serve the folder. `config.js` defaults to same-origin, while `file://` mode falls back to `http://127.0.0.1:8011`.
