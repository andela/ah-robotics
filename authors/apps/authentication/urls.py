from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ForgotPasswordAPIview, ResetPasswordAPIView, VerifyAPIView,
    ResendAPIView
)

app_name = 'authentication'
urlpatterns = [
    path(
        'user/',
        UserRetrieveUpdateAPIView.as_view()),
    path(
        'users/',
        RegistrationAPIView.as_view(),
        name="register_url"),
    path(
        'users/login/',
        LoginAPIView.as_view(),
        name="login_url"),
    path(
        'account/forgot_password/',
        ForgotPasswordAPIview.as_view(),
        name="forgot_password"),
    path(
        'account/reset_password/<token>',
        ResetPasswordAPIView.as_view(),
        name="reset_password"),
    path(
        'users/verify/<token>',
        VerifyAPIView.as_view(),
        name="verify_url"),
    path(
        'user/',
        UserRetrieveUpdateAPIView.as_view()),
    path(
        'users/',
        RegistrationAPIView.as_view(),
        name="register_url"),
    path(
        'users/login/',
        LoginAPIView.as_view(),
        name="login_url"),
    path(
        'users/verify/<token>',
        VerifyAPIView.as_view(),
        name="verify_url"),
    path(
        'users/resend-email/',
        ResendAPIView.as_view(),
        name="resend_email_url"),
    path(
        'account/forgot_password/',
        ForgotPasswordAPIview.as_view(),
        name="forgot_password"),
    path(
        'account/reset_password/<token>',
        ResetPasswordAPIView.as_view(),
        name="reset_password"),
]
