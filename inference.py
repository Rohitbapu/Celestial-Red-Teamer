#!/usr/bin/env python3
import sys
import time

def main():
    # Simulate three tasks
    tasks = ["easy", "medium", "hard"]
    for task in tasks:
        print(f"[START] task={task} env=test model=dummy", flush=True)
        # Simulate a few steps
        for step in range(1, 4):
            reward = 0.33 if step < 3 else 0.99
            done = (step == 3)
            print(f"[STEP] step={step} action=test_action reward={reward:.2f} done={str(done).lower()} error=null", flush=True)
        # End task
        success = True
        final_score = 0.999
        rewards = [0.33, 0.33, 0.99]
        r_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps=3 score={final_score:.3f} rewards={r_str}", flush=True)
        time.sleep(1)

if __name__ == "__main__":
    main()