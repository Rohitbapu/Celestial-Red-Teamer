import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional

class Sandbox:
    def __init__(self, challenge_dir: str):
        self.challenge_dir = Path(challenge_dir).absolute()
        # Create a fresh temporary directory for this episode
        self.workdir = Path(tempfile.mkdtemp(prefix="celestial_"))
        # Copy challenge files into workdir
        for item in self.challenge_dir.iterdir():
            dest = self.workdir / item.name
            if item.is_file():
                shutil.copy(item, dest)
            elif item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
        self.flag_location = self.get_flag_location()

    def exec_command(self, cmd: str) -> str:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.workdir),  # convert to string for subprocess
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out after 10 seconds"
        except Exception as e:
            return f"Error: {e}"

    def get_flag_location(self) -> Optional[str]:
        flag_file = self.challenge_dir / "flag.txt"
        if flag_file.exists():
            return flag_file.read_text().strip()
        return None

    def cleanup(self):
        shutil.rmtree(self.workdir, ignore_errors=True)
