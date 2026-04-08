import os
import json
from openai import OpenAI
from env import CloudGuardEnv
from schema import Action
from tasks import grade_easy_zombie_volumes, grade_medium_tagging, grade_hard_cost_optimization

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini") # Provide a default
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def log_step(step_num, action_str, reward, done, error=None):
    err_str = "null" if error is None else f'"{error}"'
    done_str = "true" if done else "false"
    print(f"[STEP] step={step_num} action={action_str} reward={reward:.2f} done={done_str} error={err_str}")

def run_task(task_name, grader_func):
    env = CloudGuardEnv()
    obs = env.reset()
    print(f"[START] task={task_name} env=cloudguard model={MODEL_NAME}")
    
    rewards = []
    max_steps = 3
    
    for step in range(1, max_steps + 1):
        prompt = f"""
        You are an autonomous Cloud FinOps agent. 
        Current State: {obs.model_dump_json()}
        Tasks: 1. Delete available EBS volumes. 2. Tag instances missing 'Project'. 3. Stop low CPU instances.
        Output ONLY raw JSON matching this schema: {{"action_type": "string", "resource_id": "string", "tag_key": "string", "tag_value": "string"}}.
        """
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            action_data = json.loads(response.choices[0].message.content)
            action = Action(**action_data)
            
            action_str = f"{action.action_type}('{action.resource_id}')"
            obs, reward, done, info = env.step(action)
            
            rewards.append(reward)
            log_step(step, action_str, reward, done, info.get("error"))
            
        except Exception as e:
            log_step(step, "error", 0.0, True, str(e))
            break
            
    final_score = grader_func(env.get_state())
    success_str = "true" if final_score > 0.8 else "false"
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={success_str} steps={len(rewards)} rewards={rewards_str}")

if __name__ == "__main__":
    run_task("easy-zombie-volumes", grade_easy_zombie_volumes)
    run_task("medium-tagging", grade_medium_tagging)
    run_task("hard-cost-optimization", grade_hard_cost_optimization)