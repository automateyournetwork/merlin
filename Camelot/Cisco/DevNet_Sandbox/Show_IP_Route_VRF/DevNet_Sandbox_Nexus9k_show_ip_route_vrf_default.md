
# Show IP Route (Global Routing Table)
| VRF | Address Family | Route | Active | Metric | Route Preference | Source Protocol | Source Protocol Code | Next Hop Number | Next Hop | Outgoing Interface | Updated |
| --- | -------------- | ----- | ------ | ------ | ---------------- | --------------- | -------------------- | --------------- | -------- | ------------------ | ------- |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct |  | 1 | 172.16.0.1 | Loopback1 | 01:30:07 |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct |  | 2 | 172.16.0.1 | Loopback1 | 01:30:07 |
| default | ipv4 | 172.16.1.0/30 | True | 0 | 0 | direct |  | 1 | 172.16.1.1 | Ethernet1/5 | 01:29:07 |
| default | ipv4 | 172.16.1.1/32 | True | 0 | 0 | local |  | 1 | 172.16.1.1 | Ethernet1/5 | 01:29:07 |