import os
from typing import Any

import httpx
from pydantic import BaseModel, Field


class WorkerConfig(BaseModel):
    simulation_service_url: str = Field(
        default_factory=lambda: os.getenv("SIMULATION_SERVICE_URL", "http://localhost:8080")
    )


class SimulationWorkflowWorker:
    """Thin adapter between Conductor tasks and the simulation service.

    A real Conductor client loop will poll tasks and call these methods. For
    now, this module defines the task ownership and the service integration.
    """

    def __init__(self, config: WorkerConfig | None = None) -> None:
        self.config = config or WorkerConfig()

    def validate_simulation_safety_policy(self, task_input: dict[str, Any]) -> dict[str, Any]:
        request = self._build_simulation_request(task_input)
        with httpx.Client(base_url=self.config.simulation_service_url, timeout=30.0) as client:
            response = client.post("/simulations/run", json=request)

        if response.status_code == 400:
            return {"approved": False, "reason": response.json()["detail"]}

        response.raise_for_status()
        return {"approved": True, "reason": "Approved by simulation service safety policy."}

    def prepare_simulation_parameters(self, task_input: dict[str, Any]) -> dict[str, Any]:
        request = self._build_simulation_request(task_input)
        return {
            "parameterSet": request,
            "modelFamily": "digital-hiv-abstract",
            "executionMode": "inline-toy-model",
        }

    def launch_kubernetes_simulation_job(self, task_input: dict[str, Any]) -> dict[str, Any]:
        # The first implementation runs inline. Later this becomes a Kubernetes Job submitter.
        return {
            "jobId": f"inline-{task_input.get('workflowId', 'local')}",
            "mode": "inline",
        }

    def collect_simulation_results(self, task_input: dict[str, Any]) -> dict[str, Any]:
        parameter_set = task_input["parameterSet"]
        with httpx.Client(base_url=self.config.simulation_service_url, timeout=30.0) as client:
            response = client.post("/simulations/run", json=parameter_set)

        response.raise_for_status()
        return {
            "results": response.json(),
            "resultLocation": "inline-response",
        }

    def _build_simulation_request(self, task_input: dict[str, Any]) -> dict[str, Any]:
        if "simulationRequest" in task_input:
            request = dict(task_input["simulationRequest"])
        elif "parameterSet" in task_input:
            request = dict(task_input["parameterSet"])
        else:
            request = dict(task_input)

        request.setdefault("researcher_id", task_input.get("researcherId", "unknown-researcher"))
        return request

