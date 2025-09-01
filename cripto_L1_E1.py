def cifrado_cesar(texto: str, desplazamiento: int) -> str:
    resultado = ""
    for char in texto:
        if 'a' <= char <= 'z':  # solo letras minúsculas
            # Convertimos a número (0-25), aplicamos desplazamiento, y regresamos a letra
            nuevo = (ord(char) - ord('a') + desplazamiento) % 26 + ord('a')
            resultado += chr(nuevo)
        else:
            # si no es letra minúscula, se deja igual
            resultado += char
    return resultado


# Ejemplo de uso
if __name__ == "__main__":
    texto = input("Ingrese el texto a cifrar: ")
    desplazamiento = int(input("Ingrese el desplazamiento: "))
    
    cifrado = cifrado_cesar(texto, desplazamiento)
    print("Texto cifrado:", cifrado)