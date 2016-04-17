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

    def __init__(self, account_id=None, auth_token=None):

        super(SessionBase, self).__init__()

        if auth_token:
            self.__set_session(auth_token)
        elif account_id:
            self.account_id = account_id

    def create_session(self, **payload):
        _output = OutputManager()
        _validator_key = self.create_session.__name__

        try:
            # Validate user inputs
            InputValidator(_validator_key).validate(payload)

            try:
                _account = self.get_account(email=payload['email'])

                # Compare user password with hash
                if self.verify_password_hash(payload['password'], _account.password):
                    _new_token = binascii.hexlify(os.urandom(SessionBase.AUTH_TOKEN_LENGTH))
                    _new_token = _new_token.decode(encoding='utf-8')

                    try:
                        self.session_db.set(_new_token, _account.id)
                        self.session_db.expire(_new_token, SessionBase.AUTH_TOKEN_TTL)
                        self.session_db.rpush(_account.id, _new_token)
                        self.session_db.ltrim(_account.id, 0, 999)

                        return _output.output(
                            status=ResponseCodes.OK['success'],
                            data={
                                'auth_token': _new_token
                            }
                        )

                    except RedisError as e:
                        return _output.output(
                            status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
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
            error_parser = InputErrorParser(_validator_key)

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )

    def delete_session(self):
        _output = OutputManager()

        try:
            self.session_db.delete(self.auth_token)

        except RedisError:
            return _output.output(
                status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
            )

        return _output.output(
            status=ResponseCodes.OK['success']
        )

    def __set_session(self, auth_token):
        _output = OutputManager()

        _account_id = self.session_db.get(auth_token)

        if not _account_id:
            return _output.output(
                status=ResponseCodes.UNAUTHORIZED['authError']
            )

        else:
            self.session_db.expire(auth_token, SessionBase.AUTH_TOKEN_TTL)
            self.account_id = _account_id
            self.auth_token = auth_token
