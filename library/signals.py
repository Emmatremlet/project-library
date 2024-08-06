from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Member

@receiver(user_logged_in)
def activate_member(sender, user, request, **kwargs):
    if isinstance(user, Member): 
        user.is_active = True
        user.save()

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if isinstance(user, Member):
        # user.is_active = False
        user.save()
