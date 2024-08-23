class Banco:
    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    LIMITE_SAQUES = 3
    
    def depositar(v):
        Banco.saldo += v
        Banco.extrato = Banco.extrato + f'\nDepósito =  +R${v:.2f}' 
        
    
    def sacar(v):
        if v <= Banco.saldo:
            Banco.saldo -= v
            Banco.extrato = Banco.extrato + f'\nSaque =  -R${v:.2f}' 
        else:
            print('Saldo insuficiente para realizar o saque.')
            
    def EXTRATO():
        print('\n============ EXTRATO ============')
        if Banco.extrato == '':
            print('Não foram realizadas movimentações.')
        else:
            print(Banco.extrato)
        print(f'\nSaldo: R${Banco.saldo:.2f}')
        print('=================================')
    
    def menu():
        print('''\n   >>>> BANCO <<<<
              
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair      
            ''')

    
if __name__== '__main__':
    while True:
        opção = input(f'{Banco.menu()} Opção: ').lower()
        
        if opção == 'd':
            deposito = eval(input('Digite o valor do deposito: R$'))
            if deposito < 0:
                print('Valor invalido')
            else:
                Banco.depositar(deposito)
            
        elif opção == 's':
            if Banco.numero_saques != Banco.LIMITE_SAQUES:
                saque = int(input('Digite o valor do saque: '))
                if saque < Banco.limite:
                    Banco.sacar(saque)
                    Banco.numero_saques += 1
                else:
                    print(f'Erro! Você atingiu o limite de R${Banco.limite} por operação!')
            else:
                print('Você atingiu seu limite de saques diário.')
                
        elif opção == 'e':
            Banco.EXTRATO()
            
        elif opção == 'q':
            print('Obrigado pela preferencia... \nVolte sempre e tenha um ótimo dia!')
            break
        
        else:
            print('Opção invalida!')