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

# Definição de constantes

#dicionário com os recursos e os clientes que estão subscritos
log = {}
pool = {}

###############################################################################

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id

    def subscribe(self, client_id, time_limit):
        log[self.resource_id].append(client_id)

        inicio = time.time()
        fim = inicio + time_limit

    """         if fim <= inicio:
            log[self.resource_id].remove(client_id) """
            #ideia inicial (não é suposto ser aqui) - ver a função clear_expired_subs

    def unsubscribe (self, client_id):
        log[self.resource_id].remove(client_id)

    def status(self, client_id):
        if client_id in log[self.resource_id]:
            return "SUBSCRIBED"
        else:
            return "UNSUBSCRIBED"
   
    def __repr__(self):
        output = ""
        # R <resource_id> <list of subscribers>
        return output
        #não percebo o que é que isto faz

###############################################################################

class resource_pool:
    def __init__(self, N, K, M):
        self.N = sys.argv[4]
        self.K = sys.argv[3]
        self.M = sys.argv[2]
        
    def clear_expired_subs(self):
        pass # Remover esta linha e fazer implementação da função
    #problema: como armazenar o tempo limite de cada subscrição? outro dicionário com o par (subscrição (id do recurso; id do cliente), tempo limite)?


    def subscribe(self, resource_id, client_id, time_limit):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"

        #se for atingido o limite de subscrições pelo cliente, NOK
        #problema: como saber quantas subscrições tem o cliente? fazer uma busca no dicionário log?

        if len(log[resource_id]) == self.N:        #se for atingido o limite de subscrições por recurso, NOK
            return "NOK"

        #se o cliente já estiver subscrito, atualizar o time limit

        else:
            pool[resource_id].subscribe(client_id, time_limit)
            return "OK"

    def unsubscribe (self, resource_id, client_id):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"
        
        if resource.status(resource_id, client_id) == "UNSUBSCRIBED":
            return "NOK"

        else:
            pool[resource_id].unsubscribe(client_id)
            return "OK"        

    def status(self, resource_id, client_id):
        if resource_id not in pool:
            return "UNKNOWN-RESOURCE"

        else:
            return pool[resource_id].status(client_id)

    def infos(self, option, client_id):
        pass # Remover esta linha e fazer implementação da função

    def statis(self, option, resource_id):
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # Acrescentar no output uma linha por cada recurso
        return output

###############################################################################

# código do programa principal
