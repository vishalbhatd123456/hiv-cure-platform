# Simulation Safety Boundary

## Purpose

The platform may model HIV-like behavior computationally for safe in-silico research, education, and hypothesis testing. It must not encode wet-lab protocols, pathogen engineering procedures, or operational instructions for creating or modifying real viruses.

## Where The Digital HIV Model Lives

```text
services/simulation-service/
  app/
    models/
      hiv_digital_model.py
      viral_population.py
      host_immune_response.py
      therapy_pressure.py
      reservoir_model.py
    simulations/
      latency_simulation.py
      rebound_simulation.py
      treatment_response_simulation.py
      mutation_pressure_simulation.py
    safety/
      policy_guard.py
```

## Safe Model Inputs

The model should use abstract parameters such as:

| Parameter | Meaning |
| --- | --- |
| replication_rate | Abstract viral replication tendency |
| mutation_pressure | Abstract variability pressure |
| immune_escape_score | Abstract immune evasion tendency |
| drug_susceptibility | Abstract treatment sensitivity |
| latency_probability | Abstract latency transition probability |
| reactivation_probability | Abstract reactivation probability |
| reservoir_decay_rate | Abstract reservoir decline tendency |
| viral_fitness | Abstract fitness score |
| immune_pressure | Abstract host immune pressure |
| therapy_pressure | Abstract therapy pressure |

## Explicit Non-Goals

The system must not provide:

- wet-lab engineering instructions
- actionable viral modification protocols
- procedural genetic manipulation steps
- synthesis instructions
- real pathogen construction workflows
- bypasses around biological safety review

## Safety Policy Guard

Every simulation request passes through a safety policy guard before execution.

```text
Research UI
-> API Gateway
-> Conductor
-> Simulation Service
-> Safety Policy Guard
-> Approved Abstract Digital Model
-> Kubernetes Job
```

The safety guard should validate:

- requested simulation type
- parameter ranges
- model version approval
- dataset permission
- user role
- audit requirements
- export restrictions

## Design Rule

We code an abstract digital model, not a real virus.
