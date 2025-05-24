import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from constants import AVAILABLE_REGIONS, REGIONS_FILE, VPN_CONFIG_DIR
from provisioner import startup, cleanup
from vpn_connector import run_mode_partial, run_mode_full, stop_vpn
from utils import ping_ips_from_ovpn_files, require_sudo_ui, log

class CloakVPNGui:
    def __init__(self, root):
        self.root = root
        root.title("CloakVPN Launcher")

        # Ensure we are running with sudo/root privileges
        if not require_sudo_ui():
            messagebox.showerror("Permission Denied", "This app must be run with sudo/root privileges.")
            root.destroy()
            return

        self.root.protocol("WM_DELETE_WINDOW", self.handle_exit)

        self.region_vars = {}
        self.ovpn_ping_map = {}
        self.provisioned = False

        self.vpn_thread = None
        self.vpn_stop_event = threading.Event()

        self.mode_var = tk.StringVar(value="full")
        self.interval_var = tk.StringVar(value="60")
        self.region_choice_var = tk.StringVar()

        self.build_region_selector()
        self.build_provision_controls()
        self.build_vpn_mode_controls()
        self.build_ping_summary()

    def build_region_selector(self):
        self.region_frame = ttk.LabelFrame(self.root, text="Region Selection")
        self.region_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        canvas = tk.Canvas(self.region_frame)
        scrollbar = ttk.Scrollbar(self.region_frame, orient="vertical", command=canvas.yview)
        self.region_inner = ttk.Frame(canvas)

        self.region_inner.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.region_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=200)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for i, region in enumerate(AVAILABLE_REGIONS):
            ttk.Label(self.region_inner, text=region).grid(row=i, column=0, sticky="w")
            var = tk.IntVar(value=0)
            ttk.Spinbox(self.region_inner, from_=0, to=10, width=5, textvariable=var).grid(row=i, column=1)
            self.region_vars[region] = var

    def build_provision_controls(self):
        self.provision_button = ttk.Button(self.root, text="Provision + Fetch OVPN", command=self.provision)
        self.provision_button.grid(row=1, column=0, pady=10)

    def build_vpn_mode_controls(self):
        self.mode_frame = ttk.LabelFrame(self.root, text="VPN Configuration")
        self.mode_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        ttk.Label(self.mode_frame, text="Mode:").grid(row=0, column=0)
        mode_cb = ttk.Combobox(self.mode_frame, textvariable=self.mode_var, values=["full", "partial"], state="readonly")
        mode_cb.grid(row=0, column=1)
        mode_cb.bind("<<ComboboxSelected>>", self.update_mode_fields)

        ttk.Label(self.mode_frame, text="Interval (s):").grid(row=1, column=0)
        self.interval_entry = ttk.Entry(self.mode_frame, textvariable=self.interval_var)
        self.interval_entry.grid(row=1, column=1)

        ttk.Label(self.mode_frame, text="Region (partial only):").grid(row=2, column=0)
        self.region_combo = ttk.Combobox(self.mode_frame, textvariable=self.region_choice_var, state="disabled")
        self.region_combo.grid(row=2, column=1)

        self.start_button = ttk.Button(self.mode_frame, text="Start VPN", command=self.launch_vpn, state="disabled")
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.stop_button = ttk.Button(self.mode_frame, text="Stop VPN", command=self.stop_vpn, state="normal")
        self.stop_button.grid(row=4, column=0, columnspan=2, pady=5)

    def build_ping_summary(self):
        self.ping_frame = ttk.LabelFrame(self.root, text="Ping Summary")
        self.ping_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.ping_table = ttk.Treeview(self.ping_frame, columns=("region", "best"), show="headings", height=10)
        self.ping_table.heading("region", text="Region")
        self.ping_table.heading("best", text="Best Ping (ms)")
        self.ping_table.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(self.ping_frame, orient="vertical", command=self.ping_table.yview)
        self.ping_table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

    def update_mode_fields(self, event):
        if self.mode_var.get() == "partial":
            self.region_combo.config(state="readonly")
        else:
            self.region_combo.config(state="disabled")

    def provision(self):
        selected = {r: v.get() for r, v in self.region_vars.items() if v.get() > 0}
        if not selected:
            messagebox.showerror("Input Error", "Please select at least one region.")
            return

        self.provision_button.config(state="disabled")

        def task():
            region_payload = {
                "regions": {
                    r: {"count": c} for r, c in selected.items()
                }
            }
            with open(REGIONS_FILE, "w") as f:
                json.dump(region_payload, f, indent=2)

            if VPN_CONFIG_DIR.exists():
                for file in VPN_CONFIG_DIR.iterdir():
                    if file.name != ".gitkeep":
                        file.unlink()
            else:
                VPN_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            startup()
            self.ovpn_ping_map = ping_ips_from_ovpn_files()
            log(f"[DEBUG] Fetched OVPN Ping Map: {self.ovpn_ping_map}")

            self.region_combo.config(values=list(self.ovpn_ping_map.keys()))
            self.start_button.config(state="normal")
            self.update_ping_table()
            messagebox.showinfo("Success", "Provisioning complete.")

        threading.Thread(target=task, daemon=True).start()

    def update_ping_table(self):
        for row in self.ping_table.get_children():
            self.ping_table.delete(row)
        for region, items in self.ovpn_ping_map.items():
            best = items[0][1] if items else "-"
            self.ping_table.insert("", "end", values=(region, best))

    def launch_vpn(self):
        mode = self.mode_var.get()
        interval = int(self.interval_var.get())
        all_ovpns = []
        log("[DEBUG] Launching VPN with the following OVPN map:")
        for region, files in self.ovpn_ping_map.items():
            log(f"  {region}: {[f[0] for f in files]}")
            all_ovpns.extend([os.path.join(VPN_CONFIG_DIR, f[0]) for f in files])

        log("[DEBUG] Resolved OVPN file paths:")
        for path in all_ovpns:
            log(f"  {path} - Exists: {os.path.exists(path)}")

        # Kill any previous thread/process
        if self.vpn_thread and self.vpn_thread.is_alive():
            log("[DEBUG] Stopping previous VPN thread...")
            self.vpn_stop_event.set()
            self.vpn_thread.join()

        # Start new one
        self.vpn_stop_event = threading.Event()
        if mode == "partial":
            region = self.region_choice_var.get()
            self.vpn_thread = threading.Thread(
                target=run_mode_partial,
                args=(region, all_ovpns, self.vpn_stop_event),
                daemon=True
            )
        else:
            self.vpn_thread = threading.Thread(
                target=run_mode_full,
                args=(all_ovpns, interval, self.vpn_stop_event),
                daemon=True
            )

        self.vpn_thread.start()
        messagebox.showinfo("Started", f"VPN started in {mode} mode")

    def stop_vpn(self):
        if self.vpn_thread and self.vpn_thread.is_alive():
            log("[DEBUG] Stopping VPN thread...")
            self.vpn_stop_event.set()
            self.vpn_thread.join()
        stop_vpn()

    def handle_exit(self):
        self.stop_vpn()
        cleanup()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CloakVPNGui(root)
    root.mainloop()
