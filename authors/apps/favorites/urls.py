from django.urls import path

from authors.apps.favorites import views

app_name = "favorites"

urlpatterns = [
    path('favorites/', views.ListAllFavorites.as_view(),
         name='user-favorites'),
    path('articles/<slug>/favorite',
         views.FavouritesView.as_view(), name="user-favorite"),
]
