from dataclasses import dataclass

from app.models import SimulationRequest


@dataclass(frozen=True)
class SafetyDecision:
    approved: bool
    reason: str


class SafetyPolicyGuard:
    """Policy checks for safe, abstract simulation requests."""

    blocked_terms = {
        "protocol",
        "synthesis",
        "clone",
        "construct",
        "engineer virus",
        "wet lab",
        "genetic sequence",
    }

    def evaluate(self, request: SimulationRequest) -> SafetyDecision:
        purpose = request.purpose.lower()
        for term in self.blocked_terms:
            if term in purpose:
                return SafetyDecision(
                    approved=False,
                    reason=(
                        "Simulation purpose appears to request operational "
                        "biological procedures rather than abstract modeling."
                    ),
                )

        if request.model.viral_fitness > 0.95 and request.model.drug_susceptibility < 0.05:
            return SafetyDecision(
                approved=False,
                reason="Requested model parameters exceed approved safety envelope.",
            )

        return SafetyDecision(approved=True, reason="Approved abstract simulation request.")

