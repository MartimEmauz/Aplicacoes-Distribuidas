#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 27
Números de aluno: 58668 | 58621
"""
# Zona para fazer imports

import sock_utils as utils
import socket as s
import sys
from net_client import server_connection
import time

# Programa principal

"""
Dúvidas:
É preciso dar encode ao comando?
"""

# Definição de constantes
client_id = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

while True:

    comando = str(input("comando > "))
    comando = comando.split(" ")

    if comando[0] == 'SUBSCR':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando + [client_id])
            resposta = connection.send_receive(comando_str.encode())
            print(resposta)
            connection.close()

    elif comando[0] == 'CANCEL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando + [client_id])
            resposta = connection.send_receive(comando_str.encode())
            connection.close()

    elif comando[0] == 'STATUS':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando + [client_id])
            resposta = connection.send_receive(comando_str.encode())
            connection.close()

    elif comando[:2] == 'INFOS M':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando + [client_id])
            resposta = connection.send_receive(comando_str.encode())
            connection.close()

    elif comando[:2] == 'INFOS K':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando + [client_id])
            resposta = connection.send_receive(comando_str.encode())
            connection.close()

    elif comando[:2] == 'STATIS L':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando)
            connection.close()

    elif comando[:2] == 'STATIS ALL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            comando_str = " ".join(comando)
            resposta = connection.send_receive(comando_str.encode())
            connection.close()

    elif comando[0] == 'SLEEP':
        time.sleep(int(comando[1]))

    elif comando[0] == 'EXIT':
        break

    else:
        print("UNKNOWN-COMMAND")