from scapy.all import rdpcap, ICMP, Raw, IP
import google.generativeai as genai
from colorama import Fore, Style
import re

# ---------- CONFIGURACIÓN ----------
PCAP_FILE = "cripto_LAB1_captura.pcapng"
MI_IP_LOCAL = "TU_IP"  # reemplaza con tu IP real
API_KEY = "TU_API_KEY_DE_GOOGLE"   # Reemplázala con tu clave
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------- FUNCIONES ----------
def extraer_texto_pcap(pcap_file, mi_ip):
    """
    Extrae caracteres de paquetes ICMP con origen en mi_ip.
    Toma solo el primer byte de cada payload.
    """
    paquetes = rdpcap(pcap_file)
    chars = []

    for pkt in paquetes:
        if ICMP in pkt and Raw in pkt and IP in pkt and pkt[IP].src == mi_ip:
            data = bytes(pkt[Raw].load)
            if len(data) > 0:
                try:
                    chars.append(chr(data[0]))
                except:
                    continue
    return "".join(chars)

def descifrar_cesar(texto, desplazamiento):
    """
    Aplica un desplazamiento César inverso a un texto (solo letras a-z).
    """
    resultado = ""
    for char in texto:
        if 'a' <= char <= 'z':
            nuevo = (ord(char) - ord('a') - desplazamiento) % 26 + ord('a')
            resultado += chr(nuevo)
        else:
            resultado += char
    return resultado

def consultar_ia(candidatos):
    """
    Envía todas las combinaciones a Gemini y devuelve los índices de los candidatos con sentido.
    """
    prompt = (
        "Tengo varias posibles palabras/frases obtenidas con cifrado César. "
        "Dime cuál tiene más sentido en español o inglés. "
        "Responde solo con los números de las combinaciones correctas, separados por comas:\n\n"
    )
    prompt += "\n".join([f"{i}: {c}" for i, c in enumerate(candidatos)])
    
    response = model.generate_content(prompt)
    
    # Extraer los números indicados por la IA
    indices = re.findall(r"\d+", response.text)
    indices = [int(x) for x in indices]
    return indices

# ---------- PROGRAMA PRINCIPAL ----------
if __name__ == "__main__":
    # 1. Obtener el texto cifrado desde el pcap
    texto_cifrado = extraer_texto_pcap(PCAP_FILE, MI_IP_LOCAL)
    print(f"Texto cifrado obtenido del pcap: {texto_cifrado}\n")

    # 2. Probar todas las combinaciones de César
    candidatos = [descifrar_cesar(texto_cifrado, i) for i in range(26)]

    # 3. Preguntar a la IA cuáles combinaciones tienen sentido
    indices_correctos = consultar_ia(candidatos)

    # 4. Imprimir resultados
    print("=== RESULTADOS ===")
    for i, cand in enumerate(candidatos):
        if i in indices_correctos:
            print(Fore.GREEN + f"{i}: {cand}" + Style.RESET_ALL)
        else:
            print(f"{i}: {cand}")