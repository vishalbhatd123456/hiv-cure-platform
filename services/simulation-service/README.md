# Simulation Service

Python service responsible for safe abstract in-silico simulations.

## Responsibility

- Accept simulation requests from workflow workers.
- Validate requests through the safety policy guard.
- Build abstract digital HIV model parameter sets.
- Return deterministic toy simulation results for early platform integration.
- Later: launch Kubernetes simulation jobs and track result locations.

## Boundary

This service models abstract behavior only. It must not implement wet-lab protocols or actionable pathogen modification procedures.

## Local Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8080
```

## Test

```bash
pytest
```
