from app.models import SimulationPoint, SimulationRequest, SimulationResult


class SimulationRunner:
    def run(self, request: SimulationRequest) -> SimulationResult:
        model = request.model
        env = request.environment

        points: list[SimulationPoint] = []
        viral_activity = self._initial_viral_activity(request)
        reservoir = max(0.05, model.latency_probability + (1.0 - model.reservoir_decay_rate) * 0.5)

        for day in range(0, env.time_horizon_days + 1, env.step_days):
            if day > 0:
                therapy_effect = env.therapy_pressure * model.drug_susceptibility
                immune_effect = env.immune_pressure * (1.0 - model.immune_escape_score)
                growth = model.replication_rate * model.viral_fitness
                pressure = therapy_effect + immune_effect
                viral_activity = self._clamp(viral_activity + (growth - pressure) * 0.12)

                reservoir_loss = model.reservoir_decay_rate * env.therapy_pressure * 0.08
                reservoir_gain = model.latency_probability * viral_activity * 0.03
                reservoir = self._clamp(reservoir - reservoir_loss + reservoir_gain)

            rebound_risk = self._clamp(
                (model.reactivation_probability * reservoir)
                + (viral_activity * model.immune_escape_score)
                - (env.therapy_pressure * model.drug_susceptibility * 0.35)
            )

            points.append(
                SimulationPoint(
                    day=day,
                    viral_activity_index=round(viral_activity, 4),
                    reservoir_index=round(reservoir, 4),
                    rebound_risk_index=round(rebound_risk, 4),
                )
            )

        final = points[-1]
        return SimulationResult(
            simulation_type=request.simulation_type,
            status="completed",
            points=points if request.output_detail == "standard" else [points[0], final],
            summary={
                "final_viral_activity_index": final.viral_activity_index,
                "final_reservoir_index": final.reservoir_index,
                "final_rebound_risk_index": final.rebound_risk_index,
                "interpretation": self._interpret(final.rebound_risk_index),
            },
            caveat=(
                "Toy abstract model for software architecture validation only; "
                "not a clinical, biological, or wet-lab decision system."
            ),
        )

    def _initial_viral_activity(self, request: SimulationRequest) -> float:
        model = request.model
        env = request.environment
        return self._clamp(
            (model.replication_rate * model.viral_fitness)
            + (model.mutation_pressure * 0.1)
            - (env.therapy_pressure * model.drug_susceptibility * 0.25)
        )

    def _interpret(self, rebound_risk: float) -> str:
        if rebound_risk < 0.25:
            return "low abstract rebound-risk signal"
        if rebound_risk < 0.6:
            return "moderate abstract rebound-risk signal"
        return "high abstract rebound-risk signal"

    def _clamp(self, value: float) -> float:
        return max(0.0, min(1.0, value))

