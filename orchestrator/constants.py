from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
TERRAFORM_DIR = BASE_DIR / "terraform"
ORCHESTRATOR_DIR = BASE_DIR / "orchestrator"
VPN_CONFIG_DIR = ORCHESTRATOR_DIR / "vpn-configs"
REGIONS_FILE = ORCHESTRATOR_DIR / "regions.json"
LOG_FILE = ORCHESTRATOR_DIR / "cloakvpn.log"
ORCHESTRATOR_SCRIPT = ORCHESTRATOR_DIR / "vpn_orchestrator.py"

AVAILABLE_REGIONS = sorted([
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "ca-central-1",
    "sa-east-1",
    "eu-west-1", "eu-west-2", "eu-west-3",
    "eu-central-1", "eu-central-2",
    "eu-north-1", "eu-south-1", "eu-south-2",
    "me-central-1", "me-south-1",
    "il-central-1",
    "af-south-1",
    "ap-south-1", "ap-south-2",
    "ap-southeast-1", "ap-southeast-2", "ap-southeast-3", "ap-southeast-4", "ap-southeast-5", "ap-southeast-7",
    "ap-east-1",
    "ap-northeast-1", "ap-northeast-2", "ap-northeast-3"
])

REGION_CITY_MAP = {
    "us-east-1": "N. Virginia, USA",
    "us-east-2": "Ohio, USA",
    "us-west-1": "N. California, USA",
    "us-west-2": "Oregon, USA",
    "ca-central-1": "Central Canada",
    "sa-east-1": "São Paulo, Brazil",
    
    "eu-west-1": "Ireland",
    "eu-west-2": "London, UK",
    "eu-west-3": "Paris, France",
    "eu-central-1": "Frankfurt, Germany",
    "eu-central-2": "Zurich, Switzerland",
    "eu-north-1": "Stockholm, Sweden",
    "eu-south-1": "Milan, Italy",
    "eu-south-2": "Spain",
    
    "me-central-1": "UAE",
    "me-south-1": "Bahrain",
    "il-central-1": "Tel Aviv, Israel",
    
    "af-south-1": "Cape Town, South Africa",
    
    "ap-south-1": "Mumbai, India",
    "ap-south-2": "Hyderabad, India",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Sydney, Australia",
    "ap-southeast-3": "Jakarta, Indonesia",
    "ap-southeast-4": "Melbourne, Australia",
    "ap-southeast-5": "Auckland, New Zealand",
    "ap-southeast-7": "Bangkok, Thailand",
    
    "ap-east-1": "Hong Kong",
    
    "ap-northeast-1": "Tokyo, Japan",
    "ap-northeast-2": "Seoul, South Korea",
    "ap-northeast-3": "Osaka, Japan"
}