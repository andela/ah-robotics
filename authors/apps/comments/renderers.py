from rest_framework.renderers import JSONRenderer
import json


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'comment': data
        })
