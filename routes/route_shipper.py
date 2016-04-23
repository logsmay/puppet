import json

from objects.shipper_base import ShipperBase


class RouteShipper(object):
    @staticmethod
    def on_post(req, resp):
        _shipper = ShipperBase()

        # Request body
        _payload = json.loads(str(req.stream.read(), encoding='utf-8'))
        # Authenticated execution
        _shipper.register_auth_token(req.auth)
        _result = _shipper.create_shipper(**_payload)
        # Response handlers
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
