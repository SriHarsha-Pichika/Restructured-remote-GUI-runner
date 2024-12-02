"""Configuration settings for the Remote Script Runner."""

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class SystemConfig:
    hostname: str
    ip: str

# System configuration
SYSTEMS: Dict[str, Optional[SystemConfig]] = {
    "399001 - migkit193_ha": SystemConfig(hostname="migkit193_ha", ip="10.10.193.1"),
    "399001 Virtual - vmigkit193_ha": SystemConfig(hostname="vmigkit193_ha", ip="10.10.193.1"),
    "399002 - migkit194_ha": SystemConfig(hostname="migkit194_ha", ip="10.10.194.1"),
    "399002 Virtual - vmigkit194_ha": SystemConfig(hostname="vmigkit194_ha", ip="10.10.194.1"),
    "All Systems": None
}

# SSH Configuration
SSH_TIMEOUT = 30  # seconds
KEY_PATH = "~/.ssh/id_rsa"