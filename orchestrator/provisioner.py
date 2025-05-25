import subprocess, sys, json
from download_ovpn import download_ovpn_files
from constants import TERRAFORM_DIR, REGIONS_FILE
from utils import log, enable_ipv6, kill_process
from vpn_connector import proc

def run_terraform_cmd_live(cmd, cwd, log_hook):
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        log_hook(line.rstrip())

    process.stdout.close()
    return_code = process.wait()

    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)

def run_terraform_init(log_hook=None):
    if log_hook:
        run_terraform_cmd_live(["terraform", "init"], cwd=TERRAFORM_DIR, log_hook=log_hook)
    else:
        subprocess.run(["terraform", "init"], check=True, cwd=TERRAFORM_DIR)

def run_terraform_apply(log_hook=None):
    if log_hook:
        run_terraform_cmd_live(["terraform", "apply", "-auto-approve", f"-var-file={REGIONS_FILE}"], cwd=TERRAFORM_DIR, log_hook=log_hook)
    else:
        subprocess.run(["terraform", "apply", "-auto-approve", f"-var-file={REGIONS_FILE}"], check=True, cwd=TERRAFORM_DIR)

def run_terraform_destroy(log_hook=None):
    if log_hook:
        run_terraform_cmd_live(["terraform", "destroy", "-auto-approve", f"-var-file={REGIONS_FILE}"], cwd=TERRAFORM_DIR, log_hook=log_hook)
    else:
        subprocess.run(["terraform", "destroy", "-auto-approve", f"-var-file={REGIONS_FILE}"], check=True, cwd=TERRAFORM_DIR)

def export_terraform_output():
    result = subprocess.run(["terraform", "output", "-json", "vpn_public_ips"], cwd=TERRAFORM_DIR, capture_output=True, text=True)
    output = json.loads(result.stdout)
    return output

def cleanup(log_hook=None):
    log("Caught termination signal. Cleaning up...", log_hook)
    kill_process(proc)
    enable_ipv6(log_hook)
    run_terraform_destroy(log_hook)
    sys.exit(0)
           
def startup(log_hook=None):
    log("Initializing Terraform", log_hook)
    run_terraform_init(log_hook)

    log("Applying Terraform", log_hook)
    run_terraform_apply(log_hook)

    log("Exporting terraform output json", log_hook)
    ip_map = export_terraform_output()
    log(f"Got Terraform output JSON as {ip_map}", log_hook)
    log("Exporting terraform outputs to file and Downloading .ovpn files from remote instances", log_hook)
    download_ovpn_files(ip_map, log_hook=log_hook)
