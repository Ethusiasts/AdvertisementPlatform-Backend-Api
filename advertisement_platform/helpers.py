from django.conf import settings
from django.core.mail import send_mail


roles = ["ADMIN", "CUSTOMER", "EMPLOYEE", "LANDOWNER"]


def valid_role(role):
    if role.isalpha() and role.upper() in roles:
        return True
    return False


def find_role(role):
    for r in roles:
        if r == role.upper():
            return r


def send_email(subject, content, email, link):
    send_mail(
        subject,
        f'{content}: {link}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
