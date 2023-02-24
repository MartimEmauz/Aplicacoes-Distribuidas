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
time_limits = {}

###############################################################################

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
        self.value = random.uniform(100, 200)
        self.symbol = self.name[0:3]

    def subscribe(self, client_id, time_limit):
        log[self.resource_id].append(client_id)
        time_limits[(self.resource_id, client_id)] = time_limit

    def unsubscribe (self, client_id):
        log[self.resource_id].remove(client_id)
        del time_limits[(self.resource_id, client_id)]

    def status(self, client_id):
        if client_id in log[self.resource_id]:
            return "SUBSCRIBED"
        return "UNSUBSCRIBED"
   
    def __repr__(self):
        output = ""
        output = output + "R" + self.resource_id + sorted(log[self.resource_id], key = lambda x: x[1]) + "/n"
        return output

###############################################################################

class resource_pool:
    def __init__(self, N, K, M):
        self.N = sys.argv[4] #alterar isto, são os argumentos recebidos do cliente
        self.K = sys.argv[3]
        self.M = sys.argv[2]

        for i in range(self.M):
            self.add_resource(i)

    def add_resource(self, resource_id):
        if resource_id not in pool:
            pool[resource_id] = resource(resource_id)
            log[resource_id] = []

    def clear_expired_subs(self):
        for resource_id, subs in log.items():
            for i in range(len(subs)):
                client_id, limit = subs[i]
                if time.time() > limit:
                    pool[resource_id].unsubscribe(client_id)
                    log[resource_id].pop(i)


    def subscribe(self, resource_id, client_id, time_limit):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"

        for cliente in log.values():         #se for atingido o limite de subscrições pelo cliente, NOK
            counter = 0
            if cliente == client_id:
                counter += 1
            if counter == self.K:
                return "NOK"

        if len(log[resource_id]) == self.N:        #se for atingido o limite de subscrições por recurso, NOK
            return "NOK"

        if client_id in log[resource_id]:       #se o cliente já estiver subscrito, atualizar o time limit
            time_limits[(resource_id, client_id)] = time_limit
            return "OK"

        pool[resource_id].subscribe(client_id, time_limit)
        return "OK"

    def unsubscribe (self, resource_id, client_id):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"
        
        if pool[resource_id].status(client_id) == "UNSUBSCRIBED":
            return "NOK"

        pool[resource_id].unsubscribe(client_id)
        return "OK"        

    def status(self, resource_id, client_id):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"
        return pool[resource_id].status(client_id)

    def infos(self, option, client_id):
        subscritas = []
        for i in range(self.M):
            if client_id in log[i]:
                subscritas.append(i)

        if option == "M":
                return subscritas

        if option == "K":
            return self.K - len(subscritas)            


    def statis(self, option, resource_id):
        subscritores = []
        for i in range(self.M):
            if resource_id in log[i]:
                subscritores.append(i)
        subscritores = subscritores.sort()

        n_subscritores = len(subscritores)

        if option == "L":
            return n_subscritores

        if option == "ALL":
            return self.__repr__()


    def __repr__(self):
        output = ""
        for i in range(self.M):
            output = output + pool[i].__repr__()
        return output

###############################################################################

# código do programa principal
