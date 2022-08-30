"""Fetched data processing related functions"""

from solana.rpc.api import Client

from solana_helpers import api, metaplex


def serialize(block_number: int, token_address: str, raw_token_metadata: str) -> dict:
    """
    Serialize crawled data into a needed format.

    :param block_number: int: Solana block number
    :param token_address: str: SPL token address
    :param raw_token_metadata: str: encoded Metaplex on-chain Metadata
    :return: serialized NFT metadata
    """
    return {
        'token_id': token_address,
        'block_number': block_number,
        'content': metaplex.unpack_metadata(raw_token_metadata) if raw_token_metadata else '',
    }


def is_nft_mint(token_data: dict) -> bool:
    """
    Check if SPL token transfer is an NFT mint.

    According to standard NFT must have decimals equal to 0.
    Also checking that token amount after transfer equal 1.

    :param token_data: dict: token data from transaction
    :return: bool representing if SPL token is an NFT
    """
    return (
        token_data["uiTokenAmount"]["decimals"] == 0
        and int(token_data["uiTokenAmount"]["amount"]) == 1
    )


def get_created_tokens(tx: dict) -> list:
    """
    Get tokens created during the transaction.

    Comparing token balances before and after the transaction
    to found tokens with no balance before and some balance after.

    :param tx: dict: Solana transaction object
    :return: SPL token created during the transaction
    """
    # TODO: catch KeyError exceptions
    pre_token_balances = tx['meta'].get('preTokenBalances', [])
    post_token_balances = tx['meta'].get('postTokenBalances', [])

    created_tokens = []
    for post_balance in post_token_balances:
        # using for-else syntax
        for pre_balance in pre_token_balances:
            if pre_balance['mint'] == post_balance['mint']:
                break
        else:
            created_tokens.append(post_balance)

    return created_tokens


def run_crawler(client: Client, start_block: int) -> None:
    """
    Crawling starting point.

    Fetching blocks, processing blocks and their transactions.

    :param client: Client: Solana HTTP API Client object
    :param start_block: int: block number to crawl from
    """
    blocks = api.get_blocks(client, start_block)

    for block_number in blocks:
        block = api.get_block(client, block_number)

        block_mints_output = []

        for tx in block.get('transactions', []):
            # TODO: filter out unsuccessful transactions
            # TODO: filter out transactions unrelated to tokens
            mints = [item for item in get_created_tokens(tx) if is_nft_mint(item)]
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
