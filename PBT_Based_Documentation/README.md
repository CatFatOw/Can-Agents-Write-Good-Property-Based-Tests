# Invariant-Based Documentation Generator

An experimental system for studying whether documentation reconstructed from
implementation-backed invariants can be more useful than traditional
documentation. It turns source code into candidate behavioral claims, supports
human review, generates property-based tests, evaluates those tests, and
produces contract-oriented Markdown documentation.

The project includes both a reproducible command-line research workflow and an
interactive FastAPI web application for comparing invariant-based and
traditional documentation.

## What it does

- Extracts candidate invariants from Python source code with an LLM.
- Keeps a human reviewer in the loop before claims are promoted.
- Generates Hypothesis property-based tests for approved invariants.
- Evaluates validity, soundness, and optional mutation resistance.
- Reconstructs Markdown documentation from the supported claims.
- Provides an Arena-style web UI for generating, reviewing, assessing, and
  comparing documentation.

## Demo

Source lookup for an inspectable Python object:

![Source lookup demo](./assets/demo-source-lookup.png)

The UI checks for a provider API key before issuing generation requests:

![API key required demo](./assets/demo-openai-key-required.png)

## Architecture

The web application uses a layered FastAPI backend. Routers own HTTP concerns;
services implement workflows and authorization; repositories own SQLAlchemy
queries.

```text
app/
├── main.py                  # FastAPI application and router registration
├── routers/                 # HTTP endpoints
├── services/                # Auth, user, and documentation workflows
├── repository/              # Database access functions
├── models/                  # SQLAlchemy models
├── schemas/                 # Pydantic request/response models
├── security/                # JWT, password, and admin authorization helpers
├── tasks/                   # Celery jobs for long-running work
└── alembic/                 # Database migrations
```

The static frontend (`index.html`, `app.js`, and `styles.css`) is served by the
same FastAPI process. `server.py` is retained only as a legacy reference; use
`app.main:app` for all new development and deployments.

## Quick start

### Prerequisites

- Python 3.11+
- An OpenAI, Anthropic, or CMU AI Gateway API key for generation
- PostgreSQL for a production-like setup (SQLite is used automatically for
  local smoke testing)
- Redis when using the background Celery jobs

### Install

```bash
git clone https://github.com/CatFatOw/Can-Agents-Write-Good-Property-Based-Tests.git
cd Can-Agents-Write-Good-Property-Based-Tests/PBT_Based_Documentation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure

Set a JWT signing key. Set `DATABASE_URL` for PostgreSQL, or leave it unset to
use the local SQLite fallback.

```bash
export JWT_KEY="replace-with-a-long-random-secret"
export DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/pbt_docs"

# Optional provider configuration
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-5.5"
export OPENAI_METRICS_MODEL="gpt-5.4-mini"
```

For the CMU AI Gateway, use the OpenAI-compatible API endpoint and a key from
its dashboard:

```bash
export CMU_AI_GATEWAY_BASE_URL="https://ai-gateway.andrew.cmu.edu/v1"
```

### Run the web application

```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8011 --reload
```

Open [http://127.0.0.1:8011](http://127.0.0.1:8011).

For PostgreSQL, apply migrations before starting the application:

```bash
alembic -c app/alembic.ini upgrade head
```

### Background jobs (optional)

Metric generation, mutation analysis, and CSV exports can run through Celery.
With Redis available at `REDIS_URL`, start a worker in another terminal:

```bash
celery -A app.celery_app worker --loglevel=info
```

## Research workflow

The command-line workflow uses JSON configurations for reproducible runs.

```bash
export OPENAI_API_KEY="..."
python3 gpt_documentation_generator.py --config numpy_docs_config.json
```

The first run creates reviewer files under `artifacts/<api_name>/`. Keep only
accepted claims in `human_review.md`, then run the command again to generate
tests, metrics, and reconstructed documentation. Setting `"auto_continue":
true` in the configuration continues automatically once review files exist.

```text
source code
  → candidate invariants
  → human review
  → Hypothesis tests
  → validity / soundness / optional mutation analysis
  → reconstructed documentation
```

The final documentation is deliberately free of evaluation statistics. Metrics
are an internal quality gate, not part of the resulting API documentation.

### Example configuration

```json
{
  "source": "source_code/path/to/module.py",
  "function": "api_name",
  "model": "gpt-5.4-mini",
  "artifact_root": "artifacts",
  "run_mutation": false,
  "auto_continue": true,
  "min_validity": 0.8,
  "min_soundness": 0.8,
  "min_confidence": 0.75,
  "min_mutation": 0.25
}
```

## Model providers

| Provider | Use case | Configuration |
| --- | --- | --- |
| OpenAI | Default generation and metrics | `OPENAI_API_KEY` |
| Anthropic | Invariants and Markdown generation | API key in the UI or environment |
| CMU AI Gateway | OpenAI-compatible CMU deployment | Gateway key and `/v1` base URL |

Markdown generation and metrics can use separate models. The UI exposes both
settings; environment variables provide defaults.

## Outputs

Each run produces an artifact directory such as:

```text
artifacts/<api_name>/
├── candidate_invariants.md
├── human_review.md
├── generated_tests.py
├── metrics_report.md
├── mutation_analysis.md          # when enabled
├── documentation_blocked.md      # when the quality gate fails
└── reconstructed_documentation.md
```

Examples generated in this repository include
[`numpy.linalg.norm`](./artifacts/numpy/norm/reconstructed_documentation.md)
and [`numpy.dot`](./artifacts/numpy/dot/reconstructed_documentation.md).

## Verification

Run the available tests and a minimal application smoke check:

```bash
pytest -q
python3 -c 'from fastapi.testclient import TestClient; from app.main import app; print(TestClient(app).get("/health").json())'
```

## Deployment

The repository includes `render.yaml` and `scripts/render-start.sh` for Render.
Set the production values for `JWT_KEY`, `DATABASE_URL`, `REDIS_URL`, and the
selected model provider credentials in the hosting environment. The startup
script runs migrations before launching `uvicorn app.main:app`.

## License and research status

This is a research prototype. Generated documentation and test artifacts should
be reviewed by a human before being used as authoritative API documentation.
