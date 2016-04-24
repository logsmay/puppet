from voluptuous import Schema, Optional, Required, All, Length, Match

from config.input_validation.input_validators import InputValidators


class InputSchema(object):
    def __init__(self):
        # ## Account ## #

        self.create_account = Schema({
            Required('email'): InputValidators.email(),
            Required('first_name'): All(str, Length(min=2)),
            Required('last_name'): All(str, Length(min=2)),
            Required('password'): All(str, Length(min=8))
        })

        self.update_account = Schema({
            Optional('email'): InputValidators.email(),
            Optional('first_name'): All(str, Length(min=2)),
            Optional('last_name'): All(str, Length(min=2)),
            Optional('password'): All(str, Length(min=8))
        })

        self.create_session = Schema({
            Required('email'): InputValidators.email(),
            Required('password'): str
        })

        self.create_shipper = Schema({
            Required('name'): str,
            Required('description'): str,
            Required('address'): [
                {
                    Optional('organization_name'): str,
                    Optional('unit'): str,
                    Optional('sub_premise'): str,
                    Optional('premise'): str,
                    Optional('thoroughfare'): str,
                    Optional('postal_code'): str,
                    Optional('dependent_locality'): str,
                    Optional('locality'): str,
                    Optional('sub_administrative_area'): str,
                    Optional('administrative_area'): str,
                    Required('country'): All(str, Length(min=2, max=2)),
                    Optional('geocode'): {
                        Required('latitude'): float,
                        Required('longitude'): float,
                        Required('accuracy'): int
                    },
                    Required("contact"): [
                        {
                            Required("email"): All(InputValidators.email()),
                            Required("first_name"): str,
                            Required("last_name"): str,
                            Required("phone_country"): All(str, Length(min=2, max=2)),
                            Required("phone_number"): int,
                            Optional("phone_extension"): int
                        }
                    ],
                    Required("dispatch_time"): [
                        {
                            Required("start_time"): Match('^(2[0-3]|[01][0-9]):?([0-5][0-9]):?([0-5][0-9])$'),
                            Required("end_time"): Match('^(2[0-3]|[01][0-9]):?([0-5][0-9]):?([0-5][0-9])$')
                        }
                    ]
                }
            ]
        })
