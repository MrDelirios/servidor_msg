import socket
import threading

class Servidor:
    def __init__(self, port=12345):
        self.host = self.get_ip_local()  # Detecta o IP local automaticamente
        self.port = port
        self.clientes = []
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.servidor_socket.listen(5)  # Aceita até 5 conexões simultâneas

    def get_ip_local(self):
        # Descobre o IP local conectando-se a um servidor externo fictício
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Conectar-se a um endereço externo
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        except Exception as e:
            ip_local = '127.0.0.1'  # Caso ocorra algum problema, utiliza localhost
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
                mensagem = cliente_socket.recv(1024)
                if mensagem:
                    print(f"Mensagem recebida: {mensagem.decode('utf-8')}")
                    self.broadcast(mensagem, cliente_socket)
                else:
                    break
            except:
                break

        cliente_socket.close()
        self.clientes.remove(cliente_socket)

    def start(self):
        print(f"Servidor iniciado em {self.host}:{self.port}")
        while True:
            cliente_socket, cliente_endereco = self.servidor_socket.accept()
            print(f"Nova conexão de {cliente_endereco}")
            self.clientes.append(cliente_socket)
            thread_cliente = threading.Thread(target=self.handle_client, args=(cliente_socket,))
            thread_cliente.start()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()
