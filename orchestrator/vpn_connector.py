import random, os, time
from utils import log, disable_ipv6, connect_openvpn, kill_process
from constants import VPN_CONFIG_DIR

proc = None

def run_mode_partial(region, ovpn_files):
    global proc
    filtered = [f for f in ovpn_files if f.startswith(os.path.join(VPN_CONFIG_DIR, f"{region}-"))]
    if not filtered:
        log(f"[!] No .ovpn files found for region: {region}")
        raise Exception("No .ovpn files found. Exiting.")
    disable_ipv6()
    proc = connect_openvpn(random.choice(filtered))
    proc.wait()


def run_mode_full(ovpn_files, ROTATE_INTERVAL = 60):
    global proc
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