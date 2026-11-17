# SDN-Based Network Intrusion Detection System

## Abstract
This project demonstrates an educational SDN-based network intrusion detection prototype. Mininet emulates the network, Open vSwitch performs forwarding, and OS-Ken provides centralized control. The controller monitors TCP/UDP traffic and uses threshold-based rules for possible port scans and flooding. A temporary source-IP drop rule can be installed when a threshold is crossed.

## Problem Statement
Networks can face port scanning and flooding. We aim to provide centralized monitoring and automatic mitigation using SDN.

## Objectives
- Build a virtual network with Mininet.
- Connect OVS to OS-Ken using OpenFlow 1.3.
- Monitor TCP/UDP traffic.
- Detect suspicious patterns.
- Apply temporary blocking rules.
- Evaluate normal and suspicious traffic.

## Use Case
In a college computer lab, if one host starts contacting many ports or sending unusually high traffic, the SDN controller can identify the abnormal pattern and instruct the switch to block the source temporarily.

## Architecture
Hosts -> Open vSwitch -> OS-Ken Controller

## Technologies
Ubuntu, Python, Mininet, Open vSwitch, OS-Ken, OpenFlow 1.3, TCP/UDP sockets.

## Detection
Port scan: count distinct TCP destination ports from one source in a short window.
TCP SYN burst: count SYN packets from one source.
UDP burst: count UDP packets from one source.

## Mitigation
A high-priority OpenFlow rule matching the source IPv4 address with no actions drops matching packets for a limited time.

## Current status
Basic environment setup, Mininet/OVS installation, project structure, virtual environment and basic topology connectivity have been completed. Controller verification, end-to-end IDS testing and final evaluation must be demonstrated before calling the system fully complete.

## Limitations
This is a threshold-based educational prototype, not a production IDS. Thresholds can cause false positives or false negatives.

## Future Work
Machine-learning detection, dashboard, persistent logging, more attack classes and larger-scale testing.
