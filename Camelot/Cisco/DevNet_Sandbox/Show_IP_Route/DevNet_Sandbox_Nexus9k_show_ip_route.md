
# Show IP Route
| VRF | Address Family | Route | Active | Metric | Route Preference | Source Protocol | M Best | U Best | Next Hop Index | Next Hop | Best Unicast Nexthop | Metric | Route Preference | Source Protocol | Updated |
| --- | -------------- | ----- | ------ | ------ | ---------------- | --------------- | ------ | ------ | -------------- | -------- | -------------------- | ------ | ---------------- | --------------- | ------- |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 0 | 2 | 1 | 172.16.0.1 | True | 0 | 0 | local | 04:30:45 |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 0 | 2 | 2 | 172.16.0.1 | True | 0 | 0 | direct | 04:30:45 |
| default | ipv4 | 172.16.1.0/30 | True | 0 | 0 | direct | 0 | 1 | 1 | 172.16.1.1 | True | 0 | 0 | direct | 04:29:47 |
| default | ipv4 | 172.16.1.1/32 | True | 0 | 0 | local | 0 | 1 | 1 | 172.16.1.1 | True | 0 | 0 | local | 04:29:47 |
| management | ipv4 | 0.0.0.0/0 | True | 0 | 1 | static | 0 | 1 | 1 | 10.10.20.254 | True | 0 | 1 | static | 04:30:45 |
| management | ipv4 | 10.10.20.0/24 | True | 0 | 0 | direct | 0 | 1 | 1 | 10.10.20.58 | True | 0 | 0 | direct | 04:30:45 |
| management | ipv4 | 10.10.20.58/32 | True | 0 | 0 | local | 0 | 1 | 1 | 10.10.20.58 | True | 0 | 0 | local | 04:30:45 |