# Show IP Access-Lists
| Access Control List | Access Control Entry | Permission | Logging | Source Network | Destination Network | L3 Protocol | L4 Protocol | Operator | Port |
| ------------------- | -------------------- | ---------- | ------- | -------------- | ------------------- | ----------- | ----------- | -------- | ---- |
| preauth_ipv4_acl | 60 | deny | log-none | any | any any | ipv4 | N/A | N/A | N/A |
| preauth_ipv4_acl | 50 | permit | log-none | any | any any | udp | N/A | N/A | N/A |
| preauth_ipv4_acl | 40 | permit | log-none | any | any any | udp | N/A | N/A | N/A |
| preauth_ipv4_acl | 30 | permit | log-none | any | any any | udp | N/A | N/A | N/A |
| preauth_ipv4_acl | 20 | permit | log-none | any | any any | tcp | N/A | N/A | N/A |
| preauth_ipv4_acl | 10 | permit | log-none | any | any any | udp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 460 | permit | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 450 | deny | log-none | 10.25.48.0 0.0.15.255 | any any | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 440 | deny | log-none | any | 10.25.128.0 0.0.0.127 10.25.128.0 0.0.0.127 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 430 | deny | log-none | any | 10.24.143.176 0.0.0.15 10.24.143.176 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 420 | deny | log-none | any | 10.24.243.48 0.0.0.15 10.24.243.48 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 410 | deny | log-none | any | 10.24.243.32 0.0.0.15 10.24.243.32 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 400 | deny | log-none | any | 10.67.250.80 0.0.0.15 10.67.250.80 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 390 | deny | log-none | any | 10.67.250.64 0.0.0.15 10.67.250.64 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 380 | deny | log-none | any | 10.25.240.224 0.0.0.31 10.25.240.224 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 370 | deny | log-none | any | 10.25.240.192 0.0.0.31 10.25.240.192 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 360 | deny | log-none | any | 10.76.28.0 0.0.0.31 10.76.28.0 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 350 | deny | log-none | any | 10.1.50.64 0.0.0.31 10.1.50.64 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 340 | deny | log-none | any | 10.0.247.192 0.0.0.31 10.0.247.192 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 330 | deny | log-none | any | 10.113.72.0 0.0.7.255 10.113.72.0 0.0.7.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 320 | deny | log-none | any | 10.112.72.0 0.0.7.255 10.112.72.0 0.0.7.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 310 | deny | log-none | any | 10.24.41.192 0.0.0.63 10.24.41.192 0.0.0.63 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 300 | deny | log-none | any | 10.111.72.0 0.0.7.255 10.111.72.0 0.0.7.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 290 | deny | log-none | any | 10.25.48.0 0.0.15.255 10.25.48.0 0.0.15.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 280 | deny | log-none | any | 10.24.48.0 0.0.15.255 10.24.48.0 0.0.15.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 270 | deny | log-none | any | 10.78.70.16 0.0.0.7 10.78.70.16 0.0.0.7 | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 260 | deny | log-none | 10.78.70.16 0.0.0.7 | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 250 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 240 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 230 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 220 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 210 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 200 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 190 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 180 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 170 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 160 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 150 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 140 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 130 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 120 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 110 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 100 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 90 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 80 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 70 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 60 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 50 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 40 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 30 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 20 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_OUT | 10 | deny | log-none | any | any any | udp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 390 | permit | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 380 | deny | log-none | any | 10.25.128.0 0.0.0.127 10.25.128.0 0.0.0.127 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 370 | deny | log-none | any | 10.24.143.176 0.0.0.15 10.24.143.176 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 360 | deny | log-none | any | 10.24.243.48 0.0.0.15 10.24.243.48 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 350 | deny | log-none | any | 10.24.243.32 0.0.0.15 10.24.243.32 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 340 | deny | log-none | any | 10.67.250.80 0.0.0.15 10.67.250.80 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 330 | deny | log-none | any | 10.67.250.64 0.0.0.15 10.67.250.64 0.0.0.15 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 320 | deny | log-none | any | 10.25.240.224 0.0.0.31 10.25.240.224 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 310 | deny | log-none | any | 10.25.240.192 0.0.0.31 10.25.240.192 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 300 | deny | log-none | any | 10.24.41.192 0.0.0.31 10.24.41.192 0.0.0.31 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 290 | deny | log-none | any | 10.111.72.0 0.0.7.255 10.111.72.0 0.0.7.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 280 | deny | log-none | any | 10.25.48.0 0.0.15.255 10.25.48.0 0.0.15.255 | ipv4 | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 270 | deny | log-none | any | 10.78.70.16 0.0.0.7 10.78.70.16 0.0.0.7 | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 260 | deny | log-none | 10.78.70.16 0.0.0.7 | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 250 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 240 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 230 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 220 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 210 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 200 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 190 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 180 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 170 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 160 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 150 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 140 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 130 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 120 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 110 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 100 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 90 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 80 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 70 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 60 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 50 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 40 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 30 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 20 | deny | log-none | any | any any | tcp | N/A | N/A | N/A |
| WANOPT_POLICY_ROUTING_IN | 10 | deny | log-none | any | any any | udp | N/A | N/A | N/A |
| preauth_ipv6_acl | 90 | permit | log-none | Source Protocol | N/A | N/A | UDP | 
eq | 546|
| preauth_ipv6_acl | 80 | permit | log-none | Source Protocol | N/A | N/A | UDP | 
eq | 547|
  | preauth_ipv6_acl | 20 | permit | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 53 |
  | preauth_ipv6_acl | 10 | permit | log-none | N/A,Destination Protocol | N/A | UDP | 
