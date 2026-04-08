import sys
import os
# This allows app.py to find env.py and schema.py in the main folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
import uvicorn
from schema import Action, Observation
from env import CloudGuardEnv

app = FastAPI()
environment = CloudGuardEnv()

@app.get("/")
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset", response_model=Observation)
def reset():
    return environment.reset()

@app.get("/state")
def state():
    return environment.get_state()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = environment.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
