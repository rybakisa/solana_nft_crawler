from typing import List

from settings import PAGE_SIZE
from .metaplex import derive_metadata_account


def get_blocks_page(client, start_block: int, end_block: int) -> List:
    """
    Get no more that PAGE_SIZE amount of blocks from blockchain provider API

    :param client: Solana HTTP API Client object
    :param start_block: int: Block number to crawl from
    :param end_block: int: Block number to crawl to
    :return: list of confirmed blocks within a page
    """
    assert start_block < end_block

    # TODO: handle HTTP error codes
    return client.get_blocks(start_block, end_block).get('result', [])


def get_latest_block_number(client):
    """
    Get current time slot for Solana blockchain

    :param client: Solana HTTP API Client object
    :return: Current timeslot for Solana blockchain
    """
    return client.get_slot().get('result', 0)


def get_blocks(client, start_block: int) -> List:
    """
    Get all confirmed blocks considering pagination

    :param client: Solana HTTP API Client object
    :param start_block: int: Block number to crawl from
    :return: List of all confirmed blocks
    """
    blocks = []
    end_block = get_latest_block_number(client)

    assert start_block < end_block
    pages_count = (end_block - start_block) // PAGE_SIZE

    for i in range(pages_count + 1):
        blocks += get_blocks_page(
            client,
            start_block + PAGE_SIZE * i,
            start_block + PAGE_SIZE * (i + 1),
        )

    return blocks


def get_block(client, number: int) -> dict:
    """
    Returns identity and transaction information about a confirmed block in the ledger

    :param client: Solana HTTP API Client object
    :param number: int: a slot integer denoting the target block number
    :return: dict containing identity and transaction information about a confirmed block
    """
    # TODO: handle HTTP error codes
    return client.get_block(number).get('result', {})


def get_token_metadata(client, mint_key):
    """
    Get NFT metadata by mint address

    :param client: Solana HTTP API Client object
    :param mint_key: SPL token address
    :return: decoded Metaplex on-chain Metadata
    """
    metadata_account = derive_metadata_account(mint_key)
    rawdata = client.get_account_info(metadata_account)['result']['value']['data'][0]
    return rawdata
