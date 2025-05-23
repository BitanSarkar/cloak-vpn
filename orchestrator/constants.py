from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
TERRAFORM_DIR = BASE_DIR / "terraform"
ORCHESTRATOR_DIR = BASE_DIR / "orchestrator"
VPN_CONFIG_DIR = ORCHESTRATOR_DIR / "vpn-configs"
REGIONS_FILE = ORCHESTRATOR_DIR / "regions.json"
LOG_FILE = ORCHESTRATOR_DIR / "cloakvpn.log"
ORCHESTRATOR_SCRIPT = ORCHESTRATOR_DIR / "vpn_orchestrator.py"

AVAILABLE_REGIONS = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "eu-central-1", "eu-west-1", "ap-south-1", "ap-northeast-1"
]