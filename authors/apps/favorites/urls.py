from django.urls import path

from authors.apps.favorites import views

app_name = "favorites"

urlpatterns = [
    path('favorites/', views.ListCreateFavorite.as_view(), name='favorites'),
    path('favorites/<slug>/', views.DeleteFavorite.as_view(),
         name='favorites-delete'),
]
