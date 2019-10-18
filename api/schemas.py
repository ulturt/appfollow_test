from marshmallow import fields, Schema


class PostSchema(Schema):
    external_id = fields.Int(data_key='id')
    title = fields.Str()
    url = fields.URL()
    created = fields.DateTime()


PostsSchema = PostSchema(many=True)
