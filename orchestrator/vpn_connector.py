import random, os, time
from utils import log, disable_ipv6, connect_openvpn, kill_process, enable_ipv6
from constants import VPN_CONFIG_DIR

proc = None

def run_mode_partial(region, ovpn_files, log_hook=None):
    global proc
    filtered = [f for f in ovpn_files if f.startswith(os.path.join(VPN_CONFIG_DIR, f"{region}-"))]
    if not filtered:
        log(f"[!] No .ovpn files found for region: {region}", log_hook)
        raise Exception("No .ovpn files found. Exiting.")
    disable_ipv6(log_hook)
    proc = connect_openvpn(random.choice(filtered), log_hook)
    proc.wait()


def run_mode_full(ovpn_files, ROTATE_INTERVAL = 60, log_hook=None):
    global proc
    if not ovpn_files:
        log("No .ovpn files found. Exiting.", log_hook)
        raise Exception("No .ovpn files found. Exiting.")
    disable_ipv6(log_hook)
    while True:
        config = random.choice(ovpn_files)
        region = os.path.basename(config).split(".")[0]
        proc = connect_openvpn(config, log_hook)
        log(f"Connected to {region} for {ROTATE_INTERVAL}s", log_hook)
        time.sleep(ROTATE_INTERVAL)
        kill_process(proc, log_hook)
def run_mode_partial(region, ovpn_files, stop_event, log_hook=None):
    global proc
    log(f"[*] Got region {region} for partial start-up", log_hook)
    filtered = [f for f in ovpn_files if f.startswith(os.path.join(VPN_CONFIG_DIR, f"{region}"))]
    if not filtered:
        log(f"[!] No .ovpn files found for region: {region}", log_hook)
        raise Exception("No .ovpn files found. Exiting.")

    disable_ipv6(log_hook)
    proc = connect_openvpn(random.choice(filtered), log_hook)

    # Wait loop
    while not stop_event.is_set():
        if proc.poll() is not None:  # process exited on its own
            log("[VPN] Process exited.", log_hook)
            break
        time.sleep(1)

    kill_process(proc, log_hook)
    proc = None

def run_mode_full(ovpn_files, ROTATE_INTERVAL, stop_event, log_hook=None):
    global proc
    if not ovpn_files:
        log("No .ovpn files found. Exiting.", log_hook)
        raise Exception("No .ovpn files found. Exiting.")

    disable_ipv6(log_hook)

    while not stop_event.is_set():
        config = random.choice(ovpn_files)
        region = os.path.basename(config).split(".")[0]
        log(f"[VPN] Connecting to {region}...", log_hook)

        proc = connect_openvpn(config, log_hook)
        start = time.time()

        # Wait for the interval or until the process ends early
        while time.time() - start < ROTATE_INTERVAL:
            if stop_event.is_set():
                break
            if proc.poll() is not None:
                log("[VPN] Process exited early.", log_hook)
                break
            time.sleep(1)

        kill_process(proc, log_hook)
        proc = None

def stop_vpn(log_hook=None):
    global proc
    log("Caught termination signal. Cleaning up...", log_hook)
    if proc:
        kill_process(proc, log_hook)
        proc = None
    enable_ipv6(log_hook)