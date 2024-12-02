"""SSH connection and command execution management."""

import paramiko
from typing import Tuple, Optional
from config import SSH_TIMEOUT, SystemConfig

class SSHManager:
    def __init__(self, username: str, key_path: str):
        self.username = username
        self.key_path = key_path
        self._client: Optional[paramiko.SSHClient] = None

    def connect(self, system: SystemConfig) -> None:
        """Establish SSH connection to the target system."""
        try:
            self._client = paramiko.SSHClient()
            self._client.load_system_host_keys()
            self._client.connect(
                hostname=system.ip,
                username=self.username,
                key_filename=self.key_path,
                timeout=SSH_TIMEOUT
            )
        except Exception as e:
            if self._client:
                self._client.close()
            raise ConnectionError(f"Failed to connect to {system.hostname}: {str(e)}")

    def execute_script(self, script_path: str) -> Tuple[str, str]:
        """Execute script on the remote system."""
        if not self._client:
            raise RuntimeError("Not connected to any system")

        try:
            stdin, stdout, stderr = self._client.exec_command(
                f"bash {script_path}",
                timeout=SSH_TIMEOUT
            )
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            raise RuntimeError(f"Script execution failed: {str(e)}")
        finally:
            self._client.close()
            self._client = None