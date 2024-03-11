""" Script for checking DN42 peers before adding them to production """

import os
import sys
import yaml
import validators
import requests

KNOWN_ROUTER_FILES = ["de1.yml", "se1.yml", "uk1.yml"]

def asn_exists(asn):
    r = requests.get(f"https://explorer.burble.com/api/registry/aut-num/AS{asn}", timeout=10)
    return r.status_code == 200

def validate_peer_config(config):
    if not config["name"]:
        raise Exception("Missing name")

    if not config["name"].startswith("dn42_"):
        raise Exception("Invalid name")

    if not config["remote"]:
        raise Exception("Missing remote")

    remote = config["remote"].partition(":")[0]
    if not validators.domain(remote) or validators.ipv4(remote) or validators.ipv6(remote):
        raise Exception("Invalid remote")

    if not config["local_v6"] and not config["local_v4"]:
        raise Exception("Missing local_v4 or local_v6")

    if config["local_v6"] and not validators.ipv6(config["local_v6"]):
        raise Exception("Invalid local_v6")

    if config["local_v4"] and not validators.ipv4(config["local_v4"]):
        raise Exception("Invalid local_v4")

    if not config["peer_v6"] and not config["peer_v4"]:
        raise Exception("Missing peer_v4 or peer_v6")

    if config["peer_v6"] and not validators.ipv6(config["remote_v6"]):
        raise Exception("Invalid peer_v6")

    if config["peer_v4"] and not validators.ipv4(config["remote_v4"]):
        raise Exception("Invalid peer_v4")

    if config["asn"] and not asn_exists(config["asn"]):
        raise Exception("Invalid asn")


if __name__ == "__main__":
    for router in os.listdir("conf"):
        if router not in KNOWN_ROUTER_FILES:
            print(f"'{file}' is not a legal file, skipping")
            continue

        print(router)

        with open("conf/"+ router, 'r', encoding="utf-8") as file:
            peers = yaml.safe_load(file)
            for peer in peers["wg_peers"]:
                try:
                    validate_peer_config(peer)
                except Exception as e:
                    print("Peer config validation:", e)
                    sys.exit(1)

    print("Valid configuration")
    sys.exit(0)