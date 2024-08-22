import socket
import threading
import hashlib

class Servidor:
    def __init__(self, output_function, port=12345):
        self.host = self.get_ip_local()
        self.port = port
        self.output_function = output_function
        self.clientes = []
        self.salas = {}  # Armazena informações das salas {nome_sala: {'senha': senha, 'clientes': [cliente_socket]}}
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

    def broadcast(self, mensagem, sala, cliente_atual):
        """Envia uma mensagem para todos os clientes na sala, exceto o cliente atual."""
        sala_info = self.salas.get(sala)
        if sala_info:
            with self.lock:
                for cliente in sala_info['clientes']:
                    if cliente != cliente_atual:
                        try:
                            cliente.send(mensagem)
                        except socket.error:
                            sala_info['clientes'].remove(cliente)

    def handle_client(self, cliente_socket):
        """Gerencia a comunicação com um cliente específico."""
        try:
            while True:
               # Receber dados binários em vez de string
                dados = cliente_socket.recv(1024)
                if not dados:
                    self.output_function("Conexão encerrada pelo servidor.")
                    break
                dados = dados.decode('utf-8')
                print(dados)
                if dados.startswith('/criar_sala'):
                    # Criação de sala: /criar_sala nome_sala 
                    _, nome_sala = dados.split(' ', 1)
                    if nome_sala not in self.salas:
                        self.salas[nome_sala] = {'clientes': [cliente_socket]}
                        self.output_function(f"Sala '{nome_sala}' criada com sucesso.")
                    else:
                        cliente_socket.send("Sala já existe.".encode('utf-8'))
                
                elif dados.startswith('/entrar_sala'):
                    # Entrada na sala: /entrar_sala nome_sala senha
                    _, nome_sala, senha = dados.split(' ', 2)
                    sala_info = self.salas.get(nome_sala)
                    if sala_info and sala_info['senha'] == senha:
                        sala_info['clientes'].append(cliente_socket)
                        self.output_function(f"Cliente entrou na sala '{nome_sala}'.")
                    else:
                        cliente_socket.send("Senha inválida ou sala não existe.".encode('utf-8'))
                
                elif dados.startswith('/sair_sala '):
                    # Saída da sala: /sair_sala nome_sala
                    _, nome_sala = dados.split(' ', 1)
                    sala_info = self.salas.get(nome_sala)
                    if sala_info and cliente_socket in sala_info['clientes']:
                        sala_info['clientes'].remove(cliente_socket)
                        self.output_function(f"Cliente saiu da sala '{nome_sala}'.")
                
                elif dados.startswith('/mensagem'):
                    # Envio de mensagem: /mensagem nome_sala mensagem
                    _, nome_sala, mensagem = dados.split(' ', 2)
                    sala_info = self.salas.get(nome_sala)
                    if sala_info:
                        self.broadcast(mensagem, nome_sala, cliente_socket)
                    else:
                        cliente_socket.send("Sala não encontrada.".encode('utf-8'))
                elif dados.startswith('/get'):
                    lista_salas = [key for key in self.salas]
                    cliente_socket.send(f"/salas {lista_salas}".encode('utf-8'))
                else:
                    cliente_socket.send("Comando inválido.".encode('utf-8'))
        
        except Exception as e:
            self.output_function(f"Erro ao lidar com o cliente: {e}")
        finally:
            cliente_socket.close()
            self.remover_cliente(cliente_socket)

    def remover_cliente(self, cliente_socket):
        """Remove um cliente de todas as salas em que está presente."""
        for sala_info in self.salas.values():
            if cliente_socket in sala_info['clientes']:
                sala_info['clientes'].remove(cliente_socket)

    def start(self):
        """Inicia o servidor e aceita conexões de clientes."""
        self.running = True
        self.output_function(f"Servidor iniciado em {self.host}:{self.port}")
        
        while self.running:
            try:
                cliente_socket, cliente_endereco = self.servidor_socket.accept()
                self.output_function(f"Nova conexão de {cliente_endereco}")
                with self.lock: self.clientes.append(cliente_socket)
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
            for cliente_socket in self.clientes.values():
                cliente_socket.close()
            self.clientes.clear()  # Limpar a lista de clientes
