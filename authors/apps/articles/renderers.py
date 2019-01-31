import json

from rest_framework import renderers


class ArticleJsonRenderer(renderers.BaseRenderer):
    """
    Renders a list of articles or a single instance of an article
    """
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None,
               renderer_context=None):
        """
        Render a list of articles
        """
        if 'count' in data.keys():
            return json.dumps(data)
        else:
            """
            Render a single article or an error message
            """
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})

            return json.dumps({'article': data})
