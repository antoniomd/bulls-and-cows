""" 
Hombre Muerto Hombre Herido
Un número de cuatro cifras que no se repitan
Si se acierta un número y su posición es un hombre muerto
Si se acierta un número pero no su posición es un hombre herido
"""

#! /usr/bin/env python3

# Importo la función random de la libreria
import random

# Genera el número secreto aleatoriamente
def numberGeneration():
    notValid = 1
    while notValid == 1:
        number = random.randrange(1023,9876)
        notValid = validNumber(str(number))
    return number

# Función que valida el número generado o introducido
def validNumber(number):
    notValid = 0
    for i in range(len(number)):
        for j in range(len(number)):
            if i != j and str(number)[i] == str(number)[j]:
                notValid = 1
    return notValid

def main():
    # Inicializo los valores de heridos, muertos e intentos
    muertos = heridos = intentos = 0

    # Genero el número secreto
    secretNumber = numberGeneration()

    while True:

        # El concursante introduce el número que cree que es
        notValid = 1
        while notValid == 1:
            print('¿Cuál crees que es el número?')
            myNumber = str(input())
            notValid = validNumber(str(myNumber))
            if notValid == 1:
                print('El número no cumple las normas')
        
        intentos +=1

        # Comienza un bucle for para calcular los heridos y muertos
        for index,dig in enumerate(str(myNumber)):
            if dig == str(secretNumber)[index]:
                muertos +=1
            elif dig in str(secretNumber):
                heridos +=1
        
        if muertos == 4:
            print ('Enhorabuena, ¡has acertado!')
            print ('Has necesitado ' + str(intentos) + ' intentos')
            break
        
        else:
            print('Número de muertos: ' + str(muertos))
            print('Número de heridos: ' + str(heridos))
            print('Número de intentos: ' + str(intentos))
            
            # Borro los valores de heridos, muertos e intentos
            muertos = 0
            heridos = 0

if __name__ == "__main__":
	main()