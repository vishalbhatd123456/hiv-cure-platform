# Netflix Conductor Workflow Architecture

## Role

Netflix Conductor is the workflow brain of the platform. It coordinates multi-step research processes that cross service boundaries and may run for minutes, hours, or days.

Conductor decides what happens next. Domain services decide what their data means.

## Worker Families

| Worker Family | Tech | Example Tasks |
| --- | --- | --- |
| Java workers | Spring Boot | Cohort validation, sample state transitions, audit writes |
| .NET workers | ASP.NET Core Worker Service | Trial site approvals, visit workflow, clinical review steps |
| Python workers | FastAPI / worker runtime | Simulation launch, AI training launch, omics pipeline submission |
| Node workers | NestJS | Notifications, collaboration events, external adapters |

## Primary Workflows

### Cohort Enrollment

```text
create_cohort
-> validate_consent_scope
-> deidentify_records
-> evaluate_inclusion_exclusion
-> approve_cohort
-> write_audit_event
-> notify_research_team
```

### Sample Processing

```text
register_sample
-> verify_chain_of_custody
-> assign_lab_protocol
-> perform_quality_control
-> upload_assay_result
-> approve_or_reject_sample
-> index_result_metadata
-> write_audit_event
```

### Omics Analysis

```text
upload_omics_files
-> validate_file_integrity
-> run_qc
-> preprocess_data
-> launch_argo_pipeline
-> collect_outputs
-> index_results
-> notify_researcher
```

### Simulation Run

```text
create_simulation_request
-> validate_safety_policy
-> select_approved_model
-> prepare_parameter_set
-> launch_kubernetes_job
-> monitor_execution
-> collect_results
-> generate_report
-> compare_previous_runs
```

### AI Training

```text
select_approved_dataset
-> validate_data_access
-> prepare_features
-> launch_training_job
-> evaluate_model
-> register_model_artifact
-> generate_model_card
-> request_review
-> publish_approved_model
```

## Conductor and Compute

Conductor does not run heavy scientific compute directly. It starts and observes compute through service tasks.

```text
Conductor
-> Python worker
-> Simulation or AI service
-> Kubernetes Job / Argo Workflow
-> Object Storage
-> PostgreSQL status update
-> Kafka progress events
```

## Failure Handling

Each workflow should define:

- timeout budgets
- retry policy
- compensation steps
- manual review states
- dead letter handling
- audit emission
- idempotency keys

## First Workflow To Implement

The first production-shaped workflow should be `simulation_run_v1` because it exercises the core platform path: API gateway, Conductor, Python worker, safety policy, simulation service, Kubernetes job, object storage, PostgreSQL, and notification.
