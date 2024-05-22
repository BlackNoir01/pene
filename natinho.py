import streamlit
import streamlit as st
import random
import math
import csv 

def leer_tabla_csv(archivo):
    tabla = {}
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for fila in reader:
            if len(fila) > 0:  # Asegurarse de que la fila tiene al menos un elemento
                ascii_value = fila[0]
                decimal_value = int(fila[1])
                tabla[ascii_value] = decimal_value
    return tabla

def eratostenes(n):
    numeros = [True]*(n+1)
    numeros[0] = numeros[1] = False
    for factor in range(2, int(math.sqrt(n+1))+1):
        if not numeros[factor]:
            continue
        for indice in range(factor*2, n+1, factor):
            numeros[indice] = False
    return [x for x, es_primo in enumerate(numeros) if es_primo]

def primoaleatorio(primos):
    p = random.choice(primos)
    q = random.choice(primos)
    return p, q

def encontrar_claves(phi_n):
    for e in range(2, phi_n):
        for d in range(2, phi_n):
            if (d * e) % phi_n == 1:
                return e, d

def convertir_a_numeros(texto, tabla):
    numeros = []
    for caracter in texto:
        if caracter in tabla:
            numeros.append(tabla[caracter])
        elif caracter == ' ':
            numeros.append(tabla.get(' ', -1))
    return numeros

def encriptar(texto, e, n, tabla):
    numeros = convertir_a_numeros(texto, tabla)
    numeros_encriptados = [pow(numero, e) % n for numero in numeros]
    return numeros_encriptados

def desencriptar(numeros_encriptados, d, n, tabla):
    numeros_desencriptados = [pow(numero, d) % n for numero in numeros_encriptados]
    tabla_invertida = {valor: clave for clave, valor in tabla.items()}
    texto_desencriptado = ''.join([tabla_invertida.get(numero, ' ') for numero in numeros_desencriptados])
    if texto_desencriptado.strip() == '':
        return "Clave no válida"
    else:
        return texto_desencriptado

def main():
    st.title("Encriptación RSA")

    primos = eratostenes(1000)
    p, q = primoaleatorio(primos)
    n = p * q
    phin = (p - 1) * (q - 1)
    e, d = encontrar_claves(phin)
    archivo_csv = r'C:\Users\ferna\Documents\letras.csv'
    tabla = leer_tabla_csv(archivo_csv)

    opcion = st.radio("Seleccione una opción:", ['Encriptar', 'Desencriptar'])

    if opcion == 'Encriptar':
        texto = st.text_input("Ingrese el texto a encriptar:")
        if st.button("Encriptar"):
            numeros_encriptados = encriptar(texto, e, n, tabla)
            st.write("Texto encriptado:")
            st.write(' '.join(map(str, numeros_encriptados)))
            st.write("Clave privada (d, n):", (d, n))
    elif opcion == 'Desencriptar':
        numeros_encriptados_input = st.text_input("Ingrese los números encriptados separados por espacios:")
        d_n_input = st.text_input("Ingrese la clave privada en el formato 'd, n':")
        if st.button("Desencriptar"):
            numeros_encriptados = [int(num) for num in numeros_encriptados_input.split()]
            d_input, n_input = map(int, d_n_input.split(','))
            texto_desencriptado = desencriptar(numeros_encriptados, d_input, n_input, tabla)
            st.write("Texto desencriptado:")
            st.write(texto_desencriptado)

if __name__ == "__main__":
    main()
