from rest_framework import renderers
import json


class ArticleJsonRenderer(renderers.BaseRenderer):
    """
    Renders a list of articles or a single instance of an article
    """
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None,
               renderer_context=None):
        # display a list of articles
        if isinstance(data, list):
            return json.dumps(
                {'articles': data})
        else:
            # triggered if result is an error
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})
            # display single article details
            return json.dumps({'article': data})
