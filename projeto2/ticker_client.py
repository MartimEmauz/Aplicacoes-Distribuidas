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
import pickle

# Programa principal

# Definição de constantes
client_id = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

comandos = {
    'SUBSCR': 10,
    'CANCEL': 20,
    'STATUS': 30,
    'INFOS M': 40,
    'INFOS K': 50,
    'STATIS L': 60,
    'STATIS ALL': 70,
}

while True:

    comando = str(input("Comando > "))
    print(comando)
    comando = comando.split(" ")

    if comando[0] == 'SUBSCR':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando[0] = comandos[comando[0]]
            comando.append(client_id)
            connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
            connection.close()

    elif comando[0] == 'CANCEL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando[0] = comandos[comando[0]]
            comando.append(client_id)
            resposta = connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
            connection.close()

    elif comando[0] == 'STATUS':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            comando[0] = comandos[comando[0]]
            comando.append(client_id)
            resposta = connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
            connection.close()

    elif comando[0] == 'INFOS' and comando[1] == 'M':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        connection = server_connection(HOST, PORT)
        connection.connect()
        comando = [comandos[" ".join(comando[0:2])]]
        comando.append(client_id)
        resposta = connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
        connection.close()

    elif comando[0] == 'INFOS' and comando[1] == 'K':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")

        connection = server_connection(HOST, PORT)
        connection.connect()
        comando = [comandos[" ".join(comando[0:2])]]
        comando.append(client_id)
        resposta = connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
        connection.close()

    elif comando[0] == 'STATIS' and comando[1] == 'L':
        if  len(comando) <= 2:
            print("MISSING-ARGUMENTS")
        else:
            connection = server_connection(HOST, PORT)
            connection.connect()
            newComando = [comandos[" ".join(comando[0:2])]]
            newComando.append(comando[2])
            resposta = connection.send_receive(pickle.dumps([int(x) for x in newComando], -1))
            connection.close()

    elif comando[0] == 'STATIS' and comando[1] == 'ALL':
        if  len(comando) < 2:
            print("MISSING-ARGUMENTS")
        connection = server_connection(HOST, PORT)
        connection.connect()
        comando = [comandos[" ".join(comando[0:2])]]
        resposta = connection.send_receive(pickle.dumps([int(x) for x in comando], -1))
        connection.close()
    elif comando[0] == 'SLEEP':
        time.sleep(int(comando[1]))

    elif comando[0] == 'EXIT':
        break

    else:
        print("UNKNOWN-COMMAND")