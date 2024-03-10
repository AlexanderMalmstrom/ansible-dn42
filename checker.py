""" Script for checking DN42 peers before adding them to production """

import os
import sys
import pprint
import yaml
import validators
import requests

pp = pprint.PrettyPrinter(indent=4)
legalKeys = [
    'name', 'remote',
    'wg_pubkey', 'peer_v6',
    'peer_v4', 'local_v6',
    'local_v4', 'asn',
    'description', 'port' 
    ]
legalfiles = ['de1.yml', 'se1.yml', 'uk1.yml']

# Get the list of all peers
dir_list = os.listdir("conf")
#print(dir_list)

for file in dir_list:
    if file not in legalfiles:
        print(file, "is not a legal file, please delete it")
        sys.exit(1)

for router in dir_list:
    print(router)

    with open("conf/"+ router, 'r', encoding="utf-8") as file:
        peers = yaml.safe_load(file)
        peers = peers['wg_peers']
        for peer in peers:
            for key, value in peer.items():

                if key not in legalKeys:
                    print("Oh nose,", key, "isn't a legal key")
                    sys.exit(1)
                if key == "name":
                    if not value:
                        print("Name cannot be empty")
                        sys.exit(1)

                    if not value.startswith('dn42_'):
                        print('Name should start with the prefix dn42_')
                        sys.exit(1)

                #this should be a IP or an URL, lets test that.
                if key == "remote":
                    value = value.partition(':')[0]
                    if (not validators.domain(value) or
                        validators.ipv4(value) or
                        validators.ipv6(value)):
                        print(value, "is invalid remote, should be domain or IP")
                        sys.exit(1)

                if key in ("peer_v6", "local_v6"):
                    if not validators.ipv6(value):
                        print("Invalid ", key, " this should be IPv6")
                        sys.exit(1)
                if key in ("peer_v4", "local_v4") :
                    if not validators.ipv4(value):
                        print("Invalid ", key, " this should be IPv4")
                        sys.exit(1)

                if key == "asn":
                    r = requests.get(
                        'https://explorer.burble.com/api/registry/aut-num/AS' + str(value), 
                        timeout=10)
                    if r.status_code != 200:
                        print("ASN don't exists")
                        sys.exit(1)


print("all tests looks good")
sys.exit(0)
