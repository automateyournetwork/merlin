
# Learn Routing
| VRF | Address Family | Route | Active | Metric | Next Hop Index | Next Hop | Outgoing Interface | Route Preference | Source Protocol | Source Protocol Code |
| --- | -------------- | ----- | ------ | ------ | -------------- | -------- | -------------------| ---------------- | --------------- | -------------------- |
| default | ipv4 | 10.10.100.100/32 | True | N/A | N/A | N/A | Loopback100 | N/A | local | L |
| default | ipv4 | 10.10.100.0/24 | True | N/A | N/A | N/A | Loopback100 | N/A | connected | C |
| default | ipv4 | 10.10.20.48/32 | True | N/A | N/A | N/A | GigabitEthernet1 | N/A | local | L |
| default | ipv4 | 10.10.20.0/24 | True | N/A | N/A | N/A | GigabitEthernet1 | N/A | connected | C |