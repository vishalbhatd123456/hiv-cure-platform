# Python Conductor Workers

Workers for scientific workflow tasks.

Initial task ownership:

- validate_simulation_safety_policy
- select_approved_digital_model
- prepare_simulation_parameters
- launch_kubernetes_simulation_job
- wait_for_simulation_completion
- collect_simulation_results

## Current Implementation

`simulation_worker.py` is a first adapter skeleton. It maps Conductor-style
task input into calls to `services/simulation-service`.

The first version runs against the inline toy simulation service. Later it will
be replaced by a real Conductor polling loop and Kubernetes job submission.
