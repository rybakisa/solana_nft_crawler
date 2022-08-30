from solana.publickey import PublicKey

from solana_helpers import metaplex


def test_derive_metadata_account():
    expected = PublicKey('nL1b5htp5qBsZ6HPczjV62LuY719EMxtZDFZnbFEJp6')
    actual = metaplex.derive_metadata_account('FxVES5ZfUB7M6NM5GN7TDA31cjAhoUV9xaZcE6Wj35cU')
    assert expected == actual


def test_unpack_metadata():
    expected = {
        "update_authority": b"9YjXACMG9MJ6EW9cXneUh5nfc48nUBbwb5DQkhx6qEcY",
        "mint": b"FxVES5ZfUB7M6NM5GN7TDA31cjAhoUV9xaZcE6Wj35cU",
        "data": {
            "name": "Baked Beavers Munchies #7328",
            "symbol": "MNCH",
            "uri": "https://arweave.net/k6cNTNVRPtOaHW4Dvq8nsvrajCKnCdnxitQjfVkSpO0",
            "seller_fee_basis_points": 800,
            "creators": [
                {
                    "address": b"6159yCDy3eC1tBuwuAdjAyVQubrrU7p8fuXgqA2zudiJ",
                    "verified": 1,
                    "share": 0,
                },
                {
                    "address": b"EXoAmjZ2biazBebbn5HduxGJx8Ubo2ZeHDvBpLPdrGCA",
                    "verified": 0,
                    "share": 100,
                },
            ],
        },
        "primary_sale_happened": True,
        "is_mutable": True,
    }
    actual = metaplex.unpack_metadata(
        "BH7+k/aRXkbnNKrXcxnnhZNPX8xtFOevP+rA8cE+r82R3jp7p/vCWTN9subW5S/mTBIicew7GmNvBYu8szVLz2kgAAAAQmFrZWQgQmVhdmV"
        "ycyBNdW5jaGllcyAjNzMyOAAAAAAKAAAATU5DSAAAAAAAAMgAAABodHRwczovL2Fyd2VhdmUubmV0L2s2Y05UTlZSUHRPYUhXNER2cThuc3"
        "ZyYWpDS25DZG54aXRRamZWa1NwTzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAD"
        "AQIAAABKTyHd9B7sx3yzYGzaXAWGEaC8Q0InPOEWego4mPmj+wEAyQuOormCS9swHEAoVdo1Dwf6xvDLcyq+UODPS3ReC4sAZAEBAf4BAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
    )
    assert expected == actual
