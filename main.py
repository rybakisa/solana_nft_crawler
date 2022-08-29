"""Solana NFT Crawler entry point file"""

from solana.rpc.api import Client

from crawler import run_crawler
from settings import PROVIDER_URL, PROVIDER_TIMEOUT


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Solana NFT Crawler')
    parser.add_argument(
        'start_block',
        metavar='start_block',
        type=int,
        help='an integer for the start_block slot',
    )
    args = parser.parse_args()

    run_crawler(
        client=Client(
            endpoint=PROVIDER_URL,
            timeout=PROVIDER_TIMEOUT,
        ),
        start_block=args.start_block,
    )
