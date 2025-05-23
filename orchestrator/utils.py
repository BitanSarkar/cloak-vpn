import os, sys, subprocess, json, re
from datetime import datetime
from constants import LOG_FILE, REGIONS_FILE, VPN_CONFIG_DIR

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[+] {msg}")

def require_sudo():
    if os.geteuid() != 0:
        print("[!] This script must be run with sudo/root privileges.")
        sys.exit(1)

def get_network_services():
    result = subprocess.run(["networksetup", "-listallnetworkservices"], capture_output=True, text=True)
    services = result.stdout.strip().splitlines()
    return [s.strip("*").strip() for s in services if not s.startswith("*")]

def disable_ipv6_mac():
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6off", service])
        log(f"IPv6 disabled for: {service}")

def enable_ipv6_mac():
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6automatic", service])
        log(f"IPv6 re-enabled for: {service}")

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

def load_regions():
    with open(REGIONS_FILE, "r") as f:
        return json.load(f)

def kill_process(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

def connect_openvpn(config_path):
    log(f"Connecting OpenVPN: {os.path.basename(config_path)}")
    return subprocess.Popen(["openvpn", "--config", config_path])

def collect_ovpn_paths():
    return [os.path.join(VPN_CONFIG_DIR, f) for f in os.listdir(VPN_CONFIG_DIR) if f.endswith(".ovpn")]

def extract_ip_from_ovpn(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    match = re.search(r"remote (.*?) (\d+)", content)
    return match.group(1) if match else None

def ping_ip(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        output = result.stdout
        match = re.search(r"time=([\d.]+) ms", output)
        return float(match.group(1)) if match else None
    except Exception as e:
        log(f"Ping failed for {ip}: {e}")
        return None

def ping_ips_from_ovpn_files():
    """
    Scans all .ovpn files in VPN_CONFIG_DIR, extracts IPs, pings them, returns:
    {
        "us-east-1": [("us-east-1-0.ovpn", 32.1), ("us-east-1-1.ovpn", 28.9)],
        ...
    }
    """
    region_map = {}
    for f in os.listdir(VPN_CONFIG_DIR):
        if not f.endswith(".ovpn"):
            continue
        path = os.path.join(VPN_CONFIG_DIR, f)
        ip = extract_ip_from_ovpn(path)
        if not ip:
            continue
        latency = ping_ip(ip)
        if latency is not None:
            region = f.split("-")[0]
            region_map.setdefault(region, []).append((f, latency))

    # Sort files by latency within each region
    for region in region_map:
        region_map[region].sort(key=lambda tup: tup[1])

    return region_map
