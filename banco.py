import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# [CONTA] 
class Conta: 
    def __init__(self, numero, cliente): #algumas informações de conta
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001" #agencia
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero): #aqui define um metodo de classe que serve para criar uma conta nova
        return cls(numero, cliente)   
        
    @property #aqui serve pra eu conseguir ter acesso ao "self._saldo" por exemplo, usando "Conta.saldo".
    def saldo(self): #para ter acesso ao saldo da conta
        return self._saldo
    #Pois por boas praticas o "_" antes de uma variavel serve para indicar que não pode ser modificada.
    #Porém eu poderia descartar isso já que não tem mais nenhuma função alem do acesso dela.
    #Mas nesse caso faz parte do desafio para treinar e colocar em pratica o uso de "@property".
    
    @property
    def numero(self): #para ter acesso ao numero da conta
        return self._numero

    @property
    def cliente(self): #para ter acesso ao cliente e suas informações
        return self._cliente
    
    @property
    def agencia(self): #para ter acesso ao numero da agencia
        return self._agencia
    
    @property
    def historico(self): #para ter acesso ao "extrato"
        return self._historico
    
    def sacar(self, valor): #Aqui executa o saque da conta
        # aqui eu posso definir toda a logica para ver se existe algum valor
        #a ser sacado. Se não existir, negar e mostrar a mensagem.
        # Se existir, executar o saque e returnar True 
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print('\n&@⁈ Saldo insuficiente para realizar o saque. &@⁈')     

        elif valor > 0:  
            self._saldo -= valor
            print('\n——————— SAQUE EFETUADO COM SUCESSO! ———————')        
            return True    
        else:
            print("\n&@⁈ Operação falhou! O valor informado é inválido. &@⁈")
    
        return False  
    
    def depositar(self, valor): # Aqui executa o deposito na conta
        if valor > 0:
            self._saldo += valor
            print('\n——————— DEPÓSITO FEITO COM SUCESSO! ———————') 
        
        else:
            print("\n&@⁈ Operação falhou! O valor informado é inválido. &@⁈")
            return False
        
        return True
        
