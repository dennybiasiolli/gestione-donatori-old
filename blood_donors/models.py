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
