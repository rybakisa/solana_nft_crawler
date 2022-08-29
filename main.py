from solana.rpc.api import Client

from solana_helpers import api, metaplex
from settings import START_BLOCK, CANDY_ADDRESSES, PROVIDER_URL


def has_mint(tx: dict) -> bool:
    """
    Filter function to check if transaction has Candy Machine NFT mints

    :param tx: dict: transaction data
    :return: boolean representing if transaction has NFT mints
    """
    # TODO: write explanation for this one liner
    return bool(CANDY_ADDRESSES.intersection(set(tx['transaction']['message']['accountKeys'])))


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
        'content': metaplex.unpack_metadata(raw_token_metadata),
    }


def crawl_nfts(start_block: int):
    """
    Crawling starting point

    :param: start_block int: Block number to crawl from
    :return: List of JSON objects containing NFT token ids and their metadata
    """
    client = Client(PROVIDER_URL)
    blocks = api.get_blocks(start_block)
    print(len(blocks))

    for block_number in blocks:
        block = api.get_block(block_number)

        for tx in block.get('transactions', []):
            # TODO: do more research on this filter
            # TODO: filter out unsuccessful transactions
            if has_mint(tx):
                for token_data in tx['meta'].get('postTokenBalances', []):
                    # TODO: filter only just appeared tokens
                    if token_data['uiTokenAmount']['decimals'] == 0:
                        raw_token_metadata = api.get_token_metadata(client, token_data['mint'])

                        print(
                            serialize(
                                block_number,
                                token_data['mint'],
                                raw_token_metadata,
                            )
                        )


if __name__ == '__main__':
    # TODO: add requirements.txt file
    crawl_nfts(start_block=START_BLOCK)