class ContaCorrente(Conta): #Contém os limites de saques da Conta Corrente
    def __init__(self, numero, cliente, limite=500, limite_saques=3): #**kw serve pra referenciar tudo da classe PAI
        self._limite = limite # valor limite de saques por operação
        self._limite_saques = limite_saques # quantidade limite de saques
        super().__init__(numero, cliente) #mas quando for passar os parametros tem q ser (Exemplo=parametro)

    def sacar(self, valor): # Aqui serve para impor limites de saques.
        # numero_saques = len()
        # excedeu_limite_saques = numero_saques > self._limite_saques
        excedeu_limite = valor > self._limite 
    
        if excedeu_limite:
            print("\n&@⁈ Operação falhou! O valor do saque excede o limite. &@⁈")
        
        # elif excedeu_limite_saques:
        #     print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        
        else:
            return super().sacar(valor)
        
        return False
        # Até o momento deixei apenas um limite de valor. 
        # Mas pode fazer quantos saques quiser por tanto que tenha algum valor
    
    def __str__(self): #aqui é uma formatação para a função "Listar Contas"
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """ 
     
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.contador = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return f"""
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR${conta.saldo:.2f}
        """ 
        except IndexError:
            raise StopIteration
    
   
# [CLIENTE]
class Cliente: # armazena algumas informações sobre o cliente, inclusive as contas criadas. 
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] #simula um banco de dados para armazenar todas as informações de todas as contas em um mesmo cpf

    def realizar_transacao(self, conta, transacao, extrato): #aqui envia a tranzação recebidas para o registro
        transacao.registrar(conta, extrato) 

    def adicionar_conta(self, conta):
        self.contas.append(conta) #envia a conta criada para o banco de dados

class PessoaFisica(Cliente): #armazena algumas informações sobre o cliente
    def __init__(self, nome, cpf, data_nasc, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        super().__init__(endereco)
      
        
# [HISTORICO (EXTRATO)]
class Historico: #Aqui armazena as informaçoes do extrato
    def __init__(self):
        self._transacoes = [] # simula um banco de dados para armazenar todo o extrato detalhado
    
    @property
    def transacoes(self): #pra poder ter acesso ao atributo transacoes
        return self._transacoes
    
    def adicionar_transacao(self, transacao):# aqui envia todo o conteudo recebido do registro para o banco de dados de extrato 
        self._transacoes.append(transacao)

    # TODO: atualizar as condições do tipo de transações.
    def gerar_relatorio(self, tipo_transacao=None):
        if not tipo_transacao:
            for trans in self._transacoes:
                yield trans               
        
        # elif tipo_transacao == Deposito:
        #     for trans in self._transacoes:
        #         yield trans['Depósito']
        
        # elif tipo_transacao == Saque:
        #     for trans in self._transacoes:
        #         yield trans['Saque'] 
            
        pass
    
class Transacao(ABC): #aqui define os atributos a serem usados nas classes de Deposito e Saque
    
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):#Aqui armazena toda as informações do deposito efetuado.
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self): #pra poder ter acesso ao atributo valor
        return self._valor    
        
    def registrar(self, conta, extrato): #aqui registra o deposito na conta que foi passado como parametro na função de depositar abaixo
        sucesso_transacao = conta.depositar(self.valor) 
            
        if sucesso_transacao: #aqui envia as informações do extrato
            conta.historico.adicionar_transacao(extrato) 

class Saque(Transacao): #Aqui armazena toda as informações do saque efetuado.
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self): #pra poder ter acesso ao atributo valor
        return self._valor    
        
    def registrar(self, conta, extrato): #aqui registra o saque na conta que foi passado como parametro na função de sacar abaixo
        sucesso_transacao = conta.sacar(self.valor) 
            
        if sucesso_transacao: #aqui envia as informações do extrato
            conta.historico.adicionar_transacao(extrato)        
    
# [LOG DO CODIGO]
def log_transação(func): #Serve para mostrar a data e hora de cada função executada no codigo.
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f'{datetime.now()}: {func.__name__.upper()}')
        return resultado    
    
    return envelope
    

# [FUNÇÔES DO MENU]
@log_transação
def depositar(clientes): # Serve pra efeturar um DEPOSITO no CPF solicitado.
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuário(cpf, clientes) #aq executa a funcão do filtro de usuario
    
    if not usuario:
        print('\n&@⁈ Cliente não encontrado &@⁈')
        return 
        
    valor = float(input('Digite o valor do depósito: R$'))
    conta = filtrar_conta_cliente(usuario) #aq executa a funcão do filtro de Contas
    
    if not conta:
        return
    
    transacao = Deposito(valor)
    extrato = f'Depósito \t\t+ R${valor:.2f}'
    usuario.realizar_transacao(conta, transacao, extrato)

@log_transação   
def sacar(clientes): # Serve pra efeturar um SAQUE no CPF solicitado.
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuário(cpf, clientes) #aq executa a funcão do filtro de usuario
    
    if not usuario:
        print('\n&@⁈ Cliente não encontrado &@⁈')
        return 
        
    valor = float(input('Digite o valor do Saque: R$'))
    conta = filtrar_conta_cliente(usuario) #aq executa a funcão do filtro de Contas
    
    if not conta:
        return
    
    transacao = Saque(valor)
    extrato = f'Saque \t\t\t- R${valor:.2f}'
    usuario.realizar_transacao(conta, transacao, extrato)

@log_transação    
def EXTRATO(clientes): # Serve pra emitir um EXTRATO do CPF solicitado
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuário(cpf, clientes)
    
    if not usuario:
        print('\n&@⁈ Cliente não encontrado &@⁈')
        return
    
    conta = filtrar_conta_cliente(usuario)
    
    if not conta:
        return
    
    print('\n=============== EXTRATO ================\n')
    # TODO: atualizar a implementação para utilizar um filtro escolhido (Saque ou deposito por exemplo).
    trans = conta.historico.gerar_relatorio()

    if conta.historico.transacoes == []:
        print('Não foram realizadas movimentações.')
    else:
        for transacao in trans: 
            print('----------------------------------------') 
            print(transacao)
    print('----------------------------------------')
    print(f'\nSaldo: R${conta.saldo:.2f}')
    print('========================================')   

@log_transação
def criar_usuário(usuarios): # Serve pra Cadastrar um usuário
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuário(cpf, usuarios)
    
    if usuario:
        print('\n&@⁈ ERRO! JÁ EXISTE USUÁRIO COM ESSE CPF &@⁈')
        return

    nome = input('Informe o Nome completo: ').capitalize()
    dataNasc = input('Informe a Data de nascimento (dd-mm-aaaa): ') 
    
    print('\nCADASTRO DE ENDEREÇO: ')
    rua = input('Rua: ').capitalize()
    num = input('N° ')
    bairro = input('Bairro: ').capitalize()
    cidade = input('Cidade: ').capitalize()
    estado = input('Estado(sigla): ').upper()
    endereço = {f'{rua}, {num}° - {bairro} - {cidade}/{estado}'}
    
    user = PessoaFisica(nome=nome, data_nasc=dataNasc, cpf=cpf, endereco=endereço)
    usuarios.append(user)
    print('\n——————— USUARIO CADASTRADO COM SUCESSO! ——————— ') 

@log_transação
def criar_conta(numero_conta, usuarios, contas): # Serve pra criar uma CONTA pra um USUÁRIO com cpf cadastrado
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuário(cpf, usuarios)
    
    if not usuario: 
        print("\n&@⁈ Usuário não encontrado, fluxo de criação de conta encerrado! &@⁈")
        return
        
    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print('\n——————— CONTA CRIADA COM SUCESSO! ——————— ')

def listar_contas(contas): # Serve pra Listar todas as contas existentes
    #Aqui vai chamar o ContaIterador passando "contas" como argumento
    if contas == []:
        print('\n&@⁈ ERRO! Nenhuma conta encontrada &@⁈')
    else:
        for conta in ContaIterador(contas):
            print('=' * 50)
            print(textwrap.dedent(str(conta)))
        
def filtrar_usuário(cpf, usuarios): # Aqui serve pra poder filtrar se o cpf ja é um usuário cadastrado.
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
        
def filtrar_conta_cliente(cliente): # Aqui serve pra poder filtrar se o cliente tem conta existente.
    if not cliente.contas:
        print("\n&@⁈ Cliente não possui CONTA! &@⁈")
        return
    
    #FIXME: não permite cliente escolher a conta
    return cliente.contas[0]
        
def menu():
    print('''\n   >>>> BANCO <<<<
            
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo Usuário
[q] Sair      
    ''')
    opçao = input('⇒ ').lower()
    return opçao

def main():
    clientes = []# guarda todos os usuarios cadastrados
    contas = [] # guarda todas as contas cadastradas

    while True:
        opção = menu()
        
        if opção == 'd':
            depositar(clientes)
            
        elif opção == 's':
            sacar(clientes)

        elif opção == 'e':
            EXTRATO(clientes)
            
        elif opção == 'nc':
            qt_contas = len(contas) + 1
            conta = criar_conta(qt_contas, clientes, contas)
        
        elif opção == 'lc':
            print()
            listar_contas(contas)
        
        elif opção == 'nu':
            criar_usuário(clientes)
        
        elif opção == 'q':
            print('Obrigado pela preferencia... \nVolte sempre e tenha um ótimo dia! \n')
            break

        else:
            print('\nOpção invalida!')
        
# -- INICIO DO PROGRAMA --       

main()    

# -- FIM DO PROGRAMA --


