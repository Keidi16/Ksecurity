#!/usr/bin/python3

import multiprocessing
import os.path
import subprocess, re
import time
import socket
from colorama import Fore, Back


banner = (Fore.GREEN+'''
_  ______  _____ ____ _   _ ____  ___ _______   __
| |/ / ___|| ____/ ___| | | |  _ \|_ _|_   _\ \ / /
| ' /\___ \|  _|| |   | | | | |_) || |  | |  \ V /
| . \ ___) | |__| |___| |_| |  _ < | |  | |   | |
|_|\_\____/|_____\____|\___/|_| \_\___| |_|   |

	          Versao 1.0

Monitor Access Logs || Monitorar conexoes 

''')
print (banner)

# Removir esssa funcionalidade de alertar acessos restristos aos arquivos
restrito = re.compile(r'.*(\/admin|\/.git|\/login|\/dashboard|\/private\/.config|).*')
access_log_path = "/var/log/apache2/access.log"

def monitorar_arquivo_log():
    with open(access_log_path, "r") as arquivo_log:
       
        arquivo_log.seek(0, 2)

        while True:
            # Lê novas linhas do arquivo
            novas_linhas = arquivo_log.readlines()

            if novas_linhas:
                # Processa as novas linhas
                for linha in novas_linhas:
                    # Realize aqui qualquer processamento desejado para cada linha
                    partes = linha.split()

                    # Verifica se a linha possui o formato esperado
                    if len(partes) >= 12:
                        ip = partes[0]
                        data_hora = partes[3][1:] + " " + partes[4][:-1]
                        metodo = partes[5][1:]
                        url = partes[6]
                        protocolo = partes[7][:8]

                        # Obtém o cabeçalho da requisição
                        cabeçalho = " ".join(partes[11:])
                        print("----------------------------------------------------------------------------------------")
                        print(Fore.GREEN+"IP:", ip)
                        print("Data/Hora:", data_hora)
                        print("Método:", metodo)
                        print("URL:", url)
                        print("Protocolo:", protocolo)
                        print("Cabeçalho:", cabeçalho)
                        print("----------------------------------------------------------------------------------------")

            time.sleep(1)

def get_new_connections(existing_connections):
    # Executa o comando 'netstat' para obter as conexões ativas
    output = subprocess.check_output(['netstat', '-ntu','-nlpt']).decode()

    # Extrai os endereços IP e portas das conexões
    connection_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b"
    connections = re.findall(connection_pattern, output)

    # Filtra as conexões que não estão na lista de conexões existentes
    new_connections = [conn for conn in set(connections) if conn not in existing_connections]

    # Atualiza a lista de conexões existentes
    existing_connections.extend(new_connections)

    return new_connections

def is_internal_ip(ip_address):
    # Verifica se o endereço IP é um endereço IP interno
    octets = ip_address.split('.')
    if octets[0] == '10':
        return True
    elif octets[0] == '192' and octets[1] == '168':
        return True
    elif octets[0] == '172' and 16 <= int(octets[1]) <= 31:
        return True
    elif ip_address == '127.0.0.1':
        return True
    else:
        return False

def start_monitoring():
    existing_connections = []

    try:
        while True:
              new_connections = get_new_connections(existing_connections)

              for connection in new_connections:
                  ip_address, port = connection.split(':')
                  if is_internal_ip(ip_address):
                      print(Fore.YELLOW+"--------------------------------------------------------------------------------------")
                      print(f"Nova conexão interna: {ip_address}:{port}")
                  else:
                      print(Fore.BLUE+"---------------------------------------------------------------------------------------")
                      print(f"Nova conexão externa: {ip_address}:{port}")
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")


if __name__ == '__main__':

   p1 = multiprocessing.Process(target=monitorar_arquivo_log)
   p2 = multiprocessing.Process(target=start_monitoring)
  
   p1.start()
   p2.start()
  
   p1.join()
   p2.join()
 
