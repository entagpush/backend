# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings

# from customer.models import ArtistApplication


# @receiver(post_save, sender=ArtistApplication)
# def application_notification(sender, instance, created, **kwargs):
#     if created:
#         subject = "New Artist Application Received"
#         message = (
#             f"An application has been received from {instance.name}. Please review it."
#         )
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
