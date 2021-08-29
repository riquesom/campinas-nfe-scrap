from flask_marshmallow import Schema
from marshmallow.fields import Dict, Boolean


class NfeValidateSchema(Schema):
    class Meta:
        fields = ['error', 'result']

    error = Boolean()
    result = Dict()
