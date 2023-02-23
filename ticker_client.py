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
client_id = sys.argv[0]
HOST = sys.argv[2]
PORT = sys.argv[3]

while True:

    comando = str(input("comando > "))
    comando = comando.split(" ")

    if comando[0] == 'SUBSCR':
        if  len(comando) < 3:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando.append(client_id)')
            connection.close()

    elif comando[0] == 'CANCEL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando + " " + client_id')
            connection.close()

    elif comando[0] == 'STATUS':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando + " " + client_id')
            connection.close()

    elif comando[:2] == 'INFOS M':
        if  len(comando) < 3:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando + " " + client_id')
            connection.close()

    elif comando[:2] == 'INFOS K':
        if  len(comando) < 3:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando + " " + client_id')
            connection.close()

    elif comando[:2] == 'STATIS L':
        if  len(comando) < 3:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando')
            connection.close()

    elif comando[:2] == 'STATIS ALL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

            connection = server_connection(HOST, PORT)
            connection.connect()
            resposta = connection.send_receive(b'comando')
            connection.close()

    elif comando[0] == 'SLEEP':
        time.sleep(int(comando[1]))

    elif comando[0] == 'EXIT':
        break

    else:
        print("UNKNOWN-COMMAND")