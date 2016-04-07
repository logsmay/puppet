import binascii
import os

from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from voluptuous import MultipleInvalid

from objects.account_base import AccountBase
from objects.io.output_manager import OutputManager
from objects.io.response_codes import ResponseCodes
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator


class SessionBase(AccountBase):
    AUTH_TOKEN_LENGTH = 24
    AUTH_TOKEN_TTL = 86400  # seconds

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
                _account = self.get_account(kwargs['email'])

                # Compare user password with hash
                if self.verify_password_hash(kwargs['password'], _account.password):
                    _new_token = binascii.hexlify(os.urandom(SessionBase.AUTH_TOKEN_LENGTH))
                    _new_token = _new_token.decode(encoding='utf-8')

                    try:
                        self.cache_db.set(_new_token, _account.id)
                        self.cache_db.expire(_new_token, SessionBase.AUTH_TOKEN_TTL)

                    except RedisError as e:
                        return _output.output(
                            status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                        )

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
            error_parser = InputErrorParser('create_session')

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )

    def delete_session(self, **kwargs):
        _output = OutputManager()

        try:
            # Validate user inputs
            input_validator = InputValidator('delete_session')
            input_validator.validate(kwargs)

            try:
                self.cache_db.delete(kwargs['auth_token'])

            except RedisError as e:
                return _output.output(
                    status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                )

            return _output.output(
                status=ResponseCodes.OK['success']
            )

        except MultipleInvalid as e:
            error_parser = InputErrorParser('delete_session')

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )
