from flask_marshmallow import Schema
from marshmallow.fields import Str


class RateSchema(Schema):
    class Meta:
        fields = ["day", "price"]

    message = Str()
