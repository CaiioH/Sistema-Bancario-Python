from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser  # Importe o CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Não é necessário criar um perfil, pois as informações adicionais estão no CustomUser
        pass

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Não é necessário salvar um perfil, pois as informações estão diretamente no CustomUser
    pass
