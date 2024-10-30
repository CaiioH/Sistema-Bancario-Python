from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class CustomUser(AbstractUser):
    endereco = models.CharField(max_length=255)
    data_nasc = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=11, unique=True)  # CPF deve ser único
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} Profile'


class Conta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Permite várias contas para o mesmo usuário
    agencia = '0001'
    numero_conta = models.AutoField(primary_key=True, verbose_name='Número da Conta (C/C)') 
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')


    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero_conta}
            Titular:\t{self.usuario.username}
        """ 

    def depositar(self, valor):
        valor = Decimal(valor)
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self.saldo += valor
        self.save()
        Transacao.objects.create(conta=self, tipo='DEPOSITO', valor=valor)

    def sacar(self, valor):
        valor = Decimal(valor)
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para saque.")
        self.saldo -= valor
        self.save()
        Transacao.objects.create(conta=self, tipo='SAQUE', valor=valor)

    def extrato(self):
        return Transacao.objects.filter(conta=self).order_by('-data_transacao')


class Transacao(models.Model):
    TIPOS_TRANSACAO = [
        ('SAQUE', 'Saque'),
        ('DEPOSITO', 'Depósito'),
    ]
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    tipo = models.CharField(max_length=10, choices=TIPOS_TRANSACAO)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_transacao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Transação')

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.valor} em {self.data_transacao.strftime('%d/%m/%Y %H:%M')}"
