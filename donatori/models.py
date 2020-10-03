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


class StatoDonatore(models.Model):
    utente = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=255, unique=True)
    is_attivo = models.BooleanField(default=True)
    codice = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Stato donatore'
        verbose_name_plural = 'Stati donatore'

    def __str__(self):
        return self.descrizione_estesa


class Donatore(models.Model):
    MAN = 'M'
    WOMAN = 'F'
    SEX_CHOICES = (
        (MAN, 'Maschio'),
        (WOMAN, 'Femmina'),
    )
    sezione = models.ForeignKey('Sezione', on_delete=models.CASCADE)
    num_tessera = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    sesso = models.CharField(max_length=2, choices=SEX_CHOICES)
    stato_donatore = models.ForeignKey(StatoDonatore, on_delete=models.CASCADE)
    num_tessera_cartacea = models.CharField(max_length=255, blank=True)
    data_rilascio_tessera = models.DateField(null=True, blank=True)
    codice_fiscale = models.CharField(max_length=255, blank=True)
    data_nascita = models.DateField(null=True, blank=True)
    data_iscrizione = models.DateField(null=True, blank=True)
    gruppo_sanguigno = models.CharField(max_length=10)
    rh = models.CharField(max_length=10)
    fenotipo = models.CharField(max_length=10, blank=True)
    kell = models.CharField(max_length=10, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    frazione = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    citta = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    tel_lavoro = models.CharField(max_length=255, blank=True)
    cell = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    fermo_per_malattia = models.BooleanField(default=False)
    donazioni_pregresse = models.IntegerField(default=0)
    num_benemerenze = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Donatore'
        verbose_name_plural = 'Donatori'
        unique_together = ('sezione', 'num_tessera',)

    def __str__(self):
        return self.num_tessera.upper() + ' ' + self.cognome.upper() + ' ' + self.nome.upper()
