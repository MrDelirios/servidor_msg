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
        self.servidor_socket.settimeout(1.0)  # Define um timeout para evitar bloqueios indefinidos
        self.lock = threading.Lock()
        try:
            self.servidor_socket.bind((self.host, self.port))
            self.servidor_socket.listen(5)
        except socket.error as e:
            self.output_function(f"Erro ao iniciar o servidor: {e}")
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

    def broadcast(self, mensagem, cliente_atual):
        """Envia uma mensagem para todos os clientes, exceto o cliente atual."""
        with self.lock:
            for cliente in self.clientes:
                if cliente != cliente_atual:
                    try:
                        cliente.send(mensagem)
                    except socket.error:
                        self.clientes.remove(cliente)

    def handle_client(self, cliente_socket):
        """Gerencia a comunicação com um cliente específico."""
        while True:
            try:
                dados = cliente_socket.recv(1024).decode('utf-8')
                if not dados:
                    break
                mensagem, hash_recebido = dados.split('|')

                if self.verificar_mensagem(mensagem, hash_recebido):
                    self.output_function(f"Mensagem recebida: {mensagem}")
                    self.broadcast(dados.encode('utf-8'), cliente_socket)
                else:
                    self.output_function("Mensagem corrompida ou inválida.")
            except (socket.error, ValueError) as e:
                self.output_function(f"Erro ao lidar com o cliente: {e}")
                break

        cliente_socket.close()
        with self.lock:
            self.clientes.remove(cliente_socket)

    def encriptar_mensagem(self, mensagem):
        """Gera um hash para a mensagem usando a chave secreta."""
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest()

    def verificar_mensagem(self, mensagem, hash_recebido):
        """Verifica se o hash da mensagem corresponde ao hash recebido."""
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest() == hash_recebido

    def start(self):
        """Inicia o servidor e aceita conexões de clientes."""
        self.running = True
        self.output_function(f"Servidor iniciado em {self.host}:{self.port}")
        
        while self.running:
            try:
                cliente_socket, cliente_endereco = self.servidor_socket.accept()
                self.output_function(f"Nova conexão de {cliente_endereco}")
                with self.lock:
                    self.clientes.append(cliente_socket)
                thread_cliente = threading.Thread(target=self.handle_client, args=(cliente_socket,))
                thread_cliente.start()
            except socket.timeout:
                continue  # Ignora o timeout e continua aceitando novas conexões
            except socket.error as e:
                self.output_function(f"Erro ao aceitar conexão: {e}")
                break

    def stop(self):
        """Para o servidor e fecha todas as conexões de clientes."""
        self.running = False
        # Fechar o socket do servidor para quebrar o loop de aceitação de conexões
        if self.servidor_socket:
            self.servidor_socket.close()

        # Fechar todos os sockets dos clientes
        with self.lock:
            for cliente_socket in self.clientes:
                cliente_socket.close()
            self.clientes.clear()  # Limpar a lista de clientes
