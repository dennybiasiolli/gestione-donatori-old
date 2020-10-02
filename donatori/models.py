from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfiloUtente(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sezione = models.BooleanField(
        default=False, verbose_name='Sezione')
    is_centro_di_raccolta = models.BooleanField(
        default=False, verbose_name='Centro di raccolta')
    is_donatore = models.BooleanField(
        default=False, verbose_name='Donatore')

    class Meta:
        verbose_name = 'Profilo utente'
        verbose_name_plural = 'Profili utenti'

    def __str__(self):
        return self.utente.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and ProfiloUtente.objects.filter(pk=instance.id).first() is None:
        ProfiloUtente.objects.create(utente=instance)
    instance.profiloutente.save()


class Sezione(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=255, unique=True)
    ragione_sociale = models.CharField(max_length=255, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    frazione = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    citta = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    presidente = models.CharField(max_length=255, blank=True)
    segretario = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Sezione'
        verbose_name_plural = 'Sezioni'

    def __str__(self):
        return self.descrizione
