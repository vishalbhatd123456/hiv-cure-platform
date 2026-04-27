from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SimulationType(str, Enum):
    TREATMENT_RESPONSE = "treatment_response"
    RESERVOIR_DECAY = "reservoir_decay"
    REBOUND_RISK = "rebound_risk"


class DigitalHIVModel(BaseModel):
    """Abstract in-silico viral behavior model.

    This model intentionally uses bounded, high-level properties rather than
    genetic sequences, protocols, or operational pathogen modification steps.
    """

    replication_rate: float = Field(ge=0.0, le=1.0)
    mutation_pressure: float = Field(ge=0.0, le=1.0)
    immune_escape_score: float = Field(ge=0.0, le=1.0)
    drug_susceptibility: float = Field(ge=0.0, le=1.0)
    latency_probability: float = Field(ge=0.0, le=1.0)
    reactivation_probability: float = Field(ge=0.0, le=1.0)
    reservoir_decay_rate: float = Field(ge=0.0, le=1.0)
    viral_fitness: float = Field(ge=0.0, le=1.0)


class SimulationEnvironment(BaseModel):
    immune_pressure: float = Field(ge=0.0, le=1.0)
    therapy_pressure: float = Field(ge=0.0, le=1.0)
    time_horizon_days: int = Field(ge=1, le=3650)
    step_days: int = Field(default=7, ge=1, le=90)

    @model_validator(mode="after")
    def validate_step_size(self) -> "SimulationEnvironment":
        if self.step_days > self.time_horizon_days:
            raise ValueError("step_days cannot be greater than time_horizon_days")
        return self


class SimulationRequest(BaseModel):
    researcher_id: str = Field(min_length=1, max_length=128)
    simulation_type: SimulationType
    model: DigitalHIVModel
    environment: SimulationEnvironment
    purpose: str = Field(min_length=1, max_length=512)
    output_detail: Literal["summary", "standard"] = "summary"


class SimulationPoint(BaseModel):
    day: int
    viral_activity_index: float
    reservoir_index: float
    rebound_risk_index: float


class SimulationResult(BaseModel):
    simulation_type: SimulationType
    status: Literal["completed"]
    points: list[SimulationPoint]
    summary: dict[str, float | str]
    caveat: str

