import json

from objects.account_base import AccountBase
from objects.session_base import SessionBase
from objects.shipper_base import ShipperBase

session = SessionBase(account_id=1)
account = AccountBase(account_id=1)
shipper = ShipperBase(account_id=1)


def print_status(result):
    print(result.get('status', {}).get('code'))


def print_body(result):
    print(json.dumps(result))


def test(payload):
    _result = shipper.create_shipper(**payload)

    print_status(_result)
    print_body(_result)


test({
    "name": "Warehouse",
    "description": "Warehouse shipper",
    "address": {
        "organization_name": "Terrabees Warehouse",
        "unit": "34/123",
        "sub_premise": "Zone B",
        "premise": "Top View Tower",
        "thoroughfare": "Sukhumvit Soi 59",
        "postal_code": "10110",
        "dependent_locality": "Thong Lor",
        "locality": "Bangkok",
        "sub_administrative_area": "Watthana",
        "administrative_area": "Bangkok",
        "country": "Thailand",
        "geocode": {
            "latitude": 13.724738,
            "longitude": 100.582053,
            "accuracy": 14
        }
    }
})
