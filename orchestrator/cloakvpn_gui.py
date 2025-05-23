# cloakvpn_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
import shutil
from constants import AVAILABLE_REGIONS, REGIONS_FILE, VPN_CONFIG_DIR
from provisioner import startup, cleanup
from vpn_connector import run_mode_partial, run_mode_full
from utils import ping_ips_from_ovpn_files, require_sudo, log

class CloakVPNGui:
    def __init__(self, root):
        require_sudo()
        self.root = root
        root.title("CloakVPN Launcher")
        self.root.protocol("WM_DELETE_WINDOW", cleanup)

        self.region_vars = {}
        self.mode_var = tk.StringVar(value="full")
        self.interval_var = tk.StringVar(value="60")
        self.region_choice_var = tk.StringVar()
        self.ovpn_ping_map = {}

        self.build_region_select_ui()
        self.build_provision_button()
        self.build_mode_controls()

    def build_region_select_ui(self):
        ttk.Label(self.root, text="Select Regions and Counts:").grid(row=0, column=0, sticky="w")
        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="w")
        for i, region in enumerate(AVAILABLE_REGIONS):
            ttk.Label(frame, text=region).grid(row=i, column=0, sticky="w")
            var = tk.IntVar(value=0)
            entry = ttk.Entry(frame, textvariable=var, width=5)
            entry.grid(row=i, column=1, sticky="w")
            self.region_vars[region] = var

    def build_provision_button(self):
        ttk.Button(self.root, text="1. Provision VPN Infrastructure", command=self.provision).grid(row=2, column=0, pady=10)

    def build_mode_controls(self):
        frame = ttk.LabelFrame(self.root, text="2. VPN Cloaking Mode")
        frame.grid(row=3, column=0, sticky="we", padx=5, pady=5)

        # Mode
        ttk.Label(frame, text="Mode:").grid(row=0, column=0)
        mode_cb = ttk.Combobox(frame, textvariable=self.mode_var, values=["full", "partial"], state="readonly")
        mode_cb.grid(row=0, column=1)
        mode_cb.bind("<<ComboboxSelected>>", self.update_region_select_visibility)

        # Interval
        ttk.Label(frame, text="Interval (s):").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.interval_var).grid(row=1, column=1)

        # Region choice for partial
        ttk.Label(frame, text="Fixed Region:").grid(row=2, column=0)
        self.region_combo = ttk.Combobox(frame, textvariable=self.region_choice_var, state="disabled")
        self.region_combo.grid(row=2, column=1)

        ttk.Button(frame, text="3. Start VPN", command=self.launch_vpn).grid(row=3, column=0, columnspan=2, pady=10)

    def update_region_select_visibility(self, event):
        if self.mode_var.get() == "partial":
            self.region_combo.config(state="readonly")
        else:
            self.region_combo.config(state="disabled")

    def provision(self):
        selected = {r: var.get() for r, var in self.region_vars.items() if var.get() > 0}
        if not selected:
            messagebox.showerror("Error", "Please select at least one region with count > 0")
            return
        region_data = {
            "regions": {
                r: {"count": c} for r, c in selected.items()
            }
        }
        with open(REGIONS_FILE, "w") as f:
            json.dump(region_data, f, indent=2)

        if VPN_CONFIG_DIR.exists():
            shutil.rmtree(VPN_CONFIG_DIR)
            gitkeep_path = VPN_CONFIG_DIR / ".gitkeep"
            gitkeep_path.touch(exist_ok=True)
        else:
            VPN_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        def background():
            startup()
            self.ovpn_ping_map = ping_ips_from_ovpn_files()
            self.region_combo.config(values=list(self.ovpn_ping_map.keys()))
            messagebox.showinfo("Done", "Provisioning and .ovpn download complete")

        threading.Thread(target=background, daemon=True).start()
        messagebox.showinfo("Started", "Terraform provisioning started")

    def launch_vpn(self):
        mode = self.mode_var.get()
        interval = int(self.interval_var.get())

        ovpn_paths = []
        log(f"ovpn ping map: {self.ovpn_ping_map}")
        log(f"ovpn files got: {files}")
        for region, files in self.ovpn_ping_map.items():
            ovpn_paths.extend([os.path.join(VPN_CONFIG_DIR, f[0]) for f in files])

        if mode == "partial":
            region = self.region_choice_var.get()
            if not region or region not in self.ovpn_ping_map:
                messagebox.showerror("Error", "Invalid region selected for partial mode")
                return
            threading.Thread(target=run_mode_partial, args=(region, ovpn_paths), daemon=True).start()
        else:
            threading.Thread(target=run_mode_full, args=(ovpn_paths, interval), daemon=True).start()

        messagebox.showinfo("Launched", f"VPN started in {mode} mode")

if __name__ == "__main__":
    root = tk.Tk()
    app = CloakVPNGui(root)
    root.mainloop()
