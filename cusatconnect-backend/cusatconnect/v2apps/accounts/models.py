from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.validators import RegexValidator

from django_rest_passwordreset.signals import reset_password_token_created

from rest_framework.authtoken.models import Token

from .managers import UserManager
from v2apps.departments.models import Stream, Department


class User(AbstractUser):

    username = models.CharField(blank=True, max_length=20)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('Email address'), unique=True,
                              error_messages={'unique': 'A user with that email already exists.'},
                              blank=True
                              )
    password = models.CharField(_('Password'), max_length=100, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    phone_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
                                 message="Enter a valid phone number")
    mobile_number = models.CharField(validators=[phone_regex], max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        else:
            return self.email


class ExpiringToken(Token):

    class Meta(object):
        proxy = True

    def expired(self):

        now = timezone.now()
        return self.created < now - settings.EXPIRING_TOKEN_LIFESPAN


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Cusatconnect"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@cusatconnect",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
