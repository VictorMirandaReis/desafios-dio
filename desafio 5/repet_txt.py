# Agora vamos solicitar uma string e um número inteiro como entrada. Depois teremos que retornar a string repetida o número de vezes informado.

string = input("Digite um string: ")
numero = int(input("Digite um número inteiro: "))

while numero > 0:
    if numero < 5:
        print((string + ' ') * numero)
        numero = 0
    else:
        print((string + ' ') * 5)
        numero = numero - 5
