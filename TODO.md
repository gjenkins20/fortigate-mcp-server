# TODO

Project tasks and planned work.

---

## New MCP Tools — Network Visibility

- [x] **DHCP Leases**
  - Add tool to retrieve DHCP lease information from FortiGate
  - API endpoint: `monitor/system/dhcp`
  - Show assigned IPs, MAC addresses, hostnames, lease expiry
  - Add to `FortiGateAPI`, `NetworkTools`, and register in both servers

- [x] **ARP Table**
  - Add tool to retrieve ARP table entries
  - API endpoint: `monitor/system/arp`
  - Show active MAC/IP mappings, interfaces, age
  - Add to `FortiGateAPI`, `NetworkTools`, and register in both servers

- [x] **Session Table**
  - Add tool to retrieve active sessions/connections
  - API endpoint: `monitor/firewall/session`
  - Show active connections, source/dest IPs, services, protocols, bytes transferred
  - Consider adding filtering params (by source IP, dest IP, service, policy ID)
  - Add to `FortiGateAPI`, `FirewallTools`, and register in both servers

- [x] **Device Inventory**
  - Add tool to retrieve detected devices (requires device detection enabled on FortiGate)
  - API endpoint: `monitor/user/device/query`
  - Show detected hosts, OS, device type, MAC, IP, interface
  - Add to `FortiGateAPI`, `DeviceTools` or `NetworkTools`, and register in both servers

---

## Multi-FortiGate Support (Low Priority)

- [ ] **Document multi-device workflow**
  - Add examples showing how to configure and query multiple FortiGates
  - Update README with multi-device usage patterns

---

## Completed

- [x] Fix STDIO protocol corruption (print to stdout, await on sync methods)
- [x] Fix missing entry points (__main__.py, pyproject.toml)
- [x] Fix code quality issues (bare excepts, unused imports, duplicate methods)
- [x] Add Claude Desktop integration config and documentation
- [x] Pin MCP SDK dependency
- [x] Fix all linting issues (black, isort, flake8)
- [x] Connect to FortiGate at 192.168.1.99 via Claude Desktop

---

*Last updated: 2026-02-18*
