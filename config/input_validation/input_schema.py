from voluptuous import Schema, Required, All, Length

from config.input_validation.input_validators import InputValidators


class InputSchema(object):
    def __init__(self):
        self.create_account = Schema({
            Required('email'): All(InputValidators.email()),
            Required('first_name'): All(str, Length(min=2)),
            Required('last_name'): All(str, Length(min=2)),
            Required('password'): All(str, Length(min=8))
        })

        self.create_session = Schema({
            Required('email'): All(InputValidators.email()),
            Required('password'): All(str)
        })

        self.delete_session = Schema({
            Required('auth_token'): All(str, Length(min=1))
        })
