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
    "address": [
        {
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
            "country": "TH",
            "geocode": {
                "latitude": 13.724738,
                "longitude": 100.582053,
                "accuracy": 14
            },
            "contact": [
                {
                    "first_name": "Nirmal",
                    "last_name": "Natarajan",
                    "phone_country": 'TH',
                    "phone_number": 908857089,
                    "phone_extension": 22,
                    "email": "thinknirmal@gmail.com"
                },
                {
                    "first_name": "Naphat",
                    "last_name": "Theerawat",
                    "phone_country": 'TH',
                    "phone_number": 912345678,
                    "email": "new@terrabees.com"
                }
            ],
            "dispatch_time": [
                {
                    "start_time": '09:00:00',
                    "end_time": '12:30:00'
                },
                {
                    "start_time": '13:30:00',
                    "end_time": '18:00:00'
                }
            ]
        },
        {
            "organization_name": "Apple Store",
            "unit": "456",
            "sub_premise": "Second Floor",
            "premise": "Siam Paragon",
            "thoroughfare": "Sukhumvit Road",
            "postal_code": "10112",
            "dependent_locality": "Siam",
            "locality": "Bangkok",
            "sub_administrative_area": "Khlong Toey",
            "administrative_area": "Bangkok",
            "country": "TH",
            "geocode": {
                "latitude": 13.724738,
                "longitude": 100.582053,
                "accuracy": 14
            },
            "contact": [
                {
                    "first_name": "Mahima",
                    "last_name": "Natarajan",
                    "phone_country": "TH",
                    "phone_number": 908857089,
                    "phone_extension": 22,
                    "email": "mahimarn@gmail.com"
                },
                {
                    "first_name": "Shreesha",
                    "last_name": "B.U.",
                    "phone_country": "TH",
                    "phone_number": 912345678,
                    "email": "shreesha@terrabees.com"
                }
            ],
            "dispatch_time": [
                {
                    "start_time": '09:00:00',
                    "end_time": '12:30:00'
                },
                {
                    "start_time": '13:30:00',
                    "end_time": '15:00:00'
                },
                {
                    "start_time": '15:30:00',
                    "end_time": '18:00:00'
                }
            ]
        }
    ]
})
