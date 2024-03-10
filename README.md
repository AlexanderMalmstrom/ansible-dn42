
# ansible-dn42
This repository is currently used for creating new peers for AS4242421525.

Currently you can only create ipv6 multiprotocol sessions, please contact me on IRC if you need something else.  
First select what node(s) you want to peer with in the `conf/` directory. (se1.alemal.se, de1.alemal.se, uk1.alemal.se)  
Then just add your info in a new block, like below.  
The name needs to start with `dn42_` and it should be followed with your `as-name`.  
The port should be the 5 + the last 4 digits of your ASN.  
local_v6 should always be  fe80::1525, if not please provide justification as to why in the pull request.   
description is fine to omit, but it might help me in the future, so please provide something meaningful for example, a link to you website.  
  
Example for an IPv6 multiprotocol sessions using link local IPs.  
 
```yaml
- name: dn42_AleMal
  remote: "se1.alemal.se:36258"
  port: "51525"
  wg_pubkey: "Bg91m2vr46p8oqCqB4j5JQwRoYyb/rwR3iy5X0hany4="
  peer_v6: "fe80::2189:e9"
  local_v6: "fe80::1525"
  asn: 4242421525
  description: "https://dn42.alemal.se"
```
