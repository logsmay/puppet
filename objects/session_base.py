import binascii
import os

import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from voluptuous import MultipleInvalid

from objects.account_base import AccountBase
from objects.io.output_manager import OutputManager
from objects.io.response_codes import ResponseCodes
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator


class SessionBase(AccountBase):
    AUTH_TOKEN_LENGTH = 48
    AUTH_TOKEN_TTL = 1800  # seconds

    def __init__(self):
        super(SessionBase, self).__init__()
        self.cache_db = self.get_db('session-cache')

    def create_session(self, **kwargs):
        _output = OutputManager()

        try:
            # Validate user inputs
            input_validator = InputValidator('create_session')
            input_validator.validate(kwargs)

            try:
                for account in self.get_account(kwargs['email']):
                    # Compare user password with hash
                    if bcrypt.hashpw(kwargs['password'], account.password) == account.password:
                        _new_token = binascii.hexlify(os.urandom(SessionBase.AUTH_TOKEN_LENGTH))
                        self.cache_db.set(_new_token, 'y')
                        self.cache_db.expire(_new_token, SessionBase.AUTH_TOKEN_TTL)

                        return _output.output(
                            status=ResponseCodes.OK['success'],
                            data={
                                'auth_token': _new_token
                            }
                        )
                    else:
                        return _output.output(
                            status=ResponseCodes.UNAUTHORIZED['authError']
                        )
            except (NoResultFound, MultipleResultsFound):
                return _output.output(
                    status=ResponseCodes.UNAUTHORIZED['authError']
                )
            except SQLAlchemyError:
                return _output.output(
                    status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                )

        except MultipleInvalid as e:
            error_parser = InputErrorParser('create_account')

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )
