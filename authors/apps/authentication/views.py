import jwt
import os
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.apps.core import client
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)

from authors.settings import SECRET_KEY
from .models import User
from .utils import send_email


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """Register a new User"""
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = serializer.data['email']
        username = serializer.data['username']
        token = serializer.data['token']
        subject = "Verification email"

        details = {
            'email': email,
            'username': username
        }
        send_email(request, details, token, subject)

        response_message = {
            "message": "User registered successfully. Check your email to activate your account.",
            "user_info": serializer.data}

        return Response(response_message, status=status.HTTP_201_CREATED)


class VerifyAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, token):
        try:
            email = jwt.decode(token, SECRET_KEY)['email']
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response(
                    "Email already verified.",
                    status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            return Response(
                "Email verification successful.",
                status=status.HTTP_200_OK)
        except Exception:
            return Response(
                "Token has expired.",
                status=status.HTTP_403_FORBIDDEN)


class ResendAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data.get('user', {})

        email = user['email']
        user_retrieve = User.objects.get(email=email)
        username = user_retrieve.username
        details = {
            'email': email,
            'username': username
        }
        token = jwt.encode({
            'email': email
        }, settings.SECRET_KEY).decode()
        subject = "Resend verification"
        if user_retrieve.is_verified:
            return Response(
                {
                    "message": "User already verified."
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            send_email(request, details, token, subject)
            return Response({
                "message": "Verification email resent successfully."
            }, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Login using User Credentials"""
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Get details of a User"""
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Update a User"""
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordAPIview(APIView):
    """
    This view captures user email and
    sends password reset link to user email if the user with email exists
    The reset link contains the client url(front-end password reset url)
    and a jwt token as an argument
    """

    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        client_url = request.data.get('client_url')
        user = User.objects.filter(email=email).first()

        if user is None:
            msg = {'Account with the email does not exist.'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        """
        type is added to the payload to ensure login tokens are not used
        to reset the password
        """
        # Generate token by encoding user email and reset type
        token = jwt.encode({
            'email': email,
            'type': 'reset password',
        },
            settings.SECRET_KEY
        ).decode('utf-8')

        reset_link = client.get_password_reset_link(request, token)

        subject = "Password reset link"
        from_email = os.getenv('EMAIL_HOST_USER')
        from_email, to_email, subject = from_email, email, subject
        # render password reset template with a dynamic value
        html = render_to_string('password_reset_template.html', {
                                'reset_password_link': reset_link})
        # strip html tags from the html content
        text_content = strip_tags(html)

        # create an email and attach content as html
        mail = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        mail.attach_alternative(html, "text/html")
        mail.send()

        response = {
            "message": "Kindly use the link sent to your email to reset your password"}

        return Response(response, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """
    This view updates user password and sends a success email to the user
    The view captures jwt token, password and confirm password
    """
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        token = self.kwargs.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            if e.__class__.__name__ == 'ExpiredSignatureError':
                raise exceptions.AuthenticationFailed('Token has expired')
            elif e.__class__.__name__ == 'DecodeError':
                raise exceptions.AuthenticationFailed(
                    'Cannot decode the given token')
            else:
                raise exceptions.AuthenticationFailed(str(e))
        reset_type = payload.get('type', '')
        # check the reset type
        if reset_type != 'reset password':
            response = {"message": "Something went wrong try again"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if data.get('password') != data.get('confirm_password'):
            response = {"message": "Passwords do not match"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        # get user by email
        user = User.objects.filter(email=payload.get('email')).first()
        user.set_password(data.get('password'))
        user.save()

        subject = "Password reset notification"
        email = payload.get('email')
        from_email = os.getenv('EMAIL_HOST_USER')
        from_email, to_email, subject = from_email, email, subject
        # render password reset  done template
        html = render_to_string('reset_password_done_template.html')
        # strip html tags from the html content
        text_content = strip_tags(html)
        # create an email and attach content as html
        mail = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        mail.attach_alternative(html, "text/html")
        mail.send()
        response = {"message": "Password updated successfully"}
        return Response(response, status=status.HTTP_200_OK)
