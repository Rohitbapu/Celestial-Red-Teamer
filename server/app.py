import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from typing import Dict, Any, Optional
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.environment.sandbox import Sandbox
from src.environment.guardrails import truncate_observation
from src.agent.parser import validate_command

app = FastAPI(title="Celestial Red Teamer Environment")

class ResetRequest(BaseModel):
    challenge: str = "easy"

class CelestialAction(BaseModel):
    command: str

class StepResult(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = {}

class State(BaseModel):
    observation: Dict[str, Any]
    done: bool
    info: Dict[str, Any] = {}

sandbox = None
flag_location = None
current_challenge = "easy"

def init_env(challenge: str = "easy"):
    global sandbox, flag_location, current_challenge
    if sandbox:
        sandbox.cleanup()
    challenge_path = Path("challenges") / challenge
    sandbox = Sandbox(str(challenge_path))
    flag_location = sandbox.get_flag_location() or "FLAG{"
    current_challenge = challenge
    out = sandbox.exec_command("pwd && whoami && ls -la")
    out = truncate_observation(out)
    return State(observation={"output": out}, done=False, info={})

@app.on_event("startup")
async def startup():
    init_env()

@app.post("/reset")
async def reset(req: ResetRequest = None):
    challenge = req.challenge if req else "easy"
    state = init_env(challenge)
    return state.model_dump()

@app.post("/step")
async def step(action: CelestialAction):
    global sandbox, flag_location
    cmd = action.command.strip()
    safe, err = validate_command(cmd)
    if not safe:
        out = f"Command rejected: {err}"
    else:
        out = sandbox.exec_command(cmd)
        out = truncate_observation(out)
    
    done = (flag_location in out) or ("FLAG{" in out)
    
    # SCORE FIX: 0.99 instead of 1.0 to stay strictly between 0 and 1
    reward = 0.99 if done else 0.01
    
    return StepResult(
        observation={"output": out}, 
        reward=reward, 
        done=done, 
        info={"challenge": current_challenge}
    ).model_dump()

@app.get("/state")
async def state():
    return State(observation={"output": f"Current challenge: {current_challenge}"}, done=False, info={}).model_dump()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
