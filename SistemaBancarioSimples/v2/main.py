auth = False
account_logged = {}


user_fake = {
    "CPF": 213546464,
    "nome": "Marcos",
    "data_nascimento": "2003-07-22",
    "Nacionalidade": "Brasileiro",
    "endereco": "Rua Dr Luiz - Mangue - Rio de Janeiro - RJ"
}

account_fake = {
    "user": user_fake,
    "banco": "0001",
    "conta": "123",
    "saldo": 1000,
    "limite": 500,
    "extrato": "",
    "numero_saques": 0,
    "LIMITE_SAQUES": 3
}

account_fake2 = {
    "user": user_fake,
    "banco": "0001",
    "conta": "124",
    "saldo": 0,
    "limite": 500,
    "extrato": "",
    "numero_saques": 0,
    "LIMITE_SAQUES": 3
}

contas = [account_fake, account_fake2]


def criar_cliente(*, rua, bairro, municipio, uf, cpf, nome, nascimento, nacionalidade):
    cliente = {
        "CPF": f"{int(cpf)}",
        "nome": f"{nome}",
        "data_nascimento": f"{nascimento}",
        "Nacionalidade": f"{nacionalidade}",
        "endereco": f"{rua} - {bairro} - {municipio} - {uf}"
    }

    contas.append(cliente)
    listar_usuarios()


def listar_usuarios():
    for i in range(len(contas)):
        print(contas[i])


def depositar(valor, /, metodo, conta_corrente):
    conta = conta_corrente.copy()

    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\nMétodo: {metodo}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return conta


def sacar(*, conta_corrente, valor):
    conta = conta_corrente.copy()

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > conta["limite"]
    excedeu_saques = conta["numero_saques"] >= conta["LIMITE_SAQUES"]

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return conta


def imprimir_extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


while True:
    if auth is False:
        c = str(input("Digite o núm da conta: "))
        index_account = [i for i in range(len(contas)) if contas[i]["conta"] == c]
        if index_account:
            auth = True
            account_logged = contas[index_account[0]]
    else:
        opcao = input(f"""
Olá {account_logged["user"]["nome"]}

[d] Depositar
[s] Sacar
[e] Extrato
[l] Sair da conta
[q] Sair

=> """)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            metodo = input("Método de Deposito: ")
            account_logged = depositar(valor, metodo, account_logged)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            account_logged = sacar(conta_corrente=account_logged, valor=valor)
            print(account_logged)
        elif opcao == "e":
            imprimir_extrato(account_logged["saldo"], extrato=account_logged["extrato"])
        elif opcao == "l":
            index_account = [i for i in range(len(contas)) if contas[i]["conta"] == c]
            contas[index_account[0]] = account_logged
            auth = False
        elif opcao == "c":
            rua, bairro, municipio, uf = input("Rua: "), input("\nBairro:"), input("\nMunicipio:"), input("\nUF:")
            cpf, nome, nascimento, nacionalidade = input("CPF: "), input("\nNome: "), input("\nData de nascimento:"), input("\nNacionalidade")
            criar_cliente(rua=rua, bairro=bairro, municipio=municipio, uf=uf, cpf=cpf, nome=nome, nascimento=nascimento, nacionalidade=nacionalidade)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
