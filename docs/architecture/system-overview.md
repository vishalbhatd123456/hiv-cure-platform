# System Overview

## Mission

The HIV Cure Research Platform is a distributed research operating system for safe computational analysis, cohort and sample workflows, clinical study coordination, and AI-assisted discovery.

The system is designed for research teams, clinicians, lab operators, trial coordinators, platform engineers, and data scientists.

## Core Principle

Netflix Conductor coordinates long-running research workflows. Domain services own domain state. Kubernetes and Argo execute heavy compute. Data stores are selected by access pattern rather than convenience.

## Layers

| Layer | Responsibility |
| --- | --- |
| Client | Research portal, admin console, future mobile app |
| Edge | API gateway, auth, rate limits, request shaping |
| Workflow | Netflix Conductor workflow definitions and workers |
| Domain | Cohort, sample, lab, trial, audit, notification services |
| Science | Simulation, omics, AI training, model registry, reporting |
| Compute | Kubernetes jobs, Argo workflows, CPU/GPU pools |
| Data | PostgreSQL, Redis, Kafka, object storage, OpenSearch, Neo4j |
| Governance | Consent, safety policy, audit, secrets, observability |

## Service Ownership

| Service | Primary Tech | Owns |
| --- | --- | --- |
| API Gateway | Node.js / NestJS | External API surface and BFF behavior |
| Cohort Service | Java / Spring Boot | De-identified cohort metadata |
| Sample Service | Java / Spring Boot | Sample inventory, chain of custody, biobank state |
| Lab Service | Java / Spring Boot | Assays, protocols, QC status, lab workflow state |
| Clinical Trial Service | .NET | Trial protocols, sites, visits, participant workflow state |
| Simulation Service | Python | Abstract in-silico simulations and run metadata |
| AI Training Service | Python | Training jobs, evaluation runs, model lifecycle hooks |
| Omics Service | Python | Omics pipeline orchestration and outputs |
| Knowledge Graph Service | Java / Python | Research entity relationships |
| Notification Service | Node.js | Email, webhook, Slack-style notification adapters |
| Audit Service | Java | Immutable audit events and compliance views |
| Safety Policy Service | Python / Java | Simulation and workflow guardrails |

## Data Boundaries

PostgreSQL stores transactional metadata. Object storage stores large files, results, datasets, and model artifacts. Redis handles short-lived cache, sessions, locks, and worker coordination. Kafka carries domain events. OpenSearch supports search and indexing. Neo4j stores research relationships.

## Workflow Boundary

Conductor should not become a database and should not contain business logic that belongs in services. It should coordinate tasks, retries, timeouts, compensation, approvals, and workflow visibility.
