import json

from rest_framework import renderers


class FavoriteJsonRenderer(renderers.BaseRenderer):
    """
    Renders a list of article favorites
    """
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None,
               renderer_context=None):
        """
        Render a list of article favorites
        """
        if isinstance(data, list):
            return json.dumps(
                {'favorites': data})
        else:
            """
            Render a single favorite or an error message
            """
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})

            return json.dumps({'favorite': data})
