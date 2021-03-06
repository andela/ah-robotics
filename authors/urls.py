"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:
    url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function:
    from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from .swagger_docs import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('authors.apps.authentication.urls',
                             'authentication'), namespace='authentication')),
    path('api/v1/docs/', schema_view),
    path('api/v1/', include(('authors.apps.profiles.urls',
                             'profile'), namespace='profiles')),
    path('api/v1/', include(('authors.apps.articles.urls',
                             'articles'), namespace='articles')),
    path('api/v1/', include(('authors.apps.rating.urls',
                             'rating'), namespace='rating')),
    path('api/v1/', include(('authors.apps.comments.urls',
                             'comments'), namespace='comments')),
    path('api/v1/', include(('authors.apps.favorites.urls',
                             'favorites'), namespace='favorites')),
    path('api/v1/', include(('authors.apps.bookmark.urls',
                             'bookmark'), namespace='bookmark')),
    path('api/v1/', include(('authors.apps.followers.urls', 
                            'followers'), namespace='followers'))
]
