import socket
import threading
<<<<<<< HEAD

class Cliente:
    def __init__(self, port=12345):
        self.host = self.get_ip_local()  # Detecta o IP local automaticamente
        self.port = port
=======
import hashlib

class Cliente:
    def __init__(self, port=12345):
        self.host = self.get_ip_local()
        self.port = port
        self.chave_secreta = "minha-chave-secreta"
>>>>>>> 5553f2cb832bced254ee39ca90a01eb8fbda9a21
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receber_mensagens(self):
        while True:
            try:
<<<<<<< HEAD
                mensagem = self.cliente_socket.recv(1024).decode('utf-8')
                if mensagem:
                    print(f"\nMensagem recebida: {mensagem}")
                else:
                    print("Conexão encerrada pelo servidor.")
                    break
=======
                dados = self.cliente_socket.recv(1024).decode('utf-8')
                mensagem, hash_recebido = dados.split('|')
                if self.verificar_mensagem(mensagem, hash_recebido):
                    print(f"Mensagem recebida: {mensagem}")
                else:
                    print("Mensagem corrompida ou inválida.")
>>>>>>> 5553f2cb832bced254ee39ca90a01eb8fbda9a21
            except:
                print("Erro ao receber a mensagem.")
                break

    def enviar_mensagens(self):
        while True:
<<<<<<< HEAD
            mensagem = input()
            try:
                self.cliente_socket.send(mensagem.encode('utf-8'))
            except:
                print("Erro ao enviar a mensagem.")
                break
    
    def get_ip_local(self):
        # Descobre o IP local conectando-se a um servidor externo fictício
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Conectar-se a um endereço externo
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        except Exception as e:
            ip_local = '127.0.0.1'  # Caso ocorra algum problema, utiliza localhost
=======
            mensagem = input("Você: ")
            hash_mensagem = self.encriptar_mensagem(mensagem)
            try:
                self.cliente_socket.send(f"{mensagem}|{hash_mensagem}".encode('utf-8'))
                print(mensagem, hash_mensagem)
            except:
                print("Erro ao enviar a mensagem.")
                break

    def encriptar_mensagem(self, mensagem):
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest()

    def verificar_mensagem(self, mensagem, hash_recebido):
        h = hashlib.blake2b(key=self.chave_secreta.encode('utf-8'))
        h.update(mensagem.encode('utf-8'))
        return h.hexdigest() == hash_recebido

    def get_ip_local(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        except:
            ip_local = '127.0.0.1'
>>>>>>> 5553f2cb832bced254ee39ca90a01eb8fbda9a21
        finally:
            s.close()
        return ip_local

    def start(self):
        try:
            self.cliente_socket.connect((self.host, self.port))
            print(f"Conectado ao servidor em {self.host}:{self.port}")

            # Criar threads para envio e recebimento de mensagens
            thread_receber = threading.Thread(target=self.receber_mensagens)
            thread_receber.start()

            thread_enviar = threading.Thread(target=self.enviar_mensagens)
            thread_enviar.start()

            thread_receber.join()
            thread_enviar.join()

        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
        finally:
            self.cliente_socket.close()
<<<<<<< HEAD
    
=======

if __name__ == "__main__":
    cliente = Cliente()
    cliente.start()
>>>>>>> 5553f2cb832bced254ee39ca90a01eb8fbda9a21
