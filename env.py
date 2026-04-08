import copy
from schema import Resource, Action, Observation

# The starting state of our simulated cloud
INITIAL_STATE = [
    Resource(id="i-01", type="ec2", state="running", tags={"Env": "Prod", "Project": "Core"}, cost_per_hr=1.5, cpu_utilization_pct=85.0),
    Resource(id="i-02", type="ec2", state="running", tags={"Env": "Dev"}, cost_per_hr=0.5, cpu_utilization_pct=2.0), # Missing Project tag, wasting money
    Resource(id="vol-01", type="ebs", state="in-use", tags={"Env": "Prod"}, cost_per_hr=0.1, cpu_utilization_pct=0.0, attached_to="i-01"),
    Resource(id="vol-02", type="ebs", state="available", tags={}, cost_per_hr=0.2, cpu_utilization_pct=0.0), # Zombie volume
]

class CloudGuardEnv:
    def __init__(self):
        self.state = []
        self.reset()

    def reset(self) -> Observation:
        self.state = [copy.deepcopy(r) for r in INITIAL_STATE]
        return self._get_obs("Environment reset.")

    def _get_obs(self, message: str) -> Observation:
        cost = sum(r.cost_per_hr for r in self.state if r.state not in ["deleted", "terminated"])
        return Observation(resources=self.state, current_hourly_cost=cost, message=message)

    def get_state(self):
        return self.state

    def step(self, action: Action) -> tuple[Observation, float, bool, dict]:
        resource = next((r for r in self.state if r.id == action.resource_id), None)
        if not resource:
            return self._get_obs("Error: Resource not found."), -0.1, False, {"error": "not_found"}

        msg = ""
        reward = 0.0

        if action.action_type == "delete" and resource.type == "ebs":
            if resource.state == "available":
                resource.state = "deleted"
                msg = f"Deleted unattached volume {resource.id}"
                reward = 0.5 # Good partial progress
            else:
                msg = f"Cannot delete in-use volume {resource.id}"
                reward = -0.5 # Penalize destructive behavior

        elif action.action_type == "stop" and resource.type == "ec2":
            resource.state = "stopped"
            msg = f"Stopped instance {resource.id}"
            reward = 0.2

        elif action.action_type == "terminate" and resource.type == "ec2":
            resource.state = "terminated"
            msg = f"Terminated instance {resource.id}"
            reward = 0.1

        elif action.action_type == "add_tag":
            if action.tag_key and action.tag_value:
                resource.tags[action.tag_key] = action.tag_value
                msg = f"Added tag {action.tag_key}={action.tag_value} to {resource.id}"
                reward = 0.2
            else:
                msg = "Missing tag key/value"
                reward = -0.1
        else:
            msg = f"Invalid action {action.action_type} for {resource.type}"
            reward = -0.1

        return self._get_obs(msg), reward, False, {}