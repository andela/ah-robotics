from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ForgotPasswordAPIview, ResetPasswordAPIView
)

app_name = 'authentication'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="register_url"),
    path('users/login/', LoginAPIView.as_view(), name="login_url"),
    path('account/forgot_password/', ForgotPasswordAPIview.as_view(), name="forgot_password"),
    path('account/reset_password/<token>', ResetPasswordAPIView.as_view(), name="reset_password"),
]
