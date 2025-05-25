import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
import requests
from constants import AVAILABLE_REGIONS, REGIONS_FILE, VPN_CONFIG_DIR, REGION_CITY_MAP
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
        self.region_checkboxes = {}
        self.ovpn_ping_map = {}
        self.provisioned = False
        self.choice_label_reverse_map = {v: k for k, v in REGION_CITY_MAP.items()}

        self.vpn_thread = None
        self.vpn_stop_event = threading.Event()

        self.mode_var = tk.StringVar(value="")
        self.interval_var = tk.StringVar(value="")
        self.region_choice_var = tk.StringVar()
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        self.build_left_column(self.main_frame)
        self.build_log_panel(self.main_frame)
        self.set_vpn_config_state("disabled")
        self.destroy_button.config(state="disabled")

    def build_left_column(self, parent):
        self.build_region_selector(parent)
        self.build_provision_controls(parent)
        self.build_vpn_mode_controls(parent)
        self.build_ping_summary(parent)

    def build_region_selector(self, parent):
        self.region_frame = ttk.LabelFrame(parent, text="Select Regions by City")
        self.region_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        canvas = tk.Canvas(self.region_frame, width=550, height= 250)
        self.region_inner = ttk.Frame(canvas)

        self.region_inner.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.region_inner, anchor="nw")
        canvas.grid(row=0, column=0, sticky="nsew")
        columns = 3
        sorted_regions = sorted(REGION_CITY_MAP.items())
        for idx, (region, city) in enumerate(sorted_regions):
            row = idx // columns
            col = idx % columns
            label = f"{city}"
            var = tk.IntVar(value=0)
            chk = ttk.Checkbutton(self.region_inner, text=label, variable=var)
            chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            self.region_vars[region] = var
            self.region_checkboxes[region] = chk

    def build_log_panel(self, parent):
        self.log_frame = ttk.LabelFrame(parent, text="Provisioning Log")
        self.log_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=10, pady=5)

        self.log_output = scrolledtext.ScrolledText(self.log_frame, height=10, state="disabled")
        self.log_output.pack(fill="both", expand=True)

    def build_provision_controls(self, parent):
        # Button frame inside LEFT column only
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")  # ONLY column 0

        # Make left column expand to fit
        parent.columnconfigure(0, weight=1)

        # Add provision & destroy buttons
        self.provision_button = ttk.Button(button_frame, text="Provision + Fetch OVPN", command=self.provision)
        self.provision_button.pack(side="left", expand=True, fill="x", padx=5)

        self.destroy_button = ttk.Button(button_frame, text="Destroy Provision", command=self.destroy_provision, state="disabled")
        self.destroy_button.pack(side="left", expand=True, fill="x", padx=5)
    
    def log_ui(self, message):
        self.log_output.config(state="normal")
        self.log_output.insert("end", f"{message}\n")
        self.log_output.see("end")
        self.log_output.config(state="disabled")

    def build_vpn_mode_controls(self, parent):
        self.mode_frame = ttk.LabelFrame(parent, text="VPN Configuration")
        self.mode_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        ttk.Label(self.mode_frame, text="Mode:").grid(row=0, column=0)
        self.mode_selector = ttk.Combobox(self.mode_frame, textvariable=self.mode_var, values=["full", "partial"], state="disabled")
        self.mode_selector.grid(row=0, column=1)
        self.mode_selector.bind("<<ComboboxSelected>>", self.update_mode_fields)

        ttk.Label(self.mode_frame, text="Interval (s):").grid(row=1, column=0)
        self.interval_entry = ttk.Entry(self.mode_frame, textvariable=self.interval_var, state="normal")
        self.interval_entry.grid(row=1, column=1)

        ttk.Label(self.mode_frame, text="Region (partial only):").grid(row=2, column=0)
        self.region_combo = ttk.Combobox(self.mode_frame, textvariable=self.region_choice_var, state="disabled")
        self.region_combo.grid(row=2, column=1)

        self.start_button = ttk.Button(self.mode_frame, text="Start VPN", command=self.launch_vpn, state="disabled")
        self.stop_button = ttk.Button(self.mode_frame, text="Stop VPN", command=self.stop_vpn_ui, state="disabled")
        # Make the mode_frame use a grid with equal weights
        self.mode_frame.columnconfigure(0, weight=1)
        self.mode_frame.columnconfigure(1, weight=1)

        # Place Start and Stop buttons
        self.start_button.grid(row=3, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.stop_button.grid(row=3, column=1, padx=(5, 10), pady=10, sticky="ew")
 
    def build_ping_summary(self, parent):
        self.ping_frame = ttk.LabelFrame(parent, text="Ping Summary")
        self.ping_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.ping_table = ttk.Treeview(self.ping_frame, columns=("region", "best"), show="headings", height=10)
        self.ping_table.heading("region", text="Region")
        self.ping_table.heading("best", text="Best Ping (ms)")
        self.ping_table.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(self.ping_frame, orient="vertical", command=self.ping_table.yview)
        self.ping_table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

    def set_vpn_config_state(self, state="disabled"):
        self.region_combo.config(state="disabled" if self.mode_var.get() == "partial" and state == "normal" else state)
        self.interval_entry.config(state=state)
        self.start_button.config(state=state)
        self.stop_button.config(state="disabled")
        self.destroy_button.config(state="disabled")
        self.mode_selector.config(state=state)

    def update_mode_fields(self, event):
        if self.mode_var.get() == "partial":
            self.region_combo.config(state="normal")
            self.interval_entry.config(state="readonly")
        elif self.mode_var.get() == "full":
            self.region_combo.config(state="disabled")
            self.interval_entry.config(state="normal")
        else:
            self.region_combo.config(state="disabled")
            self.interval_entry.config(state="disabled")

    def destroy_provision(self):
        confirm = messagebox.askyesno("Confirm", "This will destroy all infrastructure and delete OVPN configs. Proceed?")
        if not confirm:
            return
        self.log_ui("🧨 Destroying infrastructure...")
        self.destroy_button.config(state="disabled")
        self.set_region_selector_state("normal")
        self.set_vpn_config_state("disabled")
        def task():
            try:
                from provisioner import run_terraform_destroy
                run_terraform_destroy(log_hook=self.log_ui)
                self.log_ui("🗑️ Deleting OVPN files...")
                for file in VPN_CONFIG_DIR.iterdir():
                    if file.name != ".gitkeep":
                        file.unlink()
                self.ovpn_ping_map.clear()
                self.update_ping_table()
                self.region_combo.config(values=[])
                messagebox.showinfo("Cleanup", "Infrastructure destroyed and configs deleted.")
            except Exception as e:
                self.log_ui(f"[ERROR] Failed to destroy provision: {e}")
                messagebox.showerror("Error", f"Failed: {e}")

        threading.Thread(target=task, daemon=True).start()


    def get_public_ip(self):
        try:
            ip = requests.get("https://api.ipify.org").text.strip()
            return ip
        except Exception as e:
            print(f"[ERROR] Could not fetch public IP: {e}")
            return None
    
    def set_region_selector_state(self, state="normal"):
        for chk in self.region_checkboxes.values():
            chk.config(state=state)
            
    def provision(self):
        selected = {r: 1 for r, v in self.region_vars.items() if v.get() > 0}
        if not selected:
            messagebox.showerror("Input Error", "Please select at least one region.")
            return
        self.set_region_selector_state("disabled")
        self.provision_button.config(state="disabled")
        def task():
            region_payload = {
                "regions": {
                    r: {"count": c} for r, c in selected.items()
                },
                "my_public_ip": self.get_public_ip() + "/32"
            }
            with open(REGIONS_FILE, "w") as f:
                json.dump(region_payload, f, indent=2)

            if VPN_CONFIG_DIR.exists():
                for file in VPN_CONFIG_DIR.iterdir():
                    if file.name != ".gitkeep":
                        file.unlink()
            else:
                VPN_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            self.log_ui("🛠 Running Terraform...")
            startup(log_hook=self.log_ui)

            self.log_ui("📶 Running ping tests...")
            self.ovpn_ping_map = ping_ips_from_ovpn_files(log_hook=self.log_ui)

            self.log_ui("✅ Provisioning completed.")
            self.log_ui(f"[DEBUG] Fetched OVPN Ping Map: {self.ovpn_ping_map}")
            labels = [
                REGION_CITY_MAP.get(region[:-2], region[:-2])
                for region in self.ovpn_ping_map.keys()
            ]
            log(f"Reverse labels: {labels}", self.log_ui)
            self.region_combo.config(values=labels)
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.update_ping_table()
            self.mode_var.set("full")
            self.interval_var.set("120")
            self.set_vpn_config_state("normal")
            messagebox.showinfo("Success", "Provisioning complete.")

        threading.Thread(target=task, daemon=True).start()

    def update_ping_table(self):
        for row in self.ping_table.get_children():
            self.ping_table.delete(row)
        for region, items in self.ovpn_ping_map.items():
            best = items[0][1] if items else "-"
            self.ping_table.insert("", "end", values=(REGION_CITY_MAP[region[:-2]], best))

    def launch_vpn(self):
        mode = self.mode_var.get()
        interval = int(self.interval_var.get())
        all_ovpns = []
        self.log_ui("[DEBUG] Launching VPN with the following OVPN map:")
        for region, files in self.ovpn_ping_map.items():
            self.log_ui(f"  {region}: {[f[0] for f in files]}")
            all_ovpns.extend([os.path.join(VPN_CONFIG_DIR, f[0]) for f in files])

        self.log_ui("[DEBUG] Resolved OVPN file paths:")
        for path in all_ovpns:
            self.log_ui(f"  {path} - Exists: {os.path.exists(path)}")

        # Kill any previous thread/process
        if self.vpn_thread and self.vpn_thread.is_alive():
            self.log_ui("[DEBUG] Stopping previous VPN thread...")
            self.vpn_stop_event.set()
            self.vpn_thread.join()

        # Start new one
        self.vpn_stop_event = threading.Event()
        self.start_button.config(state="disabled")
        self.destroy_button.config(state="disabled")
        self.stop_button.config(state="normal")
        if mode == "partial":
            label = self.region_choice_var.get()
            region = self.choice_label_reverse_map.get(label)
            self.vpn_thread = threading.Thread(
                target=run_mode_partial,
                args=(region, all_ovpns, self.vpn_stop_event, self.log_ui),
                daemon=True
            )
        else:
            self.vpn_thread = threading.Thread(
                target=run_mode_full,
                args=(all_ovpns, interval, self.vpn_stop_event, self.log_ui),
                daemon=True
            )

        self.vpn_thread.start()
        messagebox.showinfo("Started", f"VPN started in {mode} mode")

    def stop_vpn_ui(self):
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.destroy_button.config(state="normal")
        if self.vpn_thread and self.vpn_thread.is_alive():
            self.log_ui("[DEBUG] Stopping VPN thread...")
            self.vpn_stop_event.set()
            self.vpn_thread.join()
        stop_vpn(log_hook=self.log_ui)

    def handle_exit(self):
        self.stop_vpn_ui()
        cleanup(log_hook=self.log_ui)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CloakVPNGui(root)
    root.mainloop()
