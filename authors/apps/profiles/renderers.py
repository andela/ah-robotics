import json

from rest_framework.renderers import JSONRenderer


class ProfilesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render User Profile
        """
        errors = data.get('errors', None)
        if errors is not None:
            return JSONRenderer(data)

        return json.dumps(data)
