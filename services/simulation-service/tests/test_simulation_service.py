from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def valid_payload() -> dict:
    return {
        "researcher_id": "researcher-001",
        "simulation_type": "treatment_response",
        "purpose": "Compare abstract treatment pressure scenarios",
        "output_detail": "standard",
        "model": {
            "replication_rate": 0.45,
            "mutation_pressure": 0.2,
            "immune_escape_score": 0.35,
            "drug_susceptibility": 0.8,
            "latency_probability": 0.2,
            "reactivation_probability": 0.15,
            "reservoir_decay_rate": 0.25,
            "viral_fitness": 0.55,
        },
        "environment": {
            "immune_pressure": 0.6,
            "therapy_pressure": 0.85,
            "time_horizon_days": 56,
            "step_days": 7,
        },
    }


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_run_simulation_returns_bounded_points() -> None:
    response = client.post("/simulations/run", json=valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["simulation_type"] == "treatment_response"
    assert len(body["points"]) == 9
    for point in body["points"]:
        assert 0 <= point["viral_activity_index"] <= 1
        assert 0 <= point["reservoir_index"] <= 1
        assert 0 <= point["rebound_risk_index"] <= 1


def test_safety_guard_blocks_operational_purpose() -> None:
    payload = valid_payload()
    payload["purpose"] = "Create a wet lab protocol"

    response = client.post("/simulations/run", json=payload)

    assert response.status_code == 400
    assert "abstract modeling" in response.json()["detail"]

