from fastapi import FastAPI, HTTPException

from app.models import SimulationRequest, SimulationResult
from app.runner import SimulationRunner
from app.safety import SafetyPolicyGuard

app = FastAPI(
    title="HIV Cure Platform Simulation Service",
    version="0.1.0",
    description="Safe abstract in-silico simulation service.",
)

policy_guard = SafetyPolicyGuard()
runner = SimulationRunner()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/simulations/run", response_model=SimulationResult)
def run_simulation(request: SimulationRequest) -> SimulationResult:
    decision = policy_guard.evaluate(request)
    if not decision.approved:
        raise HTTPException(status_code=400, detail=decision.reason)
    return runner.run(request)

