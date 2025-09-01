from scapy.all import IP, ICMP, send

def enviar_icmp_por_caracter(destino: str, texto: str):
    for caracter in texto:
        paquete = IP(dst=destino)/ICMP()/caracter.encode()
        send(paquete, verbose=0)
        print(f"Paquete enviado con carácter: {caracter}")

if __name__ == "__main__":
    destino = "8.8.8.8"  # Dirección IP de destino
    texto = input("Ingrese el texto a enviar por ICMP: ")
    enviar_icmp_por_caracter(destino, texto)
