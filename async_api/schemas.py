from marshmallow import Schema, fields, validate

from settings import MAX_LIMIT


class PostSchema(Schema):
    external_id = fields.Int(data_key='id')
    title = fields.Str()
    url = fields.URL()
    created = fields.DateTime(format='iso8601')


posts_schema = PostSchema(many=True)

output_fields = [
    'id',
    'title',
    'url',
    'created',
]
order_choices = (
    output_fields
    + list(map(lambda x: '-' + x, output_fields))
)


class PostsInputParamsSchema(Schema):
    order = fields.Method(deserialize='load_order', validate=validate.OneOf(order_choices))
    offset = fields.Int(validate=validate.Range(min=0))
    limit = fields.Int(validate=validate.Range(min=0, max=MAX_LIMIT))

    def load_order(self, value):
        if value in ['id', '-id']:
            reverse = value[0] if value[0] == '-' else ''
            return f'{reverse}external_id'
        return value


posts_request_schema = PostsInputParamsSchema()
