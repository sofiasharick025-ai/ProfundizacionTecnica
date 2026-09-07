
num1 = float(input("Ingresa el primer número: "))
num2 = float(input("Ingresa el segundo número: "))


suma = num1 + num2
resta = num1 - num2
multiplicacion = num1 * num2
division = num1 / num2 if num2 != 0 else "Indefinida (división por cero)"


print(f"Suma: {suma}")
print(f"Resta: {resta}")
print(f"Multiplicación: {multiplicacion}")
print(f"División: {division}")