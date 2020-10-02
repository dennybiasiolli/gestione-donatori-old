from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import ProfiloUtente


class ProfiloUtenteAdmin(admin.ModelAdmin):
    model = ProfiloUtente
    readonly_fields = ('utente',)
    list_display = ('utente', 'is_sezione', 'is_centro_di_raccolta',
                    'is_donatore',)



class ProfiloUtenteInline(admin.StackedInline):
    model = ProfiloUtente
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfiloUtenteInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ProfiloUtente, ProfiloUtenteAdmin)
