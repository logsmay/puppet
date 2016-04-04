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

        self.create_sesssion = Schema({
            Required('email'): All(InputValidators.email()),
            Required('password'): All(str)
        })