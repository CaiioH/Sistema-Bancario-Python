from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conta, CustomUser, Transacao
from decimal import Decimal


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        endereco = request.POST.get('endereco')
        data_nasc = request.POST.get('data_nasc')
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')

        if CustomUser.objects.filter(cpf=cpf).exists():
            messages.error(request, "O CPF já está em uso.")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return redirect('signup')

        try:
            user = CustomUser(
                username=username,
                endereco=endereco,
                data_nasc=data_nasc,
                cpf=cpf,
                nome=nome
            )
            user.set_password(password)
            user.save()

            messages.success(request, "Usuário registrado com sucesso!")
            return redirect('login')

        except Exception as e:
            print(f"Erro: {e}")
            messages.error(request, f"Erro ao registrar o usuário: {e}")
            return redirect('signup')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index_usuario')
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def criar_conta(request):
    if request.method == "POST":
        saldo_inicial = Decimal(request.POST.get('saldo_inicial', 0))  # Pegar saldo inicial como Decimal

        # Verifica se o usuário já possui uma conta
        if Conta.objects.filter(usuario=request.user).exists():
            messages.error(request, "Você já possui uma conta.")
            return redirect('index_usuario')

        # Cria a nova conta
        Conta.objects.create(usuario=request.user, saldo=saldo_inicial)
        messages.success(request, "Conta criada com sucesso!")
        return redirect('index_usuario')

    return render(request, 'criar_conta.html')


@login_required
def index_usuario(request):
    contas = Conta.objects.filter(usuario=request.user)
    return render(request, 'index_usuario.html', {'contas': contas})


@login_required
def transacao(request):
    if request.method == 'POST':
        conta_id = request.POST.get('conta_id')  # Obtém o número da conta
        tipo_transacao = request.POST.get('tipo_transacao')
        valor = Decimal(request.POST.get('valor'))

        # Validação de valor numérico
        try:
            valor = float(valor)
            if valor <= 0:
                messages.error(request, "O valor deve ser maior que zero.")
                return redirect('index_usuario')
        except ValueError:
            messages.error(request, "Insira um valor válido.")
            return redirect('index_usuario')

        try:
            # Procurando a conta pelo número da conta
            conta = Conta.objects.get(numero_conta=conta_id, usuario=request.user)

            if tipo_transacao == 'deposito':
                conta.depositar(valor)
                messages.success(request, "Depósito realizado com sucesso!")
            elif tipo_transacao == 'saque':
                try:
                    conta.sacar(valor)
                    messages.success(request, "Saque realizado com sucesso!")
                except ValueError as e:
                    messages.error(request, str(e))
            return redirect('index_usuario')

        except Conta.DoesNotExist:
            messages.error(request, 'Conta não encontrada ou não pertencente ao usuário.')
            return redirect('index_usuario')

    return redirect('index_usuario')


@login_required
def extrato_view(request):
    conta = Conta.objects.filter(usuario=request.user).first()
    transacoes = conta.extrato() if conta else []
    return render(request, 'extrato.html', {'transacoes': transacoes, 'conta': conta})
