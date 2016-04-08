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
        _validator_key = self.create_account.__name__

        try:
            # Validate user inputs
            InputValidator(_validator_key).validate(kwargs)

            # Check if account already exists
            try:
                if self.has_account(email=kwargs['email']):
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
            error_parser = InputErrorParser(_validator_key)

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )

    def update_account(self, **kwargs):
        _output = OutputManager()
        _validator_key = self.update_account.__name__
        _update_list = {}

        try:
            # Validate user inputs
            InputValidator(_validator_key).validate(kwargs)

            if 'first_name' in kwargs:
                _update_list[Account.first_name] = kwargs['first_name']

            if 'last_name' in kwargs:
                _update_list[Account.last_name] = kwargs['last_name']

            if 'password' in kwargs:
                # Hash the received password
                _update_list[Account.password] = self.__hash_password(kwargs['password'])

            if not _update_list:
                return _output.output(
                    status=ResponseCodes.BAD_REQUEST['invalidQuery']
                )

            else:
                try:
                    # Update table with new values
                    self.puppet_db.query(Account).filter(
                        Account.id == kwargs['account_id']
                    ).update(
                        _update_list
                    )

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
            error_parser = InputErrorParser(_validator_key)

            return _output.output(
                status=ResponseCodes.BAD_REQUEST['invalidQuery'],
                data=error_parser.translate_errors(e)
            )

    def has_account(self, account_id=None, email=None):
        if account_id:
            try:
                self.puppet_db.query(
                    Account.id
                ).filter(
                    Account.id == account_id
                ).one()

                return True

            except MultipleResultsFound:
                return True

            except NoResultFound:
                return False

            except SQLAlchemyError as e:
                return e

        if email:
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

    def get_account(self, account_id=None, email=None):
        if account_id:
            try:
                _account = self.puppet_db.query(
                    Account.id,
                    Account.email,
                    Account.first_name,
                    Account.last_name,
                    Account.password
                ).filter(
                    Account.id == account_id
                ).one()

                return _account
            except (NoResultFound, MultipleResultsFound, SQLAlchemyError) as e:
                return e

        if email:
            try:
                _account = self.puppet_db.query(
                    Account.id,
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
    def verify_password_hash(password, pw_hash):
        return bcrypt.hashpw(bytes(password, encoding='utf8'),
                             bytes(pw_hash, encoding='utf8')) == bytes(pw_hash, encoding='utf8')
