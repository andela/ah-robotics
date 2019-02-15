from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_email(request, details, token, subject):
    current_site = get_current_site(request)
    verification_link = "http://" + current_site.domain + \
        '/verify/{}'.format(token)
    subject = subject
    message = render_to_string('email_verification.html', {
        'verification_link': verification_link,
        'title': subject,
        'username': details['username']
    })
    body_content = strip_tags(message)
    msg = EmailMultiAlternatives(
        subject, body_content, to=[
            details['email']])
    msg.attach_alternative(message, "text/html")
    msg.send()
