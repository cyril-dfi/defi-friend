import requests
from mav import *

# Your webhook URL
webhook_url = 'https://discord.com/api/webhooks/1215240065572282399/scjLgu4683hhSvDFsPSP_yUU21QvleuJ5JRXOY2FHrZ7SMCEKXQ1Uymzm2nlFfmnzMT-'

# Random owner of a position on Maverick Mainnet
owner = HexBytes(0x37Ff9172beCAf3B78284822eD55a03FAB0Bc9E27)
pool = HexBytes(0xd50c68c7fbaee4f469e04cebdcfbf1113b4cdadf)

is_out_of_range = is_out_of_range(owner, pool)

if is_out_of_range:
    data = {
        "content": f"Owner {owner.hex()} is out of range on pool {pool.hex()}",
        "username": "Custom Notification Bot"
    }

    # POST request to the Discord webhook
    response = requests.post(webhook_url, json=data)

    # Check the response
    if response.status_code == 204:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification.")
else:
    # TO REMOVE
    data = {
        "content": f"Owner {owner.hex()} is in of range on pool {pool.hex()}",
        "username": "Custom Notification Bot"
    }

    # POST request to the Discord webhook
    response = requests.post(webhook_url, json=data)

    # Check the response
    if response.status_code == 204:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification.")