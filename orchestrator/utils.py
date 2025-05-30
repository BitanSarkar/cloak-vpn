import os, sys, subprocess, json, re, threading
from ping3 import ping, verbose_ping
from datetime import datetime
from constants import LOG_FILE, REGIONS_FILE, VPN_CONFIG_DIR

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def clean_log(text):
    return re.sub(r"\[\d+[\=\+\-]", "", ANSI_ESCAPE.sub('', text))

def log(msg, log_hook = None):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[+] {msg}")
    if log_hook is not None:
        log_hook(clean_log(f"[+] {msg}"))

def require_sudo():
    if os.geteuid() != 0:
        print("[!] This script must be run with sudo/root privileges.")
        sys.exit(1)

def require_sudo_ui():
    return os.geteuid() == 0

def get_network_services():
    result = subprocess.run(["networksetup", "-listallnetworkservices"], capture_output=True, text=True)
    services = result.stdout.strip().splitlines()
    return [s.strip("*").strip() for s in services if not s.startswith("*")]

def disable_ipv6_mac(log_hook=None):
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6off", service])
        log(f"IPv6 disabled for: {service}", log_hook)

def enable_ipv6_mac(log_hook=None):
    for service in get_network_services():
        subprocess.run(["networksetup", "-setv6automatic", service])
        log(f"IPv6 re-enabled for: {service}", log_hook)

def disable_ipv6(log_hook=None):
    log("Disabling IPv6", log_hook)
    if sys.platform == "darwin":
        disable_ipv6_mac(log_hook)
    elif sys.platform.startswith("linux"):
        subprocess.run("sysctl -w net.ipv6.conf.all.disable_ipv6=1", shell=True)
        subprocess.run("sysctl -w net.ipv6.conf.default.disable_ipv6=1", shell=True)

def enable_ipv6(log_hook=None):
    log("Enabling IPv6", log_hook)
    if sys.platform == "darwin":
        enable_ipv6_mac(log_hook)
    elif sys.platform.startswith("linux"):
        subprocess.run("sysctl -w net.ipv6.conf.all.disable_ipv6=0", shell=True)
        subprocess.run("sysctl -w net.ipv6.conf.default.disable_ipv6=0", shell=True)

def load_regions():
    with open(REGIONS_FILE, "r") as f:
        return json.load(f)

def kill_process(proc, log_hook=None):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

def connect_openvpn(config_path, log_hook=None):
    log(f"Connecting OpenVPN: {os.path.basename(config_path)}", log_hook)
    process = subprocess.Popen(
        ["openvpn", "--config", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    def stream_logs():
        for line in process.stdout:
            log(line.rstrip(), log_hook)

    log_thread = threading.Thread(target=stream_logs, daemon=True)
    log_thread.start()

    return process

def collect_ovpn_paths():
    return [os.path.join(VPN_CONFIG_DIR, f) for f in os.listdir(VPN_CONFIG_DIR) if f.endswith(".ovpn")]

def extract_ip_from_ovpn(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith("remote"):
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
    return None

def ping_ip(ip, count=5, timeout=2, log_hook=None):
    log(f"[ping_ip] Pinging {ip} with {count} packets using ping3...", log_hook)
    latencies = []

    for i in range(count):
        try:
            latency = ping(ip, timeout=timeout, unit='ms')
            if latency is not None:
                latencies.append(latency)
                log(f"[ping_ip] Ping {i+1}/{count}: {latency:.2f} ms", log_hook)
            else:
                log(f"[ping_ip] Ping {i+1}/{count}: Timeout")
        except Exception as e:
            log(f"[ping_ip] Ping {i+1}/{count}: Error - {e}")

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        log(f"[ping_ip] Average latency to {ip}: {avg_latency:.2f} ms")
        return avg_latency
    else:
        log(f"[ping_ip] All pings to {ip} failed or timed out.")
        return None

def ping_ips_from_ovpn_files(log_hook=None):
    region_map = {}
    if not os.path.isdir(VPN_CONFIG_DIR):
        log(f"[ping_ips_from_ovpn_files] VPN_CONFIG_DIR does not exist: {VPN_CONFIG_DIR}", log_hook)
        return region_map

    all_files = os.listdir(VPN_CONFIG_DIR)
    log(f"[ping_ips_from_ovpn_files] Found files: {all_files}", log_hook)

    for f in all_files:
        if not f.endswith(".ovpn"):
            continue
        path = os.path.join(VPN_CONFIG_DIR, f)
        ip = extract_ip_from_ovpn(path)
        log(f"[ping_ips_from_ovpn_files] Extracted IP from {f}: {ip}", log_hook)
        if not ip:
            continue
        latency = ping_ip(ip, log_hook=log_hook)
        if latency is not None:
            region = f.split(".")[0]
            log(f"[ping_ips_from_ovpn_files] {f} latency: {latency} ms", log_hook)
            region_map.setdefault(region, []).append((f, latency))
        else:
            log(f"[ping_ips_from_ovpn_files] Failed to get latency for {ip} in {f}", log_hook)

    for region in region_map:
        region_map[region].sort(key=lambda tup: tup[1])

    log(f"[ping_ips_from_ovpn_files] Final region map: {region_map}", log_hook)
    return region_map