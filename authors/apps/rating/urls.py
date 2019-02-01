from django.urls import path
from .views import RatingAPIView

app_name="rating"

urlpatterns = [
    path('rate/<slug>/', RatingAPIView.as_view(), name='rating')
]
