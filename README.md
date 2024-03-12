# DeFi Friend
DeFi Liquidity providooors, DeFi Friend is your friendly bot that helps you make sure that your positions are always in range, by pinging you every time one of your positions gets out of range.

# Description
We, the manual LPooors of DeFi, love doing our daily routine checks on our open positions. Our most pressing question in the morning when we wake up is usually: is my position still in range?
Well, as much as we love checking this manually, wouldn't it be nice to have some tiny piece of automation in our highly manual DeFi fun?
The goal of DeFi Friend is very simple: notify you on discord whenever your LP position is out of range.
So you don't have to worry about manual checks, and just passively wait for DeFi Friend to ping you when you need to act (if you decide to).
At the moment, DeFi Friend is only working on the Maverick DEX on ETH Mainnet and ZKSync, but I plan on adding more Dexes and chains in the future if that's useful.

# Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.10+ installed
- An Infura API key for network connections
- A Discord webhook URL for notifications

# Installation
Follow these steps to install:

- Clone the repository:
```git clone git@github.com:cyrilauberger/defi-friend.git```

- Install required Python packages:
```pip install -r requirements.txt```

- Create a .env file in the root directory with your Infura API key and Discord webhook URL:
```
INFURA_KEY=your_infura_api_key_here
WEBHOOK_URL=your_discord_webhook_url_here
```

# Usage
To use the project, follow these steps:
- Update the owners_networks_pools.csv file. 'owners_networks_pools.csv' is a csv with 3 columns: 
    1. owner (0x address of the LP user),
    2. network, aka chain (at the moment, only `mainnet` and `zksync` are supported),
    3. pool (0x address of the pool).
  
  This is what an example file would look like (with a random address I found):
  ```
  owner,network,pool
  0x37Ff9172beCAf3B78284822eD55a03FAB0Bc9E27,mainnet,0xd50c68c7fbaee4f469e04cebdcfbf1113b4cdadf
  ```

- Run the script:
```python check_in_range.py```

- Then you can run it every X minutes as it suits you

# Contributing to DeFi Friend
To contribute to this project, follow these steps:

- Fork this repository.
- Create a branch: ```git checkout -b <branch_name>```.
- Make your changes and commit them: ```git commit -m '<commit_message>'```
- Push to the original branch: ```git push origin <project_name>/<location>```
- Create the pull request.
- Alternatively, see the GitHub documentation on creating a pull request.
