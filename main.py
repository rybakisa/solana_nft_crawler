from alchemy import api, metadata

START_BLOCK = 148065394


def serialize(block_number: int, token_address: str, token_metadata: dict) -> dict:
    """
    Serialize crawled data into needed format

    :param block_number: int: Solana block number
    :param token_address: str: SPL token address
    :param token_metadata: dict: decoded Metaplex on-chain Metadata
    :return: serialized object
    """
    return {
        'token_id': token_address,
        'block_number': block_number,
        'content': token_metadata,
    }


def crawl_nfts(start_block: int):
    """
    Crawling starting point

    :param: start_block int: Block number to crawl from
    :return: List of JSON objects containing NFT token ids and their metadata
    """
    blocks = api.get_blocks(start_block)

    for block_number in blocks:
        block = api.get_block(block_number)

        for tx in block.get('transactions', []):
            # TODO: do more research on this filter
            if api.has_mint(tx):
                for token_data in tx['meta'].get('postTokenBalances', []):
                    # TODO: filter only just appeared tokens
                    if token_data['uiTokenAmount']['decimals'] == 0:
                        token_metadata = metadata.get_metadata(token_data['mint'])

                        print(
                            serialize(
                                block_number,
                                token_data['mint'],
                                token_metadata,
                            )
                        )


if __name__ == '__main__':
    # TODO: add requirements.txt file
    crawl_nfts(start_block=START_BLOCK)
