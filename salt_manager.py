"""SaltStack command execution management."""

import subprocess
from typing import Tuple

class SaltManager:
    @staticmethod
    def execute_script(script_path: str) -> Tuple[str, str]:
        """Execute script on all systems using SaltStack."""
        try:
            result = subprocess.run(
                ["salt", "*", "cmd.run", f"bash {script_path}"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"SaltStack execution failed: {str(e)}")