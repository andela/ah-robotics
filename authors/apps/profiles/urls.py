from django.urls import path
from .views import ProfileListView, ProfileItemView

app_name = 'profiles'

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles/<str:username>/', ProfileItemView.as_view(),
         name='specific_profile')
]
