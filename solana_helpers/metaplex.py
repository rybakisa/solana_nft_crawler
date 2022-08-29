import base64
import struct

from solana.publickey import PublicKey
import base58

from settings import METADATA_PROGRAM_ID


def derive_metadata_account(mint_key: str):
    """
    Derive metadata account from SPL token mint account

    :param mint_key: str: SPL token mint account
    :return: metadata account PublicKey object
    """
    return PublicKey.find_program_address(
        [
            b'metadata',
            bytes(PublicKey(METADATA_PROGRAM_ID)),
            bytes(PublicKey(mint_key)),
        ],
        PublicKey(METADATA_PROGRAM_ID),
    )[0]


def unpack_metadata(data):
    """
    Decode Metaplex Metadata

    :param data: encoded metaplex metadata
    :return: decoded metaplex metadata
    """
    data = base64.b64decode(data)
    assert data[0] == 4
    i = 1
    source_account = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
    i += 32
    mint_account = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
    i += 32
    name_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    name = struct.unpack('<' + "B" * name_len, data[i:i + name_len])
    i += name_len
    symbol_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    symbol = struct.unpack('<' + "B" * symbol_len, data[i:i + symbol_len])
    i += symbol_len
    uri_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    uri = struct.unpack('<' + "B" * uri_len, data[i:i + uri_len])
    i += uri_len
    fee = struct.unpack('<h', data[i:i + 2])[0]
    i += 2
    has_creator = data[i]
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack('<I', data[i:i + 4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
            creators.append(creator)
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    metadata = {
        "update_authority": source_account,
        "mint": mint_account,
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata