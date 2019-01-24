from rest_framework.renderers import JSONRenderer
import json


class ProfilesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # collect errors on the data
        errors = data.get('errors', None)
        if errors is not None:
            # handle the errors with JSONRenderer
            return JSONRenderer(data)
        return json.dumps(data)
