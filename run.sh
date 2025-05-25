#!/bin/bash

# Ensure you're in the root of the repo
cd "$(dirname "$0")"

# Optional: activate your venv
source venv/bin/activate

# Run the GUI with sudo
sudo python3 orchestrator/cloakvpn_gui.py