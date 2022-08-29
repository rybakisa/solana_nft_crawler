"""Helper functions for dealing with Solana Blockchain JSON RPC API"""

from solana.rpc.api import Client

from settings import PAGE_SIZE
from .metaplex import derive_metadata_account


def get_blocks_page(client: Client, start_block: int, end_block: int) -> list[int]:
    """
    Get no more that PAGE_SIZE amount of blocks from blockchain provider API

    :param client: Client: Solana HTTP API Client object
    :param start_block: int: Block number to crawl from
    :param end_block: int: Block number to crawl to
    :return: list of confirmed blocks within a page
    """
    assert start_block < end_block

    # TODO: handle HTTP error codes
    return client.get_blocks(start_block, end_block).get('result', [])


def get_latest_block_number(client: Client) -> int:
    """
    Get current time slot for Solana blockchain

    :param client: Client: Solana HTTP API Client object
    :return: Current timeslot for Solana blockchain
    """
    # TODO: handle HTTP error codes
    return client.get_slot().get('result', 0)


def get_blocks(client: Client, start_block: int) -> list[int]:
    """
    Get all confirmed blocks considering pagination

    :param client: Client: Solana HTTP API Client object
    :param start_block: int: Block number to crawl from
    :return: List of all confirmed blocks
    """
    end_block = get_latest_block_number(client)

    assert start_block < end_block
    pages_count = (end_block - start_block) // PAGE_SIZE

    return [
        item
        for i in range(pages_count + 1)
        for item in get_blocks_page(
            client,
            start_block + PAGE_SIZE * i,
            start_block + PAGE_SIZE * (i + 1),
        )
    ]


def get_block(client: Client, number: int) -> dict:
    """
    Returns identity and transaction information about a confirmed block in the ledger

    :param client: Client: Solana HTTP API Client object
    :param number: int: a slot integer denoting the target block number
    :return: dict containing identity and transaction information about a confirmed block
    """
    # TODO: handle HTTP error codes
    return client.get_block(number).get('result', {})


def get_token_metadata(client: Client, mint_key: str) -> str:
    """
    Get NFT metadata by mint address

    :param client: Client: Solana HTTP API Client object
    :param mint_key: SPL token address
    :return: decoded Metaplex on-chain Metadata
    """
    metadata_account = derive_metadata_account(mint_key)
    # TODO: handle HTTP error codes
    # TODO: catch KeyError exceptions
    rawdata = client.get_account_info(metadata_account)['result']['value']['data'][0]
    return rawdata
