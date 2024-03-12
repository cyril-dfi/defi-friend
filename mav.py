from hexbytes import HexBytes
import logging
from web3 import HTTPProvider, Web3

from config import *


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MavContract(object):
  def __init__(self, network, name):
    self.network = network
    self.name = name
    self.web3 = Web3(HTTPProvider(json_rpc_urls[self.network]))
    self.abi = abis[self.name]
    self.address = addresses[self.network][self.name]
    self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)
    
  def from_wei(self, balance):
    """Converts balance from gwei to ether."""
    return self.web3.from_wei(balance, 'ether')


class PositionInspectorContract(MavContract):
    """Subclass of MavContract specialized for the PositionInspector contract."""
    def __init__(self, network, name='PositionInspector'):
        super().__init__(network, 'PositionInspector')


    def get_balances(self, owner, pool):
        """Fetches balances for a given owner and pool."""
        logging.info(f"Fetching token balances for owner {owner.hex()} on pool {pool.hex()}")
        balances = self.contract.functions.addressBinReservesAllKindsAllTokenIds(owner=owner, pool=pool).call()
        # NB : Might be a problem if an owner has more than one position in a single pool

        balance_a = self.from_wei(balances[0])
        balance_b = self.from_wei(balances[1])

        logging.info(f"Balance of token A: {balance_a}")
        logging.info(f"Balance of token B: {balance_b}")

        return balance_a, balance_b

    def is_out_of_range(self, owner, pool):
        """Determines if the owner is out of range for the specified pool."""
        balance_a, balance_b = self.get_balances(owner, pool)

        in_range_msg = f"Owner {owner.hex()} is in range on pool {pool.hex()}"
        out_of_range_msg = f"Owner {owner.hex()} is out of range on pool {pool.hex()}"

        if balance_a == 0 or balance_b == 0:
            logging.info(out_of_range_msg)
            return True

        logging.info(in_range_msg)
        return False


class PoolInformationContract(MavContract):
    """Subclass of MavContract specialized for the PositionInspector contract."""
    def __init__(self, network, name='PoolInformation'):
        super().__init__(network, 'PoolInformation')


    def get_price(self, pool, network):
      """Gets the current price of the pair"""
      sqrt_price = self.contract.functions.getSqrtPrice(pool=pool).call()
      price = self.from_wei(sqrt_price) ** 2
      logging.info(f"Price of asset B in asset A: {price}")
      return price


    def get_active_tick_start_and_end_price(self, pool, network):
      # Take all active bins, and loop through them, and find the bin with both A and B tokens > this is bin of the current price
      # Then take bin ID - 1, and + 1 to get the min and max of the range of the active bin
      all_active_bins = self.contract.functions.getActiveBins(pool=pool, startBinIndex=0, endBinIndex=0).call()

      for active_bin in all_active_bins:
        bin_id = active_bin[0]
        bin_kind = active_bin[1]
        bin_lower_tick = active_bin[2]
        bin_reserve_a = active_bin[3]
        bin_reserve_b = active_bin[4]
        #mergeId ? cf https://etherscan.io/address/0x0087D11551437c3964Dddf0F4FA58836c5C5d949#code
        if bin_reserve_a != 0 and bin_reserve_b != 0:
          logging.info(f"Lower tick of active bin is {bin_lower_tick}")
          break

      tickLiquidityBefore = self.contract.functions.tickLiquidity(pool=pool, tick=bin_lower_tick-1).call()
      active_tick_start_price = self.from_wei(tickLiquidityBefore[0]) ** 2
      tickLiquidityAfter = self.contract.functions.tickLiquidity(pool=pool, tick=bin_lower_tick+1).call()
      active_tick_end_price = self.from_wei(tickLiquidityAfter[0]) ** 2
      logging.info(f"Pool active tick Start Price is {active_tick_start_price}")
      logging.info(f"Pool active tick End Price is {active_tick_end_price}")
      return active_tick_start_price, active_tick_end_price