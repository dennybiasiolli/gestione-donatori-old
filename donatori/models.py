from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


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


class Sesso(models.Model):
    codice = models.CharField(max_length=1, unique=True)
    descrizione = models.CharField(max_length=255)
    gg_da_sangue_a_sangue = models.IntegerField()
    gg_da_sangue_a_plasma = models.IntegerField()
    gg_da_sangue_a_piastrine = models.IntegerField()
    gg_da_plasma_a_sangue = models.IntegerField()
    gg_da_plasma_a_plasma = models.IntegerField()
    gg_da_plasma_a_piastrine = models.IntegerField()
    gg_da_piastrine_a_sangue = models.IntegerField()
    gg_da_piastrine_a_plasma = models.IntegerField()
    gg_da_piastrine_a_piastrine = models.IntegerField()

    class Meta:
        verbose_name = 'Sesso'
        verbose_name_plural = 'Sessi'

    def __str__(self):
        return self.descrizione


class StatoDonatore(models.Model):
    utente = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.CASCADE)
    codice = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=True)
    is_attivo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Stato donatore'
        verbose_name_plural = 'Stati donatore'
        unique_together = ('utente', 'codice',)

    def __str__(self):
        return self.descrizione


class Donatore(models.Model):
    sezione = models.ForeignKey(Sezione, on_delete=models.CASCADE)
    num_tessera = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    sesso = models.ForeignKey(Sesso, on_delete=models.CASCADE)
    stato_donatore = models.ForeignKey(StatoDonatore, on_delete=models.CASCADE)
    num_tessera_cartacea = models.CharField(max_length=255, blank=True)
    data_rilascio_tessera = models.DateField(null=True, blank=True)
    codice_fiscale = models.CharField(max_length=255, blank=True)
    data_nascita = models.DateField(null=True, blank=True)
    data_iscrizione = models.DateField(null=True, blank=True)
    gruppo_sanguigno = models.CharField(max_length=10, blank=True)
    rh = models.CharField(max_length=10, blank=True)
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
        return '{} - {} {}'.format(self.num_tessera, self.cognome, self.nome)


class Donazione(models.Model):
    SANGUE_INTERO = 1
    PLASMA = 2
    PIASTRINE = 3
    TIPO_DONAZIONE_CHOICES = [
        (SANGUE_INTERO, 'Sangue intero'),
        (PLASMA, 'Plasma'),
        (PIASTRINE, 'Piastrine'),
    ]
    donatore = models.ForeignKey(Donatore, on_delete=models.CASCADE)
    tipo_donazione = models.IntegerField(
        choices=TIPO_DONAZIONE_CHOICES,
        default=SANGUE_INTERO,
    )
    data_donazione = models.DateField(default=date.today)

    class Meta:
        verbose_name = 'Donazione'
        verbose_name_plural = 'Donazioni'
        unique_together = ('donatore', 'data_donazione',)

    def __str__(self):
        return '{} - {} {}'.format(
            self.data_donazione, self.donatore.cognome, self.donatore.nome)
