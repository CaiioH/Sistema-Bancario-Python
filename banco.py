import textwrap

class Banco:
    
    LIMITE_SAQUES = 3 # quantidade limite de saques
    AGENCIA = '0001' #agencia
       
    saldo = 0 #saldo
    limite = 500 # valor limite de saques por operação
    extrato = '' # extrato
    numero_saques = 0 # armazena a quantidade de saques feitos
    usuarios = []# guarda todos os usuarios cadastrados
    contas = [] # guarda todas as contas cadastradas
    qt_contas = 1 # aqui é pra definir o numero da conta   
        
    def depositar(v):
        if v < 0:
            print('Valor invalido')
        else:
            Banco.saldo += v
            Banco.extrato +=  f'\nDepósito \t\t+ R${v:.2f}'
            print('\n——————— DEPÓSITO FEITO COM SUCESSO! ———————') 
        
        return Banco.saldo, Banco.extrato
        
    def sacar(v):
        if v < Banco.limite:
            if v <= Banco.saldo:
                Banco.saldo -= v
                Banco.extrato += f'\nSaque \t\t\t- R${v:.2f}'
                print('\n——————— SAQUE EFETUADO COM SUCESSO! ———————')        
                Banco.numero_saques += 1
            else:
                print('Saldo insuficiente para realizar o saque.')     
        else:
            print(f'&@⁈ Erro! Você atingiu o limite de R${Banco.limite} por operação! &@⁈')
             
    def EXTRATO():
        print('\n=============== EXTRATO ===============')
        if Banco.extrato == '':
            print('Não foram realizadas movimentações.')
        else:
            print(Banco.extrato)
        print(f'\nSaldo: R${Banco.saldo:.2f}')
        print('========================================')
    
    def criar_conta(agencia, numero_conta, usuarios):
        cpf = input('Informe o CPF do usuário: ')
        usuario = Banco.filtrar_usuário(cpf, usuarios)
        
        if usuario: 
            print('\n——————— CONTA CRIADA COM SUCESSO! ——————— ')
            return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

        print("\n&@⁈ Usuário não encontrado, fluxo de criação de conta encerrado! &@⁈")
    
    def listar_contas(contas):
        for conta in contas:
            linha = f"""
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """ #arrumar aqui que ta dando erro no titular
            print('-' * 50)
            print(textwrap.dedent(linha))
            
    def criar_usuário(usuarios):
        cpf = input('Informe o CPF (somente número): ')
        usuario = Banco.filtrar_usuário(cpf, Banco.usuarios)
        
        if usuario:
            print('\n&@⁈ ERRO! JÁ EXISTE USUÁRIO COM ESSE CPF &@⁈')
            return

        nome = input('Informe o Nome completo: ').capitalize()
        dataNasc = input('Informe a Data de nascimento (dd-mm-aaaa): ') 
        
        print('\nCADASTRO DE ENDEREÇO (rua, N° - bairro - cidade/sigla estado): ')
        rua = input('Rua: ').capitalize()
        num = input('N° ')
        bairro = input('Bairro: ').capitalize()
        cidade = input('Cidade: ').capitalize()
        estado = input('Estado(sigla): ').upper()
        endereço = {f'{rua}, {num}° - {bairro} - {cidade}/{estado}'}
        
        user = {"nome": nome, "dataNasc": dataNasc, "cpf": cpf, "endereço": endereço}
        Banco.usuarios.append(user)
        print('\n——————— USUARIO CADASTRADO COM SUCESSO! ——————— ') 

    def filtrar_usuário(cpf, usuarios):
        for usuario in usuarios:
            if usuario["cpf"] == cpf:
                return usuario
          
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

if __name__== '__main__':
    while True:
        opção = Banco.menu()
        
        if opção == 'd':
            deposito = float(input('Digite o valor do depósito: R$'))
            Banco.depositar(deposito)
            
        elif opção == 's':
            if Banco.numero_saques != Banco.LIMITE_SAQUES:
                saque = int(input('Digite o valor do saque: '))
                Banco.sacar(saque)
            else:
                print('Você atingiu seu limite de saques diário.')
                
        elif opção == 'e':
            Banco.EXTRATO()
            
        elif opção == 'nc':
            conta = Banco.criar_conta(Banco.AGENCIA, Banco.qt_contas, Banco.usuarios)
            
            if conta:
                Banco.contas.append(conta)
                Banco.qt_contas += 1
        
        elif opção == 'lc':
            Banco.listar_contas(Banco.contas)
        
        elif opção == 'nu':
            Banco.criar_usuário(Banco.usuarios)
      
        elif opção == 'q':
            print('Obrigado pela preferencia... \nVolte sempre e tenha um ótimo dia! \n')
            break
    
        else:
            print('\nOpção invalida!')
            
            
        


