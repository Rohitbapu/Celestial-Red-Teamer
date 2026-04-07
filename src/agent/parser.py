import re
from typing import Tuple

ALLOWED_COMMANDS = {
    "ls", "cat", "echo", "ifconfig", "netstat", "nmap", "curl", "wget",
    "ps", "grep", "find", "head", "tail", "cd", "pwd", "whoami", "id",
    "python3", "python", "nc", "telnet"
}

DANGEROUS_PATTERNS = [
    r"rm\s+-rf", r"dd\s+if=", r"mkfs", r">\s*/dev/sd", r":\(\)\s*\{\s*:\|:&\s*\};:",
    r"chmod\s+777", r"sudo", r"docker", r"kill"
]

def validate_command(cmd: str) -> Tuple[bool, str]:
    cmd_lower = cmd.lower().strip()
    if not cmd_lower:
        return False, "Empty command"
    first_word = cmd_lower.split()[0]
    if first_word not in ALLOWED_COMMANDS:
        return False, f"Command '{first_word}' not allowed"
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd_lower):
            return False, f"Blocked: {pattern}"
    return True, ""