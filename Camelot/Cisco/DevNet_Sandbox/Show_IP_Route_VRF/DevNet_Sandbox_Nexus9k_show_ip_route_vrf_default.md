
# Show IP Route
| VRF | Address Family | Route | Active | Metric | Route Preference | Source Protocol | M Best | U Best | Next Hop Index | Next Hop | Best Unicast Nexthop | Metric | Route Preference | Source Protocol | Updated |
| --- | -------------- | ----- | ------ | ------ | ---------------- | --------------- | ------ | ------ | -------------- | -------- | -------------------- | ------ | ---------------- | --------------- | ------- |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 0 | 2 | 1 | 172.16.0.1 | True | 0 | 0 | direct | 01:42:10 |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 0 | 2 | 2 | 172.16.0.1 | True | 0 | 0 | local | 01:42:10 |
| default | ipv4 | 172.16.1.0/30 | True | 0 | 0 | direct | 0 | 1 | 1 | 172.16.1.1 | True | 0 | 0 | direct | 01:41:13 |
| default | ipv4 | 172.16.1.1/32 | True | 0 | 0 | local | 0 | 1 | 1 | 172.16.1.1 | True | 0 | 0 | local | 01:41:13 |