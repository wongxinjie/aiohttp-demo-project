import json

from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
)

from .. import utils


class UserSchema(Schema):
    id = fields.Integer(required=False)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('password')
    def validate_password(self, value):
        size = len(value)
        if size < 8 or size > 20:
            raise ValidationError(
                "password length limit:8 ~ 20 characters")

    def clean(self, kwargs):
        data, errors = self.load(kwargs)
        if errors:
            raise utils.APIException(
                utils.API_REQUIRED,
                payload={
                    "errors": errors
                }
            )

        return data

    def to_dict(self, kwargs):
        self.only = ('id', 'email')
        rv = self.dumps(kwargs).data
        return json.loads(rv)
