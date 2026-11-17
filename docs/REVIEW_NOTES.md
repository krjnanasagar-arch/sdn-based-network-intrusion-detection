# First Review Notes

## 30-second answer
Our project is an SDN-Based Network Intrusion Detection System. We use Mininet to create a virtual network, Open vSwitch as the switch, and OS-Ken as the SDN controller. The controller monitors TCP and UDP traffic and uses threshold-based detection to identify possible port scans and flooding. If suspicious traffic crosses a threshold, it can install a temporary drop rule.

## Problem
Network attacks such as port scanning and flooding can affect security.

## Approach
Monitor -> Analyze -> Detect -> Block -> Evaluate

## SDN
Software Defined Networking separates control logic from packet forwarding and enables centralized network control.

## Mininet
A network emulator for virtual hosts, switches and links.

## OVS
A software switch supporting OpenFlow.

## OS-Ken
A Python-based SDN controller framework.

## OpenFlow
Protocol used for controller-switch communication.

## IDS
Detects suspicious activity.

## IPS
Detects and can prevent/block suspicious activity.

## Completed
Environment setup, Mininet/OVS installation, project structure, virtual environment and basic connectivity.

## Remaining
Controller verification, controller connection, IDS tests, blocking demonstration and evaluation.

## Team
Member 1: topology/network setup.
Member 2: traffic generation/testing.
Member 3: controller/IDS logic.

Never claim a feature is fully tested unless it has actually been demonstrated.
