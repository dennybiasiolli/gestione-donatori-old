from django.contrib import admin

from .models import (
    Sezione, CentroDiRaccolta, Sesso, StatoDonatore, TipoDonazione, Donatore,
    Donazione
)


class SezioneAdmin(admin.ModelAdmin):

    # impostiamo come default l'utente corrente
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id
        return super(SezioneAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CentroDiRaccoltaAdmin(admin.ModelAdmin):

    # impostiamo come default l'utente corrente
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id
        return super(CentroDiRaccoltaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class StatoDonatoreAdmin(admin.ModelAdmin):

    # impostiamo come default l'utente corrente
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id
        return super(StatoDonatoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DonatoreAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sezione':
            # if not request.user.is_superuser:
                kwargs['queryset'] = Sezione.objects.filter(owner=request.user)
                if kwargs['queryset'].count() == 1:
                    kwargs['initial'] = kwargs['queryset'].first()
            # kwargs['queryset'] = Sezione.objects.filter(owner=request.user)
        return super(DonatoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DonazioneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'donatore':
            # if not request.user.is_superuser:
            kwargs['queryset'] = Donatore.objects.filter(sezione__owner=request.user)
        return super(DonazioneAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Sezione, SezioneAdmin)
admin.site.register(CentroDiRaccolta, CentroDiRaccoltaAdmin)
admin.site.register(Sesso)
admin.site.register(StatoDonatore, StatoDonatoreAdmin)
admin.site.register(TipoDonazione)
admin.site.register(Donatore, DonatoreAdmin)
admin.site.register(Donazione, DonazioneAdmin)
