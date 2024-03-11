from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_admin_invitation_email(invitation):
    invite_link = settings.FRONTEND_ADMIN_URL + reverse(
        "accept_invitation", kwargs={"code": invitation.code}
    )
    subject = "You are invited to join as an admin!"
    message = f"Please use the following link to accept your invitation: {invite_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [invitation.email])
