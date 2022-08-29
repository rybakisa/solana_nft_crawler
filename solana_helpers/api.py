from typing import List

import requests

from settings import PROVIDER_URL, PAGE_SIZE
from .metaplex import derive_metadata_account


def get_blocks_page(start_block: int) -> List:
    """
    Get no more that PAGE_SIZE amount of blocks from blockchain provider API

    :param start_block: int: Block number to crawl from
    :return: Full list of confirmed blocks
    """
    payload = {
        # TODO: generate id
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getBlocks",
        "params": [start_block, start_block + PAGE_SIZE]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # TODO: add timeout argument
    # TODO: handle HTTP error codes
    response = requests.post(PROVIDER_URL, json=payload, headers=headers)
    return response.json().get('result', [])


def get_blocks(start_block: int) -> List:
    """
    Get all confirmed blocks considering pagination

    :param start_block: int: Block number to crawl from
    :return: List of all confirmed blocks
    """
    blocks = []
    blocks_page = get_blocks_page(start_block)

    while len(blocks_page) == PAGE_SIZE:
        blocks += blocks_page
        blocks_page = get_blocks_page(start_block + PAGE_SIZE)

    return blocks + blocks_page


def get_block(number: int) -> dict:
    """
    Returns identity and transaction information about a confirmed block in the ledger

    :param number: int: a slot integer denoting the target block number
    :return: dict containing identity and transaction information about a confirmed block
    """
    payload = {
        # TODO: generate id
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getBlock",
        "params": [number]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # TODO: add timeout argument
    # TODO: handle HTTP error codes
    response = requests.post(PROVIDER_URL, json=payload, headers=headers)
    return response.json().get('result', {})


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
