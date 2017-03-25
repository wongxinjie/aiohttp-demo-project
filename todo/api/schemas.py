import json

from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError
)

from .. import utils
from .models import Status


class TodoSchema(Schema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=False)
    content = fields.String(required=True)
    created_at = fields.DateTime(required=False)
    status = fields.Integer(required=False)

    @validates('content')
    def validate_content(self, value):
        length = len(value)
        if length == 0 or length > 512:
            raise ValidationError(
                "content to short or to long(max length is 512")

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

    def to_dict(self, kwargs, many=False):
        self.only = ('id', 'content', 'created_at', 'status')
        if many:
            self.many = True

        rv = self.dumps(kwargs).data
        return json.loads(rv)

    def clean_status(self, value):
        choices = [e.value for e in Status]
        try:
            status = int(value)
            if status not in choices:
                raise ValidationError()
        except:
            raise utils.APIException(
                utils.API_BAD_REQUEST
            )

        return status
