#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 27
Números de aluno: 58668 | 58621
"""

# Zona para fazer importação

import sock_utils as utils
import socket as s
import sys
import time
import random
import string

# Definição de constantes

log = {}
pool = {}

HOST = sys.argv[1]
PORT = int(sys.argv[2])

###############################################################################

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
        self.value = random.uniform(100, 200)
        self.symbol = self.name[0:3]
        self.pool = pool

    def subscribe(self, client_id, time_limit):
        if int(client_id) not in log[self.resource_id]:
            log[self.resource_id].append(int(client_id))
        self.pool.time_limits[(self.resource_id, int(client_id))] = time.time() + float(time_limit)

    def unsubscribe (self, client_id):
        if int(client_id) in log[self.resource_id]:
            log[self.resource_id].remove(int(client_id))
            del self.pool.time_limits[(self.resource_id, int(client_id))]

    def status(self, client_id):
        if int(client_id) in log[self.resource_id]:
            return ("SUBSCRIBED")
        else:
            return ("UNSUBSCRIBED")
        
   
    def __repr__(self):
        output = ""
        output += "R", self.resource_id, sorted(log[self.resource_id], key = lambda x: x[1]), "\n"
        return output

###############################################################################

class resource_pool:
    def __init__(self, M, K, N):
        self.M = M
        self.K = K
        self.N = N
        self.resources = []
        self.time_limits = {}

        for resource in range(self.M):
            self.add_resource(resource)

    def add_resource(self, resource_id):
        if resource_id not in pool:
            pool[resource_id] = resource(resource_id)
            log[resource_id] = []
            self.resources.append(resource_id)

    def clear_expired_subs(self):
        for resource_id in self.resources:
            for client_id in log[resource_id]:
                if time.time() > self.time_limits[(resource_id, client_id)]:
                    resource(resource_id).unsubscribe(client_id)
                
        

    def subscribe(self, resource_id, client_id, time_limit):
        if resource_id not in self.resources:
            return "UNKNOWN-RESOURCE"

        if len(log[resource_id]) == self.N:        #se for atingido o limite de subscrições por recurso, NOK
            return "NOK"
        
        counter = 0
        for client in log.values():         #se for atingido o limite de subscrições pelo cliente, NOK
            if client_id in client:
                print("entrou no if")
                counter += 1
            if counter >= self.K:
                return "NOK"
            
        if client_id in log[resource_id]:       #se o cliente já estiver subscrito, atualizar o time limit ! N FUNCIONA
            resource(resource_id).subscribe(client_id, time_limit)
            self.time_limits[(resource_id, client_id)] = time.time() + float(time_limit) #DESNECESSARIO
            return "OK"
        
        resource(resource_id).subscribe(client_id, time_limit)
        return "OK"

    def unsubscribe (self, resource_id, client_id):
        if resource_id not in self.resources:
            return "UNKNOWN-RESOURCE"
        
        if resource(resource_id).status(client_id) == "UNSUBSCRIBED":
            return "NOK"

        resource(resource_id).unsubscribe(client_id)
        return "OK"
        
               

    def status(self, resource_id, client_id):
        if resource_id not in self.resources:
            return "UNKNOWN-RESOURCE"
        return resource(resource_id).status(client_id)

    def infos(self, option, client_id):
        subscribed = []
        for i in range(self.M):
            if int(client_id) in log[i]:
                subscribed.append(i)

        if option == "M":
            output = ' '.join([str(sub) for sub in subscribed])
            return output

        if option == "K":
            return str(self.K - len(subscribed))


    def statis(self, option, resource_id):
        subscribers = []
        for i in range(self.M):
            if resource_id in log.keys():
                subscribers.append(i)
        subscribers = subscribers.sort()

        print(log.keys())

        print(subscribers)
        print(type(subscribers))

        n_subscribers = len(subscribers)

        if option == "L":
            return str(n_subscribers)

        if option == "ALL":
            return self.__repr__()


    def __repr__(self):
        output = ""
        for i in range(self.M):
            output = output + pool[i].__repr__()
        return output

###############################################################################

# código do programa principal 

sock = utils.create_tcp_server_socket(HOST, PORT, 1000)
pool = resource_pool(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))


try:
    while True:
        print("log: ", log)
        print("time_limits: ", pool.time_limits, "\n")

        pool.clear_expired_subs()

        (conn_sock, (HOST, PORT)) = sock.accept()

        print('Ligado a %s no porto %s' % (HOST,PORT), "\n")

        received = conn_sock.recv(1024).decode()
        received = received.split(" ")
        print("received: ", received)

        

        if received[0] == "SUBSCR": #está a funcionar
            arguments = received[1:]
            resource_id, client_id, time_limit = arguments
            send = pool.subscribe(int(resource_id), float(time_limit), client_id)
            conn_sock.send(send.encode())

        if received[0] == "CANCEL":
            arguments = received[1:]
            resource_id, client_id = arguments
            send = pool.unsubscribe(int(resource_id), client_id)
            conn_sock.send(send.encode())

        if received[0] == "STATUS":
            arguments = received[1:]
            resource_id, client_id = arguments
            send = pool.status(int(resource_id), client_id)
            conn_sock.send(send.encode())

        if received[0] == "INFOS":
            if received[1] == "M":
                print("entrou no M")
                send = pool.infos("M", received[2])
                print(send)
                conn_sock.send(send.encode())

            if received[1] == "K":
                send = pool.infos("K", received[2])
                conn_sock.send(send.encode())

        if received[0] == "STATIS":
            if received[1] == "L":
                send = pool.statis("L", int(received[2]))
                conn_sock.send(send.encode())

            if received[1] == "ALL":
                send = pool.statis("ALL", int(received[2]))
                conn_sock.send(send.encode())
        

finally:
    sock.close()

#problemas:
#ainda não verifiquei o funcionamento do comando statis