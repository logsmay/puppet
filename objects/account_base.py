import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from voluptuous import MultipleInvalid

from models.puppet_model import Account
from objects.io.output_manager import OutputManager
from objects.puppet_base import PuppetBase
from utils.input_validation.input_error_parser import InputErrorParser
from utils.input_validation.input_validator import InputValidator
from objects.io.response_codes import ResponseCodes


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
            if self.has_account(kwargs['email']):
                return _output.output(
                    status=ResponseCodes.FORBIDDEN['accountExists'],
                    data={
                        'email': 'Email address is already associated with an existing account'
                    }
                )

            # Hash the received password
            kwargs['password'] = bcrypt.hashpw(bytes(kwargs['password'], encoding='utf8'), bcrypt.gensalt())

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
        _count = self.puppet_db.query(
            Account.email
        ).filter(
            Account.email == email
        ).limit(1).all()

        return True if len(_count) > 0 else False
