import csv
import os
import requests

from mav import *

with open('owners_networks_pools.csv', 'r') as read_obj: 
    # 'owners_networks_pools.csv' is a csv with 3 columns: 
    # 1. owner (address of the LP user), 
    # 2. network (at the moment "mainnet" and "zksync" are supported)
    # 3. pool (0x address of the pool)
    csv_reader = csv.reader(read_obj) 
    owners_networks_pools = list(csv_reader) 

for line in owners_networks_pools[1:]: # Remove the title line
    owner = HexBytes(line[0])
    network = line[1]
    pool = HexBytes(line[2])
    position_inspector_contract = PositionInspectorContract(network)
    out_of_range = position_inspector_contract.is_out_of_range(owner, pool)
    pool_information_contract = PoolInformationContract(network)
    pool_information_contract.get_price(pool, network)
    pool_information_contract.get_active_tick_start_and_end_price(pool, network)

    if out_of_range:
        data = {
            "content": f"Owner {owner.hex()} is out of range on pool {pool.hex()}",
            "username": "Custom Notification Bot"
        }

        # POST request to the Discord webhook
        response = requests.post(webhook_url, json=data)

        # Check the response
        if response.status_code == 204:
            logging.info(f"Notification sent successfully! Owner {owner.hex()} is out of range on pool {pool.hex()}")
        else:
            logging.error(f"Failed to send notification for owner {owner.hex()} on pool {pool.hex()}. Status code: {response.status_code}")
