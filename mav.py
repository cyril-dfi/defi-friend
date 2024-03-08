import datetime
import os
import sys
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3
from hexbytes import HexBytes

from mav_contracts import *

infura_key = "a4be4c2bdcd3460a96e969fc9376db9b"

# account: LocalAccount = Account.from_key(private_key)
# my_address = account.address

network = 'mainnet'

# Connect to JSON-RPC node
json_rpc_url = f'https://{network}.infura.io/v3/{infura_key}'

web3 = Web3(HTTPProvider(json_rpc_url))


class MavContract(object):
  def __init__(self, network, name):
    self.abi = abis[name]
    self.address = addresses[network][name]
    self.contract = web3.eth.contract(address=self.address, abi=self.abi)


PositionInspector = MavContract(network, "PositionInspector")
PoolInformation = MavContract(network, "PoolInformation")

def get_balance_from_gwei(balance):
  # Divide by 10**18
  return web3.from_wei(balance, 'ether')

def get_balances(owner, pool):
  # NB : Might be a problem if an owner has more than one position on a single pool
  balances = PositionInspector.contract.functions.addressBinReservesAllKindsAllTokenIds(owner=owner, pool=pool).call()
  balance_a = get_balance_from_gwei(balances[0])
  balance_b = get_balance_from_gwei(balances[1])
  print(f"Balance of token A: {balance_a}")
  print(f"Balance of token B: {balance_b}")
  return balance_a, balance_b

def get_price(pool):
  sqrt_price = PoolInformation.contract.functions.getSqrtPrice(pool=pool).call()
  price = get_balance_from_gwei(sqrt_price) ** 2
  print(f"Price of asset B in asset A: {price}")
  return price


def get_active_tick_start_and_end_price(pool):
# Take all active bins, and loop through them, and find the bin with both A and B tokens > this is bin of the current price
# Then take bin ID - 1, and + 1 to get the min and max of the range of the active bin
  all_active_bins = PoolInformation.contract.functions.getActiveBins(pool=pool, startBinIndex=0, endBinIndex=0).call()

  for active_bin in all_active_bins:
    bin_id = active_bin[0]
    bin_kind = active_bin[1]
    bin_lower_tick = active_bin[2]
    bin_reserve_a = active_bin[3]
    bin_reserve_b = active_bin[4]
    #mergeId ? cf https://etherscan.io/address/0x0087D11551437c3964Dddf0F4FA58836c5C5d949#code
    if bin_reserve_a != 0 and bin_reserve_b != 0:
      print(f"Lower tick of active bin is {bin_lower_tick}")
      break

  tickLiquidityBefore = PoolInformation.contract.functions.tickLiquidity(pool=pool, tick=bin_lower_tick-1).call()
  active_tick_start_price = get_balance_from_gwei(tickLiquidityBefore[0]) ** 2
  tickLiquidityAfter = PoolInformation.contract.functions.tickLiquidity(pool=pool, tick=bin_lower_tick+1).call()
  active_tick_end_price = get_balance_from_gwei(tickLiquidityAfter[0]) ** 2
  print(f"Pool active tick Start Price is {active_tick_start_price}")
  print(f"Pool active tick End Price is {active_tick_end_price}")
  return active_tick_start_price, active_tick_end_price


def is_out_of_range(owner, pool):
  balance_a, balance_b = get_balances(owner, pool)
  if balance_a == 0 or balance_b == 0:
    print(f"Owner {owner.hex()} is out of range on pool {pool.hex()}")
    return True
  print(f"Owner {owner.hex()} is in range on pool {pool.hex()}")
  return False


# get_balances(owner, pool)
# get_price(pool)
# get_active_tick_start_and_end_price(pool)
# is_out_of_range(owner, pool)

