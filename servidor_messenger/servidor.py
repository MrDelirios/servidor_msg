import socket
import threading
import hashlib

class Servidor:
    def __init__(self, output_function, port=12345):
        self.host = self.get_ip_local()
        self.port = port
        self.output_function = output_function
        self.clientes = []
        self.chave_secreta = "minha-chave-secreta"
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.servidor_socket.listen(5)

    def get_ip_local(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        except:
            ip_local = '127.0.0.1'
        finally:
            s.close()
        return ip_local

    def broadcast(self, mensagem, cliente_atual):
        for cliente in self.clientes:
            if cliente != cliente_atual:
                try:
                    cliente.send(mensagem)
                except:
                    self.clientes.remove(cliente)

    def handle_client(self, cliente_socket):
        while True:
            try:
                dados = cliente_socket.recv(1024).decode('utf-8')
                mensagem, hash_recebido = dados.split('|')

                if self.verificar_mensagem(mensagem, hash_recebido):
                    self.output_function(f"Mensagem recebida: {mensagem}")
                    self.broadcast(dados.encode('utf-8'), cliente_socket)
                else:
                    self.output_function("Mensagem corrompida ou inválida.")
            except:
                break

        cliente_socket.close()
        self.clientes.remove(cliente_socket)

    def encriptar_mensagem(self, mensagem):
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest()

    def verificar_mensagem(self, mensagem, hash_recebido):
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest() == hash_recebido

    def start(self):
        self.output_function(f"Servidor iniciado em {self.host}:{self.port}")
        while True:
            cliente_socket, cliente_endereco = self.servidor_socket.accept()
            self.output_function(f"Nova conexão de {cliente_endereco}")
            self.clientes.append(cliente_socket)
            thread_cliente = threading.Thread(target=self.handle_client, args=(cliente_socket,))
            thread_cliente.start()
