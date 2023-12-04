from datetime import date

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


while True:

    opcao = input(menu)

    if opcao == "d":
        valor = int(input("Selecione o valor a ser depositado: "))

        if valor > 0:
            saldo += valor

            print(f"Deposito no valor de R$ {valor} realizado.")
            extrato += f"DEPOSITO: R$ {valor}\nDATA: {date.today()}\n"
        else:
            print("Faça um deposito positivo.")

    elif opcao == "s":
        saque = int(input("Selecione o valor a ser sacado."))

        if (saque > 500 or saque <= 0) or saque > saldo:
            print("Faça um saque positivo e menor que R$ 500")
        else:
            if LIMITE_SAQUES > 0:
                saldo -= saque

                print(f"Saque no valor de R$ {saque} realizado.\n Saldo atual: R$ {saldo}")
                extrato += f"SAQUE: R$ {saque}\nDATA: {date.today()}\n"
                LIMITE_SAQUES -= 1
            else:
                print("Limite de saque atingindo")
    elif opcao == "e":

        print(extrato)
    elif opcao == "q":

        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
