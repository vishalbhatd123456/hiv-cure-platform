# Service Catalog

## Client Applications

| Service | Tech | Purpose |
| --- | --- | --- |
| research-portal | React / Next.js | Researcher workflows, simulations, cohort/sample views |
| admin-console | React / Next.js | Platform operations, approvals, access governance |

## Edge Services

| Service | Tech | Purpose |
| --- | --- | --- |
| api-gateway | Node.js / NestJS | Public API, BFF, auth enforcement, request shaping |
| identity-provider | Keycloak | OIDC login, organizations, roles, service accounts |

## Domain Services

| Service | Tech | Purpose |
| --- | --- | --- |
| cohort-service | Java / Spring Boot | Cohort metadata and eligibility logic |
| sample-service | Java / Spring Boot | Biobank inventory and sample chain of custody |
| lab-service | Java / Spring Boot | Protocols, assays, QC, lab workflow state |
| clinical-trial-service | .NET | Trial protocol, site, visit, and participant workflows |
| audit-service | Java | Immutable compliance and platform audit records |
| notification-service | Node.js | Notification routing and templates |
| knowledge-graph-service | Java / Python | Research graph of samples, studies, hypotheses, biomarkers |

## Science Services

| Service | Tech | Purpose |
| --- | --- | --- |
| simulation-service | Python | Abstract digital HIV simulations and run management |
| safety-policy-service | Python / Java | Guardrails for simulation and data-access workflows |
| ai-training-service | Python / PyTorch | Training, evaluation, and model lifecycle hooks |
| omics-service | Python | Omics workflow submission and result collection |
| model-registry-service | Python / Java | Model artifact registration, model cards, approval states |
| research-report-service | Node.js / Python | Report assembly from workflow outputs |

## Workflow Services

| Service | Tech | Purpose |
| --- | --- | --- |
| conductor-server | Netflix Conductor | Workflow orchestration |
| java-workers | Java | Domain workflow tasks |
| dotnet-workers | .NET | Clinical trial workflow tasks |
| python-workers | Python | Scientific compute launch tasks |
| node-workers | Node.js | Notification and adapter tasks |

## Infrastructure Services

| Service | Tech | Purpose |
| --- | --- | --- |
| postgres | PostgreSQL | Transactional metadata |
| redis | Redis | Sessions, cache, locks, lightweight coordination |
| kafka | Kafka | Event streaming |
| object-storage | S3 / MinIO | Datasets, outputs, model artifacts |
| opensearch | OpenSearch | Search and indexing |
| neo4j | Neo4j | Knowledge graph |
| observability | OTEL, Prometheus, Grafana, Loki | Logs, metrics, traces |
| secrets | Vault / KMS | Secrets and encryption keys |
