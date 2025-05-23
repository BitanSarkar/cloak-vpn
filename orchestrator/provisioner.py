import subprocess, sys, json
from download_ovpn import download_ovpn_files
from constants import TERRAFORM_DIR, REGIONS_FILE
from utils import log, enable_ipv6, kill_process

def run_terraform_init():
    subprocess.run(["terraform", "init"], check=True, cwd=TERRAFORM_DIR)


def run_terraform_apply():
    subprocess.run(["terraform", "apply", "-auto-approve", f"-var-file={REGIONS_FILE}"], check=True, cwd=TERRAFORM_DIR)


def run_terraform_destroy():
    subprocess.run(["terraform", "destroy", "-auto-approve", f"-var-file={REGIONS_FILE}"], cwd=TERRAFORM_DIR)

def export_terraform_output():
    result = subprocess.run(["terraform", "output", "-json", "vpn_public_ips"], cwd=TERRAFORM_DIR, capture_output=True, text=True)
    output = json.loads(result.stdout)
    return output

def cleanup():
    log("Caught termination signal. Cleaning up...")
    enable_ipv6()
    run_terraform_destroy()
    sys.exit(0)
           
def startup():
    log("Initializing Terraform")
    run_terraform_init()

    log("Applying infrastructure")
    run_terraform_apply()

    log("Exporting terraform output json")
    ip_map = export_terraform_output()
    log(f"Got Terraform output JSON as {ip_map}")

    log("Exporting terraform outputs to file and Downloading .ovpn files from remote instances")
    download_ovpn_files(ip_map)