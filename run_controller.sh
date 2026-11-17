#!/bin/bash
cd "$(dirname "$0")"
source controller/venv/bin/activate
exec osken-manager controller/sdn_ids_controller.py --ofp-tcp-listen-port 6653
