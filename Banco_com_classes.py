from abc import ABC, abstractproperty, abstractclassmethod


class Historico:
    def __init__(self):
        self.transacoes = list()
    
    @property
    def transacoes(self):
        return self.trasacoes
    
    def add_trasacao(self, transacao):
        self.transacoes.append(
            {
            "Tipo": transacao.__class__.__name__,
            "valor": transacao.valor 
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = '0001'
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo
    
    @property 
    def numero(self):
        return self.__numero
    
    @property 
    def agencia(self):
        return self.__agencia
    
    @property 
    def cliente(self):
        return self.__cliente
    
    @property 
    def historico(self):
        return self.__historico
    
    def saldo(self):
        return (f'Seu saldo é de R${self.__saldo}')        

    def sacar(self, valor):
        if valor < self.__saldo and valor > 0:
            self.__saldo -= valor
            print(f'saque de R${valor} efetuado!')
            return True
        else:
            print('Saldo insuficiente!')
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f'Deposito de R${valor} efetuado!')
            return True
        else:
            print('Erro no deposito \nO valor precisa ser positivo!')
        return False


class Conta_corrente(Conta):
    def __init__(self, numero, cliente , limite=500.00, limite_saques=3):
        super().__init__(numero, cliente)
        self.__limite = limite
        self.__limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [Transacao for transacao in self.historico.
             transacoes if transacao ['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print('Voce não tem limite para concluir essa operação!!!')
        
        elif excedeu_saques:
            print('Voce ja fez o maximo de saques da sua conta!!!')

        else:
            return super().sacar(valor)
        
        return False

    def __str__(self) -> str:
        return f"""\
Agencia:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
        """



class Cliente:
    def __init__(self, endereco) -> None:
        self.__endereco = endereco
        self.__contas = list()
    
    def realizar_transacao(self, conta, transacao):
        Transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)


class Pessoa(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Transacao(ABC):
    
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)