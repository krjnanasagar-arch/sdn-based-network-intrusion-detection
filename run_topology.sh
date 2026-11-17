#!/bin/bash
cd "$(dirname "$0")"
sudo mn -c
sudo python3 topology/topology.py
