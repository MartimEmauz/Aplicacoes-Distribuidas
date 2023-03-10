# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: 27
Números de aluno: 58668 | 58621
"""

# zona para fazer importação

import sock_utils as utils
import socket as s

# definição da classe server_connection 

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = None
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        sock = utils.create_tcp_client_socket(self.address, self.port)
        self.sock = sock

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e imprime
        a resposta recebida pela mesma socket.
        """
        self.sock.sendall(data)
        resposta = self.sock.recv(1024)
        print(resposta.decode())
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
