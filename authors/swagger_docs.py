from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response


# noinspection PyArgumentList
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    # noinspection PyArgumentList
    schema = coreapi.Document(
        title='Authors Haven API',
        url='localhost:8000',
        content={
            'users': {
                'create_user': coreapi.Link(
                    url='/api/v1/users/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='The name of the User.'
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='The email of the User.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The intended password of the User.'
                        )
                    ],
                    description='Create a User Account.'
                ),
                'login_user': coreapi.Link(
                    url='/api/v1/users/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='The name of the User.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The password of User.'
                        )
                    ],
                    description='Login a User.'
                ),
                'get_user': coreapi.Link(
                    url='/api/v1/user/',
                    action='GET',
                    description='Display a Users Details.',
                ),
                'update_user': coreapi.Link(
                    url='/api/v1/user/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='New name to be updated'
                        ),
                        coreapi.Field(
                            name='bio',
                            required=True,
                            location='form',
                            description='Short Description about the User.'
                        ),
                        coreapi.Field(
                            name='image',
                            required=True,
                            location='form',
                            description='The Image url of the user.'
                        )
                    ],
                    description='Update a Users Details.',
                ),

            }
        }
    )
    return response.Response(schema)
