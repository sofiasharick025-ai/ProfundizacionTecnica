
edad1 = int(input("Ingresa la primera edad: "))
edad2 = int(input("Ingresa la segunda edad: "))

son_iguales = edad1 == edad2
primera_es_mayor = edad1 > edad2
ambas_mayores_18 = (edad1 > 18) and (edad2 > 18)

print("¿Son iguales?:", son_iguales)
print("¿La primera es mayor?:", primera_es_mayor)
print("¿Ambas son mayores de 18?:", ambas_mayores_18)