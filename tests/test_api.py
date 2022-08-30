from unittest.mock import patch
import pytest

from solana_helpers import api


@pytest.fixture
def client_instance():
    with patch('solana.rpc.api.Client') as MockClient:
        instance = MockClient.return_value
        instance.get_slot.return_value = {'jsonrpc': '2.0', 'result': 148271989, 'id': 2}
        instance.get_block.return_value = {
            "jsonrpc": "2.0",
            "result": {
                "blockHeight": None,
                "blockTime": None,
                "blockhash": "AcknnkY4ok5BZuk69WijDETKVRUPZoMtniZHMe4ZaK1e",
                "parentSlot": 0,
                "previousBlockhash": "4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZAMdL4VZHirAn",
                "rewards": [],
                "transactions": [],
            },
            "id": 14,
        }
        instance.get_blocks.return_value = {
            "jsonrpc": "2.0",
            "result": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            "id": 16,
        }
        yield instance


def test_get_blocks_page(client_instance):
    expected = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    actual = api.get_blocks_page(client_instance, 100, 110)
    assert expected == actual


def test_get_latest_block_number(client_instance):
    expected = 148271989
    actual = api.get_latest_block_number(client_instance)
    assert expected == actual


def test_get_block(client_instance):
    expected = {
        "blockHeight": None,
        "blockTime": None,
        "blockhash": "AcknnkY4ok5BZuk69WijDETKVRUPZoMtniZHMe4ZaK1e",
        "parentSlot": 0,
        "previousBlockhash": "4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZAMdL4VZHirAn",
        "rewards": [],
        "transactions": [],
    }
    actual = api.get_block(client_instance, 1)
    assert expected == actual
