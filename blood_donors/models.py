from datetime import datetime
from django.db import models


class Sezione(models.Model):
    owner = models.ForeignKey('auth.User')
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
    owner = models.ForeignKey('auth.User')
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
