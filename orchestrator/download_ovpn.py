import os
import json
import subprocess
import time

from pathlib import Path

MAX_WAIT = 180  # seconds
RETRY_INTERVAL = 10  # seconds

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "vpn-configs"))
KEY_PATH = os.path.expanduser("~/.ssh/ghostvpn")

def wait_for_ovpn(ip, retries=MAX_WAIT // RETRY_INTERVAL):
    for attempt in range(retries):
        ssh_cmd = [
            "ssh", "-i", KEY_PATH,
            "-o", "StrictHostKeyChecking=no",
            f"ec2-user@{ip}",
            "sudo cat /root/client.ovpn"
        ]
        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True)
            if result.returncode == 0 and "BEGIN" in result.stdout:
                return result.stdout
        except Exception as e:
            pass

        print(f"[*] Retry {attempt + 1}/{retries}: Waiting for client.ovpn on {ip}")
        time.sleep(RETRY_INTERVAL)
    return None


def download_ovpn_files(ip_map):
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    print(f"[*] Complete IP map found {ip_map}.")

    for region, ip_list in ip_map.items():
        if not ip_list:
            print(f"[!] No IPs found for {region}. Skipping.")
            continue

        for i, ip in enumerate(ip_list):
            filename = f"{region}-{i}.ovpn"
            dest_path = os.path.join(CONFIG_DIR, filename)
            print(f"[*] Waiting for /root/client.ovpn from {region} [{ip}]")

            ovpn_content = wait_for_ovpn(ip)
            print(f"")
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
                print(f"[✓] Saved: {dest_path}")
            else:
                print(f"[✗] Timeout: client.ovpn not available on {ip}")