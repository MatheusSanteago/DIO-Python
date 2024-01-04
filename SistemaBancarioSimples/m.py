from datetime import datetime
from abc import ABC, abstractmethod, abstractclassmethod


class Cliente():
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self.agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self.numero

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Ops")
        elif valor > 0:
            self._saldo -= valor
            print("Oks")
        else:
            print("erro")
            return False

        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Ok")
        else:
            print("erro")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("OPS")
        elif excedeu_saques:
            print("OPS")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Agência:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%m:%s")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        super()._valor = valor

        @property
        def valor(self):
            return self._valor

        def registrar(self, conta):
            sucesso_transacao = conta.sacar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        super()._valor = valor

        @property
        def valor(self):
            return self._valor

        def registrar(self, conta):
            sucesso_transacao = conta.depositar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)
