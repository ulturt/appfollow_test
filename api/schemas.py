import itertools

from marshmallow import fields, Schema, validate

from settings import DEFAULT_OFFSET, DEFAULT_LIMIT, MAX_LIMIT


class PostSchema(Schema):
    external_id = fields.Int(data_key='id')
    title = fields.Str()
    url = fields.URL()
    created = fields.DateTime(format='iso8601')


PostsSchema = PostSchema(many=True)


output_fields = [
    field.data_key or field.name
    for field in PostsSchema.fields.values()
]
order_choices = list(
    f'{a}{b}'
    for a, b in itertools.product(['', '-'], output_fields)
)


class PostsInputParamsSchema(Schema):
    action = fields.Str(validate=validate.OneOf(['parse']))
    order = fields.Method(deserialize='load_order', validate=validate.OneOf(order_choices))
    offset = fields.Int(default=DEFAULT_OFFSET, validate=validate.Range(min=0))
    limit = fields.Int(default=DEFAULT_LIMIT, validate=validate.Range(min=0, max=MAX_LIMIT))

    def load_order(self, value):
        if value in ['id', '-id']:
            reverse = value[0] if value[0] == '-' else ''
            return f'{reverse}external_id'
        return value


RequestArgsSchema = PostsInputParamsSchema()
