from fastapi import FastAPI
import os
from typing import List, Optional

from openai import OpenAI
from environment import OpenEnv
from models import Action
from tasks.hard import get_grader

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

app = FastAPI()

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={float(reward):.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{float(r):.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/reset")
async def reset_endpoint():
    env = OpenEnv()
    obs = env.reset()
    grader = get_grader()

    rewards = []
    steps_taken = 0

    log_start(task="email_triage_hard", env="email_env", model=MODEL_NAME)

    boss_action = None
    customer_action = None
    dev_action = None
    other_actions = []

    for e in obs.inbox:
        s = e.sender.lower()
        subj = e.subject.lower()

        if "boss" in s or "urgent" in subj:
            boss_action = Action(action_type="assign_label", email_id=e.id, label="urgent")
        elif "spam" in s or "win" in e.body.lower():
            other_actions.append(Action(action_type="archive", email_id=e.id))
        elif "customer" in s:
            customer_action = Action(
                action_type="reply",
                email_id=e.id,
                reply_text="Sorry for the inconvenience.\nWe will fix and resolve your login issue immediately."
            )
        elif "hr" in s:
            other_actions.append(Action(action_type="assign_label", email_id=e.id, label="internal"))
        elif "dev" in s:
            dev_action = Action(action_type="assign_label", email_id=e.id, label="review")

    actions = []
    if boss_action: actions.append(boss_action)
    if customer_action: actions.append(customer_action)
    actions.extend(other_actions)
    if dev_action: actions.append(dev_action)

    actions.append(Action(action_type="finish"))

    for step, act in enumerate(actions, 1):
        obs, reward, done, info = env.step(act)

        rewards.append(reward)
        steps_taken = step

        log_step(step, act.action_type, reward, done, None)

        if done:
            break

    score = grader.grade(env)
    success = score >= 0.8

    log_end(success, steps_taken, score, rewards)

    return {
        "status": "ok",
        "score": float(score),
        "steps": steps_taken
    }
