from sqlalchemy.exc import SQLAlchemyError
from voluptuous import MultipleInvalid

from models.puppet_model import (
    Consignor,
    Address,
    AddressGeo,
    AddressContact,
    AddressDispatchTime
)
from objects.io.output_manager import OutputManager
from objects.io.response_codes import ResponseCodes
from objects.session_base import SessionBase, InvalidSession
from utils.functions import remove_children, merge_range
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator


class ConsignorBase(SessionBase):
    def __init__(self, account_id=None):
        super(ConsignorBase, self).__init__(account_id=account_id)

    def create_consignor(self, **payload):
        _output = OutputManager()

        try:
            self.protect()

            _validator_key = self.create_consignor.__name__

            try:
                # Validate user inputs
                InputValidator(_validator_key).validate(payload)

                # Extract children values as they will be removed in the next step
                _consignor_payload = payload
                _address_payload = _consignor_payload['address']

                # Remove nested arrays and dictionaries
                remove_children(_consignor_payload)

                # Set account ID as foreign key
                _consignor_payload.update({
                    Consignor.fk_account_id.key: self.get_account_id()
                })

                try:
                    # Create a new consignor
                    _new_consignor = Consignor(**_consignor_payload)
                    self.puppet_db.add(_new_consignor)

                    # Insert ID of the new consignor
                    self.puppet_db.flush()
                    _consignor_insert_id = _new_consignor.id

                    #################
                    # ## Address ## #
                    #################
                    for address in _address_payload:
                        # Extract children values as they will be removed in the next step
                        _contact_payload = address['contact']
                        _dispatch_time_payload = address['dispatch_time']

                        if 'geocode' in address:
                            _geo_payload = address['geocode']
                        else:
                            _geo_payload = {}

                        # Remove nested arrays and dictionaries
                        remove_children(address)

                        # Set consignor ID as foreign key
                        address.update({
                            Address.fk_consignor_id.key: _consignor_insert_id
                        })

                        # Create a new address
                        _new_address = Address(**address)
                        self.puppet_db.add(_new_address)

                        # Insert ID of the new address
                        self.puppet_db.flush()
                        _address_insert_id = _new_address.id

                        #################
                        # ## Contact ## #
                        #################
                        for contact in _contact_payload:
                            # Remove nested arrays and dictionaries
                            remove_children(contact)

                            # Set address ID as foreign key
                            contact.update({
                                AddressContact.fk_address_id.key: _address_insert_id
                            })

                            # Create new contact
                            _new_contact = AddressContact(**contact)
                            self.puppet_db.add(_new_contact)

                        #######################
                        # ## Dispatch time ## #
                        #######################
                        # Find overlaps in time ranges and merge them when possible
                        _dispatch_time_payload = list(merge_range(
                            ranges=_dispatch_time_payload,
                            start_key=AddressDispatchTime.start_time.key,
                            end_key=AddressDispatchTime.end_time.key
                        ))

                        # Iterate and store
                        for dispatch_time in _dispatch_time_payload:
                            # Remove nested arrays and dictionaries
                            remove_children(dispatch_time)

                            # Set address ID as foreign key
                            dispatch_time.update({
                                AddressDispatchTime.fk_address_id.key: _address_insert_id
                            })

                            # Create new dispatch time
                            _new_dispatch_time = AddressDispatchTime(**dispatch_time)
                            self.puppet_db.add(_new_dispatch_time)

                        #################
                        # ## Geocode ## #
                        #################
                        if _geo_payload:
                            # Remove nested arrays and dictionaries
                            remove_children(_geo_payload)

                            # Set address ID as foreign key
                            _geo_payload.update({
                                AddressGeo.fk_address_id.key: _address_insert_id
                            })

                            # Create new geocode entry
                            _new_geo = AddressGeo(**_geo_payload)
                            self.puppet_db.add(_new_geo)

                    # Commit database changes
                    self.puppet_db.commit()

                    # Respond with success message
                    return _output.output(
                        status=ResponseCodes.OK['success']
                    )

                except SQLAlchemyError:
                    # Rollback database changes
                    self.puppet_db.rollback()

                    # Respond with failure message
                    return _output.output(
                        status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                    )

            except MultipleInvalid as e:
                # Parser to streamline Voluptuous errors
                error_parser = InputErrorParser()

                # Respond with input validation errors
                return _output.output(
                    status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                    data=error_parser.translate_errors(e)
                )

        except InvalidSession:
            # Kick the intruder out
            return _output.output(
                status=ResponseCodes.UNAUTHORIZED['authError']
            )
