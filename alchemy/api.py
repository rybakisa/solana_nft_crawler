from typing import List

import requests


# TODO: move to settings file
# TODO: get values from env
PROVIDER_API_KEY = 'demo'
PROVIDER_URL = f'https://solana-mainnet.g.alchemy.com/v2/{PROVIDER_API_KEY}'
CANDY_ADDRESSES = {
    'cndyAnrLdpjq1Ssp1z8xxDsB8dxe7u4HL5Nxi2K5WXZ',
    'cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ',
}
PAGE_SIZE = 100000


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


def get_block(number: int):
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


def has_mint(tx: dict) -> bool:
    """
    Filter function to check if transaction has Candy Machine NFT mints

    :param tx: dict: transaction data
    :return: boolean representing if transaction has NFT mints
    """
    # TODO: write explanation for this one liner
    return bool(CANDY_ADDRESSES.intersection(set(tx['transaction']['message']['accountKeys'])))
