"""Solana NFT Crawler entry point file with helper functions"""

from solana.rpc.api import Client

from solana_helpers import api, metaplex
from settings import PROVIDER_URL, PROVIDER_TIMEOUT


def serialize(block_number: int, token_address: str, raw_token_metadata: str) -> dict:
    """
    Serialize crawled data into needed format

    :param block_number: int: Solana block number
    :param token_address: str: SPL token address
    :param raw_token_metadata: str: encoded Metaplex on-chain Metadata
    :return: serialized object
    """
    return {
        'token_id': token_address,
        'block_number': block_number,
        'content': metaplex.unpack_metadata(raw_token_metadata) if raw_token_metadata else '',
    }


def is_nft(token_data: dict) -> bool:
    """
    Check if SPL token is an NFT

    :param token_data: dict: token data from transaction
    :return: bool representing if SPL token is an NFT
    """
    return (
        token_data["uiTokenAmount"]["decimals"] == 0
        and int(token_data["uiTokenAmount"]["amount"]) == 1
    )


def get_tokens_transfers(tx: dict) -> list:
    """
    Get transaction's tokens transfer metadata

    :param tx: dict: Solana transaction object
    :return: SPL token transfers data from transaction's metadata
    """
    # TODO: catch KeyError exceptions
    pre_token_balances = tx['meta'].get('preTokenBalances', [])
    post_token_balances = tx['meta'].get('postTokenBalances', [])

    token_transfers = []
    for post_balance in post_token_balances:
        # using for-else syntax
        for pre_balance in pre_token_balances:
            if pre_balance['mint'] == post_balance['mint']:
                break
        else:
            token_transfers.append(post_balance)

    return token_transfers


def crawl_nfts(client: Client, start_block: int) -> None:
    """
    Crawling starting point

    :param client: Client: Solana HTTP API Client object
    :param start_block: int: Block number to crawl from
    :return: List of JSON objects containing NFT token ids and their metadata
    """
    blocks = api.get_blocks(client, start_block)

    for block_number in blocks:
        block = api.get_block(client, block_number)

        block_mints_output = []

        for tx in block.get('transactions', []):
            # TODO: filter out unsuccessful transactions
            # TODO: filter out transactions unrelated to tokens
            mints = [item for item in get_tokens_transfers(tx) if is_nft(item)]
            for mint in mints:
                block_mints_output.append(
                    serialize(
                        block_number,
                        mint['mint'],
                        api.get_token_metadata(client, mint['mint']),
                    )
                )

        if block_mints_output:
            print(block_mints_output)


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

    crawl_nfts(
        client=Client(
            endpoint=PROVIDER_URL,
            timeout=PROVIDER_TIMEOUT,
        ),
        start_block=args.start_block,
    )
