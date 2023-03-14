import time
from net_client import server_connection
import pickle


class TickerStub:
    def __init__(self, host, port, client_id):
        self.conn_sock = server_connection(host, port)
        self.comandos = {
            'SUBSCR': 10,
            'CANCEL': 20,
            'STATUS': 30,
            'INFOS M': 40,
            'INFOS K': 50,
            'STATIS L': 60,
            'STATIS ALL': 70,
        }
        self.client_id = client_id

    def connect(self):
        self.conn_sock.connect()

    def disconnect(self):
        # Fecha a ligação conn_sock
        # Métodos tradicionais de um objeto do tipo lista
        self.conn_sock.close()

    def comando(self, comando):
        # Envia o comando para o servidor
        # Retorna a resposta do servidor
        connection = self.conn_sock
        self.connect()
        if comando[0] == 'SUBSCR':
            if len(comando) <= 2:
                return "MISSING-ARGUMENTS"

            else:
                comando[0] = self.comandos[comando[0]]
                comando.append(self.client_id)
                connection.send_receive(pickle.dumps(
                    [int(x) for x in comando], -1))

        elif comando[0] == 'CANCEL':
            if len(comando) < 2:
                return "MISSING-ARGUMENTS"

            else:

                comando[0] = self.comandos[comando[0]]
                comando.append(self.client_id)
                resposta = connection.send_receive(
                    pickle.dumps([int(x) for x in comando], -1))

        elif comando[0] == 'STATUS':
            if len(comando) < 2:
                return "MISSING-ARGUMENTS"

            else:

                comando[0] = self.comandos[comando[0]]
                comando.append(self.client_id)
                resposta = connection.send_receive(
                    pickle.dumps([int(x) for x in comando], -1))

        elif comando[0] == 'INFOS' and comando[1] == 'M':
            if len(comando) < 2:
                return "MISSING-ARGUMENTS"

            comando = [self.comandos[" ".join(comando[0:2])]]
            comando.append(self.client_id)
            resposta = connection.send_receive(
                pickle.dumps([int(x) for x in comando], -1))

        elif comando[0] == 'INFOS' and comando[1] == 'K':
            if len(comando) < 2:
                return "MISSING-ARGUMENTS"

            comando = [self.comandos[" ".join(comando[0:2])]]
            comando.append(self.client_id)
            resposta = connection.send_receive(
                pickle.dumps([int(x) for x in comando], -1))

        elif comando[0] == 'STATIS' and comando[1] == 'L':
            if len(comando) <= 2:
                return "MISSING-ARGUMENTS"
            else:

                newComando = [self.comandos[" ".join(comando[0:2])]]
                newComando.append(comando[2])
                resposta = connection.send_receive(
                    pickle.dumps([int(x) for x in newComando], -1))

        elif comando[0] == 'STATIS' and comando[1] == 'ALL':
            if len(comando) < 2:
                return "MISSING-ARGUMENTS"

            comando = [self.comandos[" ".join(comando[0:2])]]
            resposta = connection.send_receive(
                pickle.dumps([int(x) for x in comando], -1))
        elif comando[0] == 'SLEEP':
            time.sleep(int(comando[1]))

        elif comando[0] == 'EXIT':
            self.disconnect()
            return "EXIT"

        else:
            return "UNKNOWN-COMMAND"
