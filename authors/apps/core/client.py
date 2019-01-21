import os
from django.contrib.sites.shortcuts import get_current_site


def get_domain():
    return os.getenv('CLIENT_DOMAIN', '')


def get_password_reset_link(request, token):
    '''
    :param:client_url for front-end application
    :param:token :
    '''
    """
    client_url refers to the front-end application reset url
    e.g http://ah-robotics/front-end/reset-password

    """
    domain = get_current_site(request).domain
    return 'http://{}/api/v1/account/reset_password/{}'.format(domain, token)
