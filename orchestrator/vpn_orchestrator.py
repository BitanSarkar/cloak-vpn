import argparse, os, signal, time, random
from utils import require_sudo, disable_ipv6, log, kill_process, collect_ovpn_paths, connect_openvpn 
from constants import VPN_CONFIG_DIR
from provisioner import startup, cleanup
from vpn_connector import run_mode_full, run_mode_partial

def parse_args():
    parser = argparse.ArgumentParser(description="CloakVPN: Stealthy VPN Rotator with OpenVPN + Terraform")
    parser.add_argument("--mode", choices=["full", "partial"], default="full", help="Cloaking mode: full = IP+rotation, partial = fixed IP only")
    parser.add_argument("--rotate-interval", type=int, default=60, help="Interval in seconds to rotate VPN connections (only in full mode)")
    parser.add_argument("--region", type=str, default=None, help="Region to connect to in partial mode (e.g. us-east-1)")
    args = parser.parse_args()
    if args.mode == "partial" and not args.region:
        parser.error("--region is required when mode is partial")
    return args

def main():
    args = parse_args()
    global MODE, ROTATE_INTERVAL
    MODE = args.mode
    ROTATE_INTERVAL = args.rotate_interval
    region = args.region
    try:
        require_sudo()
        signal.signal(signal.SIGINT, lambda sig, frame: cleanup())
        signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())
        startup()
        ovpn_files = collect_ovpn_paths()
        log(f"Starting VPN mode: {MODE}")
        if MODE.casefold() == "partial".casefold():
            run_mode_partial(region, ovpn_files)
        elif MODE.casefold() == "full".casefold():
            run_mode_full(ovpn_files)
        else:
            log("Invalid mode. Use MODE=full or MODE=partial")
            cleanup()
    except Exception as e:
        log(f"[!] Got Error {e}")
        cleanup()


if __name__ == "__main__":
    main()