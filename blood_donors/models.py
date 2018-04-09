from datetime import datetime
from django.db import models


class Sezione(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=255)
    indirizzo = models.CharField(max_length=255, blank=True)
    frazione = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    citta = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Sezioni"
        unique_together = ('owner', 'descrizione',)

    def __str__(self):
        return self.descrizione


class CentroDiRaccolta(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=255)
    indirizzo = models.CharField(max_length=255, blank=True)
    frazione = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    citta = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "CentriDiRaccolta"
        unique_together = ('owner', 'descrizione',)

    def __str__(self):
        return self.descrizione


class Sesso(models.Model):
    descrizione = models.CharField(unique=True, max_length=255)
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
        verbose_name_plural = "Sessi"

    def __str__(self):
        return self.descrizione


class StatoDonatore(models.Model):
    descrizione = models.CharField(unique=True, max_length=255)
    descrizione_estesa = models.CharField(unique=True, max_length=255)
    is_attivo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "StatiDonatore"

    def __str__(self):
        return self.descrizione_estesa


class TipoDonazione(models.Model):
    descrizione = models.CharField(unique=True, max_length=255)

    class Meta:
        verbose_name_plural = "TipiDonazione"

    def __str__(self):
        return self.descrizione


class Donatore(models.Model):
    sezione = models.ForeignKey('Sezione', on_delete=models.CASCADE)
    num_tessera = models.CharField(max_length=255)
    num_tessera_cartacea = models.CharField(max_length=255, blank=True)
    data_rilascio_tessera = models.DateField(null=True, blank=True)
    cognome = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    codice_fiscale = models.CharField(max_length=255, blank=True)
    sesso = models.ForeignKey('Sesso', on_delete=models.CASCADE)
    data_nascita = models.DateField(null=True, blank=True)
    data_iscrizione = models.DateField(null=True, blank=True)
    stato_donatore = models.ForeignKey(
        'StatoDonatore', on_delete=models.CASCADE)
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
    centro_raccolta_default = models.ForeignKey(
        'CentroDiRaccolta', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Donatori"
        unique_together = ('sezione', 'num_tessera',)

    def __str__(self):
        return self.num_tessera.upper() + ' ' + self.cognome.upper() + ' ' + self.nome.upper()


class Donazione(models.Model):
    donatore = models.ForeignKey('Donatore', on_delete=models.CASCADE)
    data = models.DateField()
    tipo_donazione = models.ForeignKey(
        'TipoDonazione', on_delete=models.CASCADE)
    centro_di_raccolta = models.ForeignKey(
        'CentroDiRaccolta', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Donazioni"

    def __str__(self):
        return self.donatore + ' - ' + self.data + ' - ' + self.tipo_donazione