eq | 53 |
| preauth_ipv4_acl | 50 | permit | log-none | Source Protocol | N/A | N/A | UDP | 
eq | bootpc|
  | preauth_ipv4_acl | 40 | permit | log-none | N/A,Destination Protocol | N/A | UDP | 
eq | 68 |
| preauth_ipv4_acl | 30 | permit | log-none | Source Protocol | N/A | N/A | UDP | 
eq | bootps|
  | preauth_ipv4_acl | 20 | permit | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 53 |
  | preauth_ipv4_acl | 10 | permit | log-none | N/A,Destination Protocol | N/A | UDP | 
eq | 53 |
| WANOPT_POLICY_ROUTING_OUT | 250 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 8081|  | WANOPT_POLICY_ROUTING_OUT | 240 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 8081 |
| WANOPT_POLICY_ROUTING_OUT | 230 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 1494|  | WANOPT_POLICY_ROUTING_OUT | 220 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 1494 |
| WANOPT_POLICY_ROUTING_OUT | 210 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 2598|  | WANOPT_POLICY_ROUTING_OUT | 200 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 2598 |
| WANOPT_POLICY_ROUTING_OUT | 190 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | smtp|  | WANOPT_POLICY_ROUTING_OUT | 180 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 25 |
| WANOPT_POLICY_ROUTING_OUT | 170 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 444|  | WANOPT_POLICY_ROUTING_OUT | 160 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 444 |
| WANOPT_POLICY_ROUTING_OUT | 150 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 443|  | WANOPT_POLICY_ROUTING_OUT | 140 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 443 |
| WANOPT_POLICY_ROUTING_OUT | 130 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 9999|  | WANOPT_POLICY_ROUTING_OUT | 120 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 9999 |
| WANOPT_POLICY_ROUTING_OUT | 110 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
 N/A | N/A |  | WANOPT_POLICY_ROUTING_OUT | 100 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
range | 1719 |
| WANOPT_POLICY_ROUTING_OUT | 90 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 5070|  | WANOPT_POLICY_ROUTING_OUT | 80 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 5070 |
| WANOPT_POLICY_ROUTING_OUT | 70 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
 N/A | N/A |  | WANOPT_POLICY_ROUTING_OUT | 60 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
range | 5060 |
| WANOPT_POLICY_ROUTING_OUT | 50 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 22|  | WANOPT_POLICY_ROUTING_OUT | 40 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 22 |
| WANOPT_POLICY_ROUTING_OUT | 30 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | telnet|  | WANOPT_POLICY_ROUTING_OUT | 20 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 23 |
| WANOPT_POLICY_ROUTING_IN | 250 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 8081|  | WANOPT_POLICY_ROUTING_IN | 240 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 8081 |
| WANOPT_POLICY_ROUTING_IN | 230 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 1494|  | WANOPT_POLICY_ROUTING_IN | 220 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 1494 |
| WANOPT_POLICY_ROUTING_IN | 210 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 2598|  | WANOPT_POLICY_ROUTING_IN | 200 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 2598 |
| WANOPT_POLICY_ROUTING_IN | 190 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | smtp|  | WANOPT_POLICY_ROUTING_IN | 180 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 25 |
| WANOPT_POLICY_ROUTING_IN | 170 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 444|  | WANOPT_POLICY_ROUTING_IN | 160 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 444 |
| WANOPT_POLICY_ROUTING_IN | 150 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 443|  | WANOPT_POLICY_ROUTING_IN | 140 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 443 |
| WANOPT_POLICY_ROUTING_IN | 130 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 9999|  | WANOPT_POLICY_ROUTING_IN | 120 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 9999 |
| WANOPT_POLICY_ROUTING_IN | 110 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
 N/A | N/A |  | WANOPT_POLICY_ROUTING_IN | 100 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
range | 1719 |
| WANOPT_POLICY_ROUTING_IN | 90 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 5070|  | WANOPT_POLICY_ROUTING_IN | 80 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 5070 |
| WANOPT_POLICY_ROUTING_IN | 70 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
 N/A | N/A |  | WANOPT_POLICY_ROUTING_IN | 60 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
range | 5060 |
| WANOPT_POLICY_ROUTING_IN | 50 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | 22|  | WANOPT_POLICY_ROUTING_IN | 40 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 22 |
| WANOPT_POLICY_ROUTING_IN | 30 | deny | log-none | Source Protocol | N/A | N/A | TCP | 
eq | telnet|  | WANOPT_POLICY_ROUTING_IN | 20 | deny | log-none | N/A | Destination Protocol | N/A | TCP | 
eq | 23 |
