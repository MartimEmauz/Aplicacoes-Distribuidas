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
from ticker_stub import TickerStub as Ticker

# Programa principal

# Definição de constantes
client_id = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

stub = Ticker(HOST, PORT, client_id)

stub.connect()

while True:
    
    comando = str(input("Comando > "))
    print(comando)
    comando = comando.split(" ")
    stub.comando(comando)

