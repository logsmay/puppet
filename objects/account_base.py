import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from voluptuous import MultipleInvalid

from models.puppet_model import Account
from objects.io.output_manager import OutputManager
from objects.io.response_codes import ResponseCodes
from objects.puppet_base import PuppetBase
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator


class AccountBase(PuppetBase):
    def __init__(self):
        super(AccountBase, self).__init__()
        self.puppet_db = self.get_db('puppet')

    def create_account(self, **kwargs):
        _output = OutputManager()

        try:
            # Validate user inputs
            input_validator = InputValidator('create_account')
            input_validator.validate(kwargs)

            # Check if account already exists
            try:
                if self.has_account(kwargs['email']):
                    return _output.output(
                        status=ResponseCodes.FORBIDDEN['accountExists'],
                        data={
                            'email': 'Email address is already associated with an existing account'
                        }
                    )
            except SQLAlchemyError:
                return _output.output(
                    status=ResponseCodes.INTERNAL_SERVER_ERROR['internalError']
                )

            # Hash the received password
            kwargs['password'] = self.__hash_password(kwargs['password'])

            try:
                # Create a new account
                _new_account = Account(**kwargs)
                self.puppet_db.add(_new_account)
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
            error_parser = InputErrorParser('create_account')

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )

    def has_account(self, email):
        try:
            self.puppet_db.query(
                Account.email
            ).filter(
                Account.email == email
            ).one()

            return True

        except MultipleResultsFound:
            return True

        except NoResultFound:
            return False

        except SQLAlchemyError as e:
            return e

    def get_account(self, email):
        try:
            _account = self.puppet_db.query(
                Account.email,
                Account.first_name,
                Account.last_name,
                Account.password
            ).filter(
                Account.email == email
            ).one()

            return _account
        except (NoResultFound, MultipleResultsFound, SQLAlchemyError) as e:
            return e

    @staticmethod
    def __hash_password(password):
        return bcrypt.hashpw(bytes(password, encoding='utf8'), bcrypt.gensalt())

    @staticmethod
    def verify_password_hash(password, hash):
        return bcrypt.hashpw(bytes(password, encoding='utf8'),
                             bytes(hash, encoding='utf8')) == bytes(hash, encoding='utf8')
