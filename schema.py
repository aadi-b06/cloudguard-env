from pydantic import BaseModel
from typing import List, Optional, Dict

class Resource(BaseModel):
    id: str
    type: str  # "ec2" or "ebs"
    state: str # "running", "stopped", "available", "deleted"
    tags: Dict[str, str]
    cost_per_hr: float
    cpu_utilization_pct: float
    attached_to: Optional[str] = None

class Action(BaseModel):
    action_type: str # "terminate", "delete", "stop", "add_tag"
    resource_id: str
    tag_key: Optional[str] = None
    tag_value: Optional[str] = None

class Observation(BaseModel):
    resources: List[Resource]
    current_hourly_cost: float
    message: str