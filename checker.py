""" Script for checking DN42 peers before adding them to production """

import os
import sys
import yaml
import validators
import requests

KNOWN_ROUTER_FILES = ["de1.yml", "se1.yml", "uk1.yml"]

# Check if an ASN exists
def asn_exists(asn):
    r = requests.get(f"https://explorer.burble.com/api/registry/aut-num/AS{asn}", timeout=10)
    return r.status_code == 200

# Validates used keys of a peer config
def validate_peer_config(config):
    if not "name" in config or not config["name"]:
        raise Exception("Missing name")

    if not config["name"].startswith("dn42_"):
        raise Exception("Invalid name")

    if not config["name"].startswith("dn42_"):
        raise Exception("Invalid name")
    try:
        if not "remote" in config or not config["remote"]:
            raise Exception("Missing remote")
    except:
        1
    try:
        remote = config["remote"].partition(":")[0]
        if not validators.domain(remote) or validators.ipv4(remote) or validators.ipv6(remote):
            raise Exception("Invalid remote")
    except: 
        1

    if not "local_v6" in config and not "local_v4" in config:
        raise Exception("Missing one of local_v4, local_v6")

    if "local_v6" in config and not validators.ipv6(config["local_v6"]):
        raise Exception("Invalid local_v6")

    if "local_v4" in config and not validators.ipv4(config["local_v4"]):
        raise Exception("Invalid local_v4")

    if not "peer_v6" in config and not "peer_v4" in config:
        raise Exception("Missing peer_v4 or peer_v6")

    if "peer_v6" in config and not validators.ipv6(config["peer_v6"]):
        raise Exception("Invalid peer_v6")

    if "peer_v4" in config and not validators.ipv4(config["peer_v4"]):
        raise Exception("Invalid peer_v4")

    if "asn" in config and not asn_exists(config["asn"]):
        raise Exception("Invalid asn")

if __name__ == "__main__":
    for file in os.listdir("conf"):
        if file not in KNOWN_ROUTER_FILES:
            print(f"Unknown file '{file}', skipping")
            continue

        print(file)

        with open(f"conf/router/{file}", 'r', encoding="utf-8") as config:
            peers = yaml.safe_load(config)
            for peer in peers["wg_peers"]:
                try:
                    validate_peer_config(peer)
                except Exception as e:
                    print("Peer config validation:", e)
                    sys.exit(1)

    print("Valid configuration")
    sys.exit(0)
