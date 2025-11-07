import datetime

# ----------------------------------------------------------------------
# Classes de Transação
# ----------------------------------------------------------------------

class Transacao:
    """Classe base para todas as transações."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Método abstrato para registrar a transação na conta."""
        raise NotImplementedError

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o depósito na conta."""
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o saque na conta."""
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

# ----------------------------------------------------------------------
# Classe Histórico
# ----------------------------------------------------------------------

class Historico:
    """Registra o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico com data e hora."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# ----------------------------------------------------------------------
# Classes de Conta
# ----------------------------------------------------------------------

class Conta:
    """Classe base para contas bancárias."""
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de classe para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """Realiza um saque na conta."""
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        elif valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    """Representa uma conta corrente com limite e limite de saques."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para incluir limites."""
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
                and datetime.datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date() == datetime.date.today()
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# ----------------------------------------------------------------------
# Classes de Cliente
# ----------------------------------------------------------------------

class Cliente:
    """Classe base para clientes do banco."""
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação na conta do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    """Representa um cliente pessoa física."""
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

# ----------------------------------------------------------------------
# Funções de Apoio (Simulação de Menu)
# ----------------------------------------------------------------------

def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(menu_text)

def filtrar_cliente(cpf, clientes):
    """Retorna o cliente com o CPF informado, se existir."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """Permite ao cliente escolher uma de suas contas."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # Simplificação: assume que o cliente só tem uma conta por enquanto
    # Em um sistema real, pediríamos ao usuário para escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    """Função para realizar um depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    """Função para realizar um saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    """Função para exibir o extrato da conta."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f} ({transacao['data']})")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_novo_cliente(clientes):
    """Função para criar um novo cliente (Pessoa Física)."""
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_nova_conta(numero_conta, clientes, contas):
    """Função para criar uma nova conta corrente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    """Função para listar todas as contas."""
    for conta in contas:
        print("=" * 100)
        print(str(conta))

# ----------------------------------------------------------------------
# Função Principal
# ----------------------------------------------------------------------

def main():
    """Função principal para executar o sistema bancário."""
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_novo_cliente(clientes)

        elif opcao == "nc":
            criar_nova_conta(numero_conta, clientes, contas)
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()
