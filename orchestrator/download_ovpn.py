import os
import json
import subprocess
import time
from utils import log
from pathlib import Path

MAX_WAIT = 180  # seconds
RETRY_INTERVAL = 10  # seconds

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "vpn-configs"))
KEY_PATH = os.path.expanduser("~/.ssh/ghostvpn")

def wait_for_ovpn(ip, retries=MAX_WAIT // RETRY_INTERVAL, log_hook=None):
    for attempt in range(1, retries + 1):
        ssh_cmd = [
            "ssh", "-i", KEY_PATH,
            "-o", "StrictHostKeyChecking=no",
            f"ec2-user@{ip}",
            "sudo cat /root/client.ovpn"
        ]
        log(f"[{ip}] Attempt {attempt}: Fetching .ovpn via SSH...", log_hook)
        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True)

            if result.returncode == 0 and "BEGIN" in result.stdout:
                log(f"[{ip}] ✅ Successfully retrieved .ovpn on attempt {attempt}", log_hook)
                return result.stdout
            else:
                log(f"[{ip}] ❌ Failed on attempt {attempt}, return code {result.returncode}", log_hook)
                if result.stderr:
                    log(f"[{ip}] STDERR: {result.stderr.strip()}", log_hook)
        except Exception as e:
            log(f"[{ip}] ⚠ SSH exception on attempt {attempt}: {e}", log_hook)
            pass
        time.sleep(RETRY_INTERVAL)

    log(f"[{ip}] ❌ All {retries} attempts failed to fetch .ovpn", log_hook)
    return None

def download_ovpn_files(ip_map, log_hook=None):
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    log(f"[*] Complete IP map found {ip_map}.", log_hook)

    for region, ip_list in ip_map.items():
        if not ip_list:
            log(f"[!] No IPs found for {region}. Skipping.", log_hook)
            continue

        for i, ip in enumerate(ip_list):
            filename = f"{region}-{i}.ovpn"
            dest_path = os.path.join(CONFIG_DIR, filename)
            log(f"[*] Waiting for /root/client.ovpn from {region} [{ip}]", log_hook)

            ovpn_content = wait_for_ovpn(ip, log_hook=log_hook)
            if ovpn_content:
                filtered_lines = [
                    line for line in ovpn_content.splitlines()
                    if not (
                        "setenv opt block-outside-dns" in line
                        or
                        "ignore-unknown-option block-outside-dns" in line
                    )
                ]
                with open(dest_path, "w") as f:
                    f.write("\n".join(filtered_lines) + "\n")
                log(f"[✓] Saved: {dest_path}", log_hook)
            else:
                log(f"[✗] Timeout: client.ovpn not available on {ip}", log_hook)