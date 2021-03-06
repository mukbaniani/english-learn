from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .tokens import encode_reset_token


class Mail:
    @staticmethod
    def send_verify_email_token(to, user, request) -> None:
        current_site = get_current_site(request)
        verify_token = default_token_generator.make_token(user)
        send_mail(
            'verify email',
            f'verify your email account click here {current_site}/api/user/{user.id}/{verify_token}',
            f'{settings.EMAIL_HOST_USER}',
            [to],
            fail_silently=False,
        )

    @staticmethod
    def send_password_reset_token(to, user, request):
        current_site = get_current_site(request)
        send_mail(
            'reset password',
            f'click here to reset your password {current_site.domain}/api/user/update-reset-password/{encode_reset_token(user)}',
            f'{settings.EMAIL_HOST_USER}',
            [f'{to}'],
            fail_silently=False,
        )
