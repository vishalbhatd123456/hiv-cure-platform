# Simulation Service

Python service responsible for safe abstract in-silico simulations.

## Responsibility

- Accept simulation requests from workflow workers.
- Validate requests through the safety policy guard.
- Build abstract digital HIV model parameter sets.
- Launch Kubernetes simulation jobs.
- Track run status and result locations.

## Boundary

This service models abstract behavior only. It must not implement wet-lab protocols or actionable pathogen modification procedures.
