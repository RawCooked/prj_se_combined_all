# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings

# @receiver(post_save, sender=User)
# def notify_admin_on_signup(sender, instance, created, **kwargs):
#     if created:  # Vérifie que l'utilisateur est nouvellement créé
#         send_mail(
#             'Nouvel utilisateur inscrit',
#             f'Un nouvel utilisateur s\'est inscrit : {instance.username} ({instance.email}).',
#             settings.DEFAULT_FROM_EMAIL,  # Email de l'expéditeur (configuré dans settings.py)
#             [admin_email for admin_email in settings.ADMINS],  # Liste des administrateurs
#             fail_silently=False,
#         )