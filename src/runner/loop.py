#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.agent.brain import LLMBrain
from src.agent.parser import validate_command
from src.environment.sandbox import Sandbox
from src.environment.guardrails import truncate_observation

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Celestial Red Teamer")
    parser.add_argument("--challenge", type=str, default="easy", help="Challenge subfolder (easy/medium/hard)")
    parser.add_argument("--max-steps", type=int, default=30)
    args = parser.parse_args()
    
    challenge_path = Path(f"challenges/{args.challenge}")
    if not challenge_path.exists():
        console.print(f"[red]Challenge {args.challenge} not found![/red]")
        sys.exit(1)
    
    console.print(f"[bold cyan]🚀 Celestial Red Teamer[/bold cyan]")
    console.print(f"Challenge: {args.challenge} | Max steps: {args.max_steps}")
    
    sandbox = Sandbox(str(challenge_path))
    brain = LLMBrain()
    history = []
    
    flag_location = sandbox.get_flag_location() or "FLAG{"
    step = 0
    success = False
    
    try:
        obs = sandbox.exec_command("pwd && whoami && ls -la")
        obs = truncate_observation(obs)
        
        while step < args.max_steps and not success:
            step += 1
            console.print(f"\n[bold blue]Step {step}[/bold blue]")
            cmd = brain.get_command(obs, history)
            console.print(f"[green]🤖 AI command:[/green] {cmd}")
            
            safe, err = validate_command(cmd)
            if not safe:
                console.print(f"[red]⛔ Guardrail blocked: {err}[/red]")
                obs = f"Command rejected: {err}"
                history.append({"role": "assistant", "content": cmd})
                history.append({"role": "user", "content": obs})
                continue
            
            output = sandbox.exec_command(cmd)
            output = truncate_observation(output)
            console.print(f"[dim]📟 Output:\n{output}[/dim]")
            
            if flag_location in output or "FLAG{" in output:
                console.print("[bold green]🏆 FLAG FOUND! 🏆[/bold green]")
                success = True
                break
            
            obs = output
            history.append({"role": "assistant", "content": cmd})
            history.append({"role": "user", "content": obs})
        
        console.print(f"[bold green]✅ Success in {step} steps![/bold green]" if success else f"[bold red]❌ Failed after {args.max_steps} steps[/bold red]")
    finally:
        sandbox.cleanup()
        console.print("[dim]Sandbox destroyed.[/dim]")

if __name__ == "__main__":
    main()