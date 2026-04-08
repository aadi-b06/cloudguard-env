from fastapi import FastAPI
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