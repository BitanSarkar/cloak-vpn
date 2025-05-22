import argparse
import json
import subprocess
import os
import signal
import sys
import time
import random
from datetime import datetime
from download_ovpn import download_ovpn_files


TERRAFORM_DIR = os.path.dirname(os.path.abspath(__file__))
REGIONS_FILE = os.path.join(TERRAFORM_DIR, "regions.json")
VPN_CONFIG_DIR = os.path.join(TERRAFORM_DIR, "vpn-configs")
PUBLIC_IPS_FILE = os.path.join(TERRAFORM_DIR, "vpn_public_ips.json")
LOG_FILE = os.path.join(TERRAFORM_DIR, f"cloakvpn.log")

def parse_args():
    parser = argparse.ArgumentParser(description="CloakVPN: Stealthy VPN Rotator with OpenVPN + Terraform")
    parser.add_argument("--mode", choices=["full", "partial"], default="full", help="Cloaking mode: full = IP+rotation, partial = fixed IP only")
    parser.add_argument("--rotate-interval", type=int, default=60, help="Interval in seconds to rotate VPN connections (only in full mode)")
    parser.add_argument("--region", type=str, default=None, help="Region to connect to in partial mode (e.g. us-east-1)")
    args = parser.parse_args()

    # Validate that --region is required if mode is partial
    if args.mode == "partial" and not args.region:
        parser.error("--region is required when mode is partial")
    return args

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[+] {msg}")


def load_regions():
    with open(REGIONS_FILE, "r") as f:
        return json.load(f)


def run_terraform_init():
    subprocess.run(["terraform", "init"], check=True, cwd=TERRAFORM_DIR)


def run_terraform_apply():
    subprocess.run(["terraform", "apply", "-auto-approve", f"-var-file={REGIONS_FILE}"], check=True, cwd=TERRAFORM_DIR)


def run_terraform_destroy():
    subprocess.run(["terraform", "destroy", "-auto-approve", f"-var-file={REGIONS_FILE}"], cwd=TERRAFORM_DIR)


def export_terraform_output():
    result = subprocess.run(["terraform", "output", "-json"], cwd=TERRAFORM_DIR, capture_output=True, text=True)
    output = json.loads(result.stdout)
    with open(PUBLIC_IPS_FILE, "w") as f:
        json.dump(output.get("vpn_public_ips", {}), f, indent=2)
    return output.get("vpn_public_ips", {})

def get_network_services():
    result = subprocess.run(["networksetup", "-listallnetworkservices"], capture_output=True, text=True)
    services = result.stdout.strip().splitlines()
    return [s.strip("*").strip() for s in services if not s.startswith("*")]

def disable_ipv6_mac():
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6off", service])
        print(f"[+] IPv6 disabled for: {service}")

def enable_ipv6_mac():
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6automatic", service])
        print(f"[+] IPv6 re-enabled for: {service}")

def disable_ipv6():
    log("Disabling IPv6")
    if sys.platform == "darwin":
        disable_ipv6_mac()
    elif sys.platform.startswith("linux"):
        subprocess.run("sysctl -w net.ipv6.conf.all.disable_ipv6=1", shell=True)
        subprocess.run("sysctl -w net.ipv6.conf.default.disable_ipv6=1", shell=True)


def enable_ipv6():
    log("Enabling IPv6")
    if sys.platform == "darwin":
        enable_ipv6_mac()
    elif sys.platform.startswith("linux"):
        subprocess.run("sysctl -w net.ipv6.conf.all.disable_ipv6=0", shell=True)
        subprocess.run("sysctl -w net.ipv6.conf.default.disable_ipv6=0", shell=True)


def connect_openvpn(config_path):
    log(f"Connecting OpenVPN: {os.path.basename(config_path)}")
    return subprocess.Popen(["openvpn", "--config", config_path])


def kill_process(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


def collect_ovpn_paths():
    return [os.path.join(VPN_CONFIG_DIR, f) for f in os.listdir(VPN_CONFIG_DIR) if f.endswith(".ovpn")]


def run_mode_partial(region):
    ovpn_files = collect_ovpn_paths()
    filtered = [f for f in ovpn_files if f.startswith(os.path.join(VPN_CONFIG_DIR, f"{region}-"))]
    if not filtered:
        log(f"[!] No .ovpn files found for region: {region}")
        raise Exception("No .ovpn files found. Exiting.")
        return
    disable_ipv6()
    proc = connect_openvpn(filtered[0])
    proc.wait()


def run_mode_full():
    ovpn_files = collect_ovpn_paths()
    if not ovpn_files:
        log("No .ovpn files found. Exiting.")
        raise Exception("No .ovpn files found. Exiting.")
    
    disable_ipv6()
    while True:
        config = random.choice(ovpn_files)
        region = os.path.basename(config).split(".")[0]
        proc = connect_openvpn(config)
        log(f"Connected to {region} for {ROTATE_INTERVAL}s")
        time.sleep(ROTATE_INTERVAL)
        kill_process(proc)


# --- MAIN AUTOMATION ---
def main():
    args = parse_args()
    global MODE, ROTATE_INTERVAL
    MODE = args.mode
    ROTATE_INTERVAL = args.rotate_interval
    region = args.region
    try:
        if os.geteuid() != 0:
            print("This script must be run with sudo/root privileges.")
            sys.exit(1)

        def cleanup():
            log("Caught termination signal. Cleaning up...")
            enable_ipv6()
            run_terraform_destroy()
            sys.exit(0)

        signal.signal(signal.SIGINT, lambda sig, frame: cleanup())
        signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())

        log("Initializing Terraform")
        run_terraform_init()

        log("Applying infrastructure")
        run_terraform_apply()

        log("Exporting terraform outputs to file and Downloading .ovpn files from remote instances")
        download_ovpn_files()

        log(f"Starting VPN mode: {MODE}")
        if MODE.casefold() == "partial".casefold():
            run_mode_partial(region)
        elif MODE.casefold() == "full".casefold():
            run_mode_full()
        else:
            log("Invalid mode. Use MODE=full or MODE=partial")
            cleanup()
    except Exception as e:
        log(f"[!] Got Error {e}")
        cleanup()


if __name__ == "__main__":
    main()