from abc import ABC, abstractmethod
from datetime import date

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente: Cliente, numero: int, agencia: str):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(cliente, numero, "0001")

    def saldo(self) -> float:
        return self._saldo

    def sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self._saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, agencia: str, limite: float, limite_saques: int):
        super().__init__(cliente, numero, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int, limite=500.0, limite_saques=3):
        return cls(cliente, numero, "0001", limite, limite_saques)

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta._historico.adicionar_transacao(self)


if __name__ == "__main__":
    # 1. Create a customer
    joao = PessoaFisica(
        cpf="123.456.789-00",
        nome="João da Silva",
        data_nascimento=date(1990, 5, 21),
        endereco="Rua das Flores, 123"
    )

    # 2. Create a checking account (Conta Corrente)
    conta = ContaCorrente.nova_conta(joao, 1001)
    joao.adicionar_conta(conta)

    # 3. Perform a Deposit
    print(f"Saldo Inicial: R$ {conta.saldo():.2f}")
    deposito = Deposito(500.0)
    joao.realizar_transacao(conta, deposito)
    print(f"Saldo após depósito: R$ {conta.saldo():.2f}")

    # 4. Perform a Withdrawal
    saque = Saque(150.0)
    joao.realizar_transacao(conta, saque)
    print(f"Saldo após saque: R$ {conta.saldo():.2f}")