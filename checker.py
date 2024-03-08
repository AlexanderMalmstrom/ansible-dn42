import os
import yaml
import pprint

pp = pprint.PrettyPrinter(indent=4)
legalKeys = ['name', 'remote', 'wg_pubkey', 'peer_v6', 'peer_v4', 'local_v6', 'local_v4', 'asn', 'description', 'port' ]
legalfiles = ['de1.yml', 'se1.yml', 'uk1.yml']

# Get the list of all peers
dir_list = os.listdir("conf")
#print(dir_list)

for file in dir_list:
    if file not in legalfiles:
        print(file, "is not a legal file, please delete it")
        exit(1)

for router in dir_list:
    print(router)

    with open("conf/"+ router, 'r') as file:
        peers = yaml.safe_load(file)
        peers = peers['wg_peers']
        for peer in peers:
            for key, value in peer.items():
                print(key, value)
                if key not in legalKeys:
                    print("Oh nose,", key, "isnt an leagal key")
                    exit(1)
                if(key == "port"):
                    if 50000 <= value <= 59999:
                        print("Port is Valid")
                    else:
                        exit(1)

                
                