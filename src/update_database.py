"""
Update database
"""
import os
import time
from slickrpc import Proxy
from logger import Logger
import mongo
from btc_block_iterator import BTCBlockIterator
from tx_cache import TxCache
from tx_resolve import resolve_input_addresses


class BlockchainDBMaintainer:
    """
    responsible for inserting blocks from cryptocurency node
    to mongoDB and resolving transaction input addresses
    """

    def __init__(self):
        self.logger = Logger()
        self.mongo = mongo.Mongo(self.logger)
        self.rpc_connection = Proxy(
            f"http://{os.environ['CRYPTO_USER']}:{os.environ['CRYPTO_PASS']}@"
            f"{os.environ['CRYPTO_HOST']}:{os.environ['CRYPTO_PORT']}"
        )
        self.tx_cache = TxCache(logger=self.logger)

    def run(self):
        """execution starts here"""
        while True:
            start_time = time.time()
            self.save_blocks()
            self.logger.info('current collection count: {}'.format(
                self.mongo.blocks_collection.count()
            ))
            time_to_sleep = max(0, 30 - int(time.time() - start_time))
            if time_to_sleep > 10:
                self.tx_cache.reduce_size()
            time.sleep(time_to_sleep)

    def save_blocks(self):
        """saves blocks"""
        for block in BTCBlockIterator(
                self.rpc_connection,
                self.logger,
                self.mongo):
            if block['height'] % 100 == 0:
                self.logger.info(f"saving block (height: {block['height']})")
            self.tx_cache.add_from_block(block)
            resolve_input_addresses(block, self.tx_cache, self.mongo, self.logger)
            self.mongo.save_block(block)


if __name__ == '__main__':
    while True:
        try:
            BlockchainDBMaintainer().run()
        except Exception as e:
            print(e)
            time.sleep(10)


