from django.contrib import admin
from contas.models import Conta, Transacao
from .models import CustomUser  # Importe o CustomUser

class ContaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'agencia', 'numero_conta', 'saldo', 'data_criacao')
    list_filter = ('usuario', 'data_criacao',)

class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'conta', 'valor', 'data_transacao')
    list_filter = ('tipo', 'conta', 'valor', 'data_transacao',)

# Registre o CustomUser com o admin do Django
admin.site.register(CustomUser)
admin.site.register(Conta, ContaAdmin)
admin.site.register(Transacao, TransacaoAdmin)
