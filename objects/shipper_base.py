from sqlalchemy.exc import SQLAlchemyError
from voluptuous import MultipleInvalid

from models.puppet_model import Shipper, Address, AddressGeo
from objects.io.output_manager import OutputManager
from objects.io.response_codes import ResponseCodes
from objects.session_base import SessionBase, InvalidSession
from utils.functions import remove_children
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator


class ShipperBase(SessionBase):
    def __init__(self, account_id=None):
        super(ShipperBase, self).__init__(account_id=account_id)

    def create_shipper(self, **payload):
        _output = OutputManager()

        try:
            self.protect()

            _validator_key = self.create_shipper.__name__

            try:
                # Validate user inputs
                InputValidator(_validator_key).validate(payload)

                _shipper_payload = payload
                _address_payload = _shipper_payload['address']
                _geo_payload = {}

                if 'geocode' in _address_payload:
                    _geo_payload = _address_payload['geocode']

                remove_children(_shipper_payload)
                _shipper_payload.update({
                    Shipper.fk_account_id.key: self.get_account_id()
                })

                try:
                    # Create a new shipper
                    _new_shipper = Shipper(**_shipper_payload)
                    self.puppet_db.add(_new_shipper)
                    self.puppet_db.flush()

                    _shipper_insert_id = _new_shipper.id

                    remove_children(_address_payload)
                    _address_payload.update({
                        Address.fk_shipper_id.key: _shipper_insert_id
                    })

                    # Create a new address
                    _new_address = Address(**_address_payload)
                    self.puppet_db.add(_new_address)
                    self.puppet_db.flush()

                    if _geo_payload:
                        _address_insert_id = _new_address.id

                        remove_children(_geo_payload)
                        _geo_payload.update({
                            AddressGeo.fk_address_id.key: _address_insert_id
                        })

                        # Create new geocode entry
                        _new_geo = AddressGeo(**_geo_payload)
                        self.puppet_db.add(_new_geo)
                        self.puppet_db.flush()

                    self.puppet_db.commit()

                    return _output.output(
                        status=ResponseCodes.OK['success']
                    )
                except SQLAlchemyError:
                    self.puppet_db.rollback()

                    return _output.output(
                        status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                    )

            except MultipleInvalid as e:
                error_parser = InputErrorParser()

                return _output.output(
                    status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                    data=error_parser.translate_errors(e)
                )

        except InvalidSession:
            return _output.output(
                status=ResponseCodes.UNAUTHORIZED['authError']
            )