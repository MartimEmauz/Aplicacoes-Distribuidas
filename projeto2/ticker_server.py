#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 27
Números de aluno: 58668 | 58621
"""

# Zona para fazer importação

import pickle
import sock_utils as utils
import socket as s
import sys
import time
import random
import string

# Definição de constantes

log = {}  # dicionario com os IDs dos recursos e os clientes que os subscreveram
pool = {}  # dicionario com os IDs dos recursos e os recursos correspondentes

HOST = sys.argv[1]
PORT = int(sys.argv[2])

###############################################################################


class resource:
    def __init__(self, resource_id):
        """Inicializa um recurso.

        Args:
            resource_id (int): Identificador do recurso.

        Attributes:
            resource_id (int): Identificador do recurso.
            name (str): Nome do recurso.
            value (float): Valor do recurso.
            symbol (str): Símbolo do recurso.
            pool (resource_pool): Pool de recursos.
        """
        self.resource_id = resource_id
        self.name = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(7))
        self.value = random.uniform(100, 200)
        self.symbol = self.name[0:3]
        self.pool = pool

    def subscribe(self, client_id, time_limit):
        """Subscreve um cliente num recurso.

        Args:
            client_id (int): Identificador do cliente.
            time_limit (float): Limite de tempo de subscrição.
        """
        if int(client_id) not in log[self.resource_id]:
            log[self.resource_id].append(int(client_id))
        self.pool.time_limits[(self.resource_id, int(
            client_id))] = time.time() + float(time_limit)

    def unsubscribe(self, client_id):
        """Cancela a subscrição de um cliente num recurso.

        Args:
            client_id (int): Identificador do cliente.                 
        """
        if int(client_id) in log[self.resource_id]:
            log[self.resource_id].remove(int(client_id))
            del self.pool.time_limits[(self.resource_id, int(client_id))]

    def status(self, client_id):
        """Verifica se um cliente está subscrito num recurso.

        Args:
            client_id (int): Identificador do cliente.

        Returns:
            str: "SUBSCRIBED" se o cliente estiver subscrito, "UNSUBSCRIBED" caso contrário.
        """
        if int(client_id) in log[self.resource_id]:
            return "SUBSCRIBED"
        else:
            return "UNSUBSCRIBED"

    def __repr__(self):
        """Devolve a representação textual de um recurso.

        Returns:
            str: Representação textual de um recurso, contendo o seu ID, o número atual de subscritores desse recurso, e a lista de clientes subscritos do recurso.
        """
        output = []
        for client in log[self.resource_id]:
            output.append(client)
        if len(output) <= 0:
            output.append(None)
        return output

###############################################################################


class resource_pool:
    def __init__(self, M, K, N):
        """Inicializa um pool de recursos.

        Args:
            M (int): Número de recursos.
            K (int): Número máximo de subscrições por cliente.
            N (int): Número máximo de subscrições por recurso.

        Attributes:
            M (int): Número de recursos.
            K (int): Número máximo de subscrições por cliente.
            N (int): Número máximo de subscrições por recurso.
            resources (list): Lista com os IDs dos recursos.
            time_limits (dict): Dicionário com os limites de tempo das subscrições.
        """
        self.M = M
        self.K = K
        self.N = N
        self.resources = []
        self.time_limits = {}

        for resource in range(1, self.M+1):
            self.add_resource(resource)

    def add_resource(self, resource_id):
        """Adiciona um recurso à pool.

        Args:
            resource_id (int): Identificador do recurso.
        """
        if resource_id not in pool:
            pool[resource_id] = resource(resource_id)
            log[resource_id] = []
            self.resources.append(resource_id)

    def clear_expired_subs(self):
        """Cancela as subscrições expiradas.
        """
        for resource_id in self.resources:
            for client_id in log[resource_id]:
                if time.time() > self.time_limits[(resource_id, client_id)]:
                    resource(resource_id).unsubscribe(client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        """Subscreve um cliente num recurso.

        Args:
            resource_id (int): Identificador do recurso.
            client_id (int): Identificador do cliente.
            time_limit (float): Limite de tempo de subscrição.

        Returns:
            boolean: True se a subscrição for bem sucedida, False ou None caso contrário.
        """
        if resource_id not in self.resources:  # se o recurso não existir, retornar None
            return None

        # se for atingido o limite de subscrições por recurso, retornar False
        if len(log[resource_id]) == self.N:
            return False

        counter = 0
        for client in log.values():
            if client_id in client:
                counter += 1
            if counter >= self.K:  # se for atingido o limite de subscrições pelo cliente, retornar False
                return False

        # se o cliente já estiver subscrito, atualizar o time limit e retornar True
        if client_id in log[resource_id]:
            resource(resource_id).subscribe(client_id, time_limit)
            self.time_limits[(resource_id, client_id)
                             ] = time.time() + float(time_limit)
            return True

        resource(resource_id).subscribe(client_id, time_limit)
        return True

    def unsubscribe(self, resource_id, client_id):
        """Cancela a subscrição de um cliente num recurso.

        Args:
            resource_id (int): Identificador do recurso.
            client_id (int): Identificador do cliente.

        Returns:
            boolean: True se a subscrição for cancelada, False ou None caso contrário.
        """
        if resource_id not in self.resources:  # se o recurso não existir, retornar "UNKNOWN-RESOURCE"
            return None

        # se o cliente não estiver subscrito, retornar "NOK"
        if not resource(resource_id).status(client_id):
            return False

        # se o cliente estiver subscrito, cancelar a subscrição e retornar "OK"
        resource(resource_id).unsubscribe(client_id)
        return True

    def status(self, resource_id, client_id):
        """Verifica o estado de subscrição de um cliente num recurso.

        Args:
            resource_id (int): Identificador do recurso.
            client_id (int): Identificador do cliente.

        Returns:
            str: "SUBSCRIBED" se o cliente estiver subscrito, "UNSUBSCRIBED" caso contrário.
        """
        if resource_id not in self.resources:  # se o recurso não existir, retornar "UNKNOWN-RESOURCE"
            return None
        return resource(resource_id).status(client_id)

    def infos(self, option, client_id):
        """Devolve informações sobre os recursos subscritos por um cliente.

        Args:
            option (str): Opção de informação.
            client_id (int): Identificador do cliente.

        Returns:
            int: Informação sobre os recursos subscritos por um cliente.
        """
        subscribed = []
        for i in range(self.M):
            if int(client_id) in log[i]:
                subscribed.append(i)

        if option == "M":  # Se a opção for M, devolve o número de recursos subscritos pelo cliente
            return [sub for sub in subscribed]

        if option == "K":  # Se a opção for K, devolve o número de subscrições disponíveis para o cliente
            return self.K - len(subscribed)

    def statis(self, option, resource_id=None):
        """Devolve informações sobre um ou todos os recursos.

        Args:
            option (str): Opção de informação.
            resource_id (int): Identificador do recurso.

        Returns:
            int: Informação sobre os recursos.
        """
        if resource_id != None:
            subscribers = 0
            if resource_id in log.keys():
                for i in log[resource_id]:
                    subscribers += 1

        if option == "L":  # Se a opção for L, devolve o número de subscrições ativas para um dado recurso
            return subscribers

        if option == "ALL":  # Se a opção for ALL, devolve a representação textual de todos os recursos
            return self.__repr__()

    def __repr__(self):
        output = []
        for rec in self.resources:
            recurso = resource(rec)
            output.append(recurso.__repr__())
        return output

###############################################################################

# código do programa principal


sock = utils.create_tcp_server_socket(HOST, PORT, 1000)  # cria um socket TCP
pool = resource_pool(int(sys.argv[3]), int(sys.argv[4]), int(
    sys.argv[5]))  # cria uma pool de recursos


try:
    while True:
        """ 
        print("log: ", log) #para debug
        print("time_limits: ", pool.time_limits) #para debug
        """

        (conn_sock, (HOST, PORT)) = sock.accept()

        # ligado = ('Ligado a %s no porto %s' % (HOST,PORT))
        # print(ligado)

        pool.clear_expired_subs()

        terminado = "Ligação terminada"

        received = pickle.loads(utils.receive_all(conn_sock, 1024))
        ligado = [int(received[0])+1]
        print("Comando > ", received)

        if received[0] == 10:
            arguments = received[1:]
            resource_id, client_id, time_limit = arguments
            send = ligado
            send.append(pool.subscribe(int(resource_id),
                        float(time_limit), client_id))
            # print(pool.subscribe(int(resource_id), float(time_limit), client_id))
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 20:
            arguments = received[1:]
            resource_id, client_id = arguments
            send = ligado
            send.append(pool.unsubscribe(int(resource_id), client_id))
            print(pool.unsubscribe(int(resource_id), client_id))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 30:
            arguments = received[1:]
            resource_id, client_id = arguments
            send = ligado
            send.append(pool.status(int(resource_id), client_id))
            print(pool.status(int(resource_id), client_id))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 40:
            send = ligado
            send.append(pool.infos("M", received[1]))
            print(pool.infos("M", received[1]))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 50:
            send = ligado
            send.append(pool.infos("K", received[1]))
            print(pool.infos("K", received[1]))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 60:
            send = ligado
            print(received)
            send.append(pool.statis("L", int(received[1])))
            print(pool.statis("L", int(received[1])))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        if received[0] == 70:
            send = ligado
            for x in pool.statis("ALL"):
                send.append(x)
            print(pool.statis("ALL"))
            # send += terminado
            conn_sock.send(pickle.dumps(send, -1))

        print(terminado, "\n")

finally:
    sock.close()
