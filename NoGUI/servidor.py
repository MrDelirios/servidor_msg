import socket
import threading
import hashlib

class Servidor:
    def __init__(self, port=12345):
        self.host = self.get_ip_local()
        self.port = port
        self.clientes = []  # Lista de clientes conectados
        self.salas = {}  # Armazena informações das salas {nome_sala: {'clientes': [cliente_socket]}}

        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.settimeout(1.0)  # Define um timeout para evitar bloqueios indefinidos
        self.lock = threading.Lock()

        try:
            self.servidor_socket.bind((self.host, self.port))
            self.servidor_socket.listen(5)
        except socket.error as e:
            print(f"Erro ao iniciar o servidor: {e}")
            raise

    def get_ip_local(self):
        """Obtém o IP local da máquina."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        except socket.error as e:
            ip_local = '127.0.0.1'
        finally:
            s.close()
        return ip_local

    def broadcast(self, mensagem, sala, cliente_atual):
        """Envia uma mensagem para todos os clientes na sala, exceto o cliente atual."""
        sala_info = self.salas.get(sala)
        if sala_info:
            with self.lock:
                for cliente in sala_info['clientes']:
                    if cliente != cliente_atual:
                        try:
                            cliente.sendall(mensagem)
                        except socket.error:
                            sala_info['clientes'].remove(cliente)

    def handle_client(self, cliente_socket):
        """Gerencia a comunicação com um cliente específico."""
        try:
            while True:
                # Receber dados binários
                dados = cliente_socket.recv(1024)
                if not dados:
                    print("Conexão encerrada pelo cliente.")
                    break
                
                # Decodificar a mensagem
                mensagem = dados.decode('utf-8')
                
                if mensagem.startswith('/criar_sala'):
                    print(f"Cliente{cliente_socket.getpeername()} solicitou: {mensagem}")
                    # Criação de sala: /criar_sala nome_sala
                    _, nome_sala = mensagem.split(' ', 1)
                    if nome_sala not in self.salas:
                        self.salas[nome_sala] = {'clientes': [cliente_socket]}
                        print(f"Sala '{nome_sala}' criada com sucesso.")
                    else:
                        cliente_socket.send("Sala já existe.".encode('utf-8'))
                
                elif mensagem.startswith('/entrar_sala'):
                    print(f"Cliente{cliente_socket.getpeername()} solicitou: {mensagem}")
                    # Entrada na sala: /entrar_sala nome_sala
                    _, nome_sala = mensagem.split(' ', 1)
                    sala_info = self.salas.get(nome_sala)
                    if sala_info:
                        sala_info['clientes'].append(cliente_socket)
                        print(f"Cliente entrou na sala '{nome_sala}'.")
                    else:
                        cliente_socket.send("Sala não encontrada.".encode('utf-8'))
                
                elif mensagem.startswith('/sair_sala'):
                    print(f"Cliente{cliente_socket.getpeername()} solicitou: {mensagem}")
                    # Saída da sala: /sair_sala nome_sala
                    _, nome_sala = mensagem.split(' ', 1)
                    sala_info = self.salas.get(nome_sala)
                    if sala_info and cliente_socket in sala_info['clientes']:
                        sala_info['clientes'].remove(cliente_socket)
                        print(f"Cliente saiu da sala '{nome_sala}'.")
                
                elif mensagem.startswith('/mensagem'):
                    # Envio de mensagem: /mensagem mensagem
                    _, msg = mensagem.split(' ', 1)
                    sala_info = self.encontrar_sala_cliente(cliente_socket)
                    if sala_info:
                        print(f"Cliente{cliente_socket.getpeername()} Enviou: {msg} para sala: {sala_info}")
                        self.broadcast(msg.encode('utf-8'), sala_info, cliente_socket)
                    else:
                        cliente_socket.send("Sala não encontrada.".encode('utf-8'))
                
                elif mensagem.startswith('/get'):
                    lista_salas = [key for key in self.salas]
                    cliente_socket.send(f"/salas {lista_salas}".encode('utf-8'))
                
                else:
                    cliente_socket.send("Comando inválido.".encode('utf-8'))
        
        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}")
        finally:
            cliente_socket.close()
            self.remover_cliente(cliente_socket)

    def remover_cliente(self, cliente_socket):
        """Remove um cliente de todas as salas em que está presente e da lista de clientes."""
        for sala_info in self.salas.values():
            if cliente_socket in sala_info['clientes']:
                sala_info['clientes'].remove(cliente_socket)
        with self.lock:
            if cliente_socket in self.clientes:
                self.clientes.remove(cliente_socket)

    def start(self):
        """Inicia o servidor e aceita conexões de clientes."""
        self.running = True
        print(f"Servidor iniciado em {self.host}:{self.port}")
        
        while self.running:
            try:
                cliente_socket, cliente_endereco = self.servidor_socket.accept()
                print(f"Nova conexão de {cliente_endereco}")
                with self.lock:
                    self.clientes.append(cliente_socket)
                thread_cliente = threading.Thread(target=self.handle_client, args=(cliente_socket,))
                thread_cliente.start()
            except socket.timeout:
                continue  # Ignora o timeout e continua aceitando novas conexões
            except socket.error as e:
                print(f"Erro ao aceitar conexão: {e}")
                break

    def stop(self):
        """Encerra o servidor e fecha todos os sockets."""
        self.running = False
        if self.servidor_socket:
            self.servidor_socket.close()
        with self.lock:
            for sala_info in self.salas.values():
                for cliente_socket in sala_info['clientes']:
                    cliente_socket.close()
            self.clientes.clear()

    def encontrar_sala_cliente(self, cliente_socket):
        """Encontra a sala em que o cliente está presente."""
        for nome_sala, sala_info in self.salas.items():
            if cliente_socket in sala_info['clientes']:
                return nome_sala
        return None

if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()
