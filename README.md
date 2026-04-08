# CloudGuard-Env: Cloud FinOps & Governance

## Motivation & Real-World Utility
Cloud waste is a multi-billion dollar enterprise problem. Autonomous agents have immense potential to audit infrastructure, identify "zombie" resources, enforce security tagging, and optimize costs. **CloudGuard-Env** models a genuine Cloud FinOps process where an agent must traverse a simulated provider state, weighing cost optimization against the risk of destructive actions on production resources.

## Action & Observation Spaces
The environment relies on structured JSON (simulating cloud provider APIs):
* **Observation Space:** A list of `Resource` objects (EC2 instances, EBS volumes) with attributes for `state`, `tags`, `cost_per_hr`, and `cpu_utilization_pct`, along with the `current_hourly_cost`.
* **Action Space:** A JSON object allowing `terminate`, `delete`, `stop`, or `add_tag` on specific `resource_id`s.

## Tasks & Difficulty Progression
1. **Easy (The Zombie Reaper):** Identify and `delete` unattached ("available") EBS volumes to reduce baseline costs.
2. **Medium (Governance Enforcer):** Identify active EC2 instances missing mandatory governance tags (e.g., `Project`) and apply the correct `add_tag` action.
3. **Hard (Cost Optimization):** Analyze the `cpu_utilization_pct` of all instances. Safely `stop` or `terminate` severely underutilized instances while leaving vital production instances running.

## Setup & Usage
**Prerequisites:** Python 3.10+, Docker (optional)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set Environment Variables
export API_BASE_URL="[https://api.openai.com/v1](https://api.openai.com/v1)"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your_hf_token_here"

# 3. Run Inference Baseline
python inference.py