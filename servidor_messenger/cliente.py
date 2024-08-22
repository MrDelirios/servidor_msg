import socket
import threading
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Cliente:
    def __init__(self, output_function, port=12345):
        self.host = "192.168.0.103"  
        self.port = port
        self.senha = ""
        self.sala = []
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_function = output_function  # Função de saída para a interf

    def receber_mensagens(self):
        while True:
            try:
                # Receber dados binários em vez de string
                dados = self.cliente_socket.recv(1024)
                if not dados:
                    self.output_function("Conexão encerrada pelo servidor.")
                    break
                dados = dados.decode('utf-8')
                if dados.startswith('/salas'):
                    _, lista_de_salas = dados.split(' ', 1)
                    self.sala = eval(lista_de_salas)
                    print(self.sala)
                else:
                    mensagem = self.descriptografar_mensagem(dados)
                    self.output_function(f"Mensagem recebida: {mensagem}")
            except Exception as e:
                self.output_function(f"Erro ao receber a mensagem: {e}")
                break

    def enviar_mensagens(self, mensagem):
        hash_mensagem = self.encriptar_mensagem(mensagem)
        try:
            self.cliente_socket.send(f"/mensagem {hash_mensagem}".encode('utf-8'))
            self.output_function(f"Eu: {mensagem}")
        except Exception as e:
            self.output_function(f"Erro ao enviar a mensagem: {e}")

    def encriptar_mensagem(self, mensagem):
        chave = self.derivar_chave(self.senha)
        nonce = get_random_bytes(12)
        cipher = AES.new(chave, AES.MODE_GCM, nonce=nonce)
        mensagem_criptografada, tag = cipher.encrypt_and_digest(mensagem.encode('utf-8'))
        return nonce + tag + mensagem_criptografada

    def descriptografar_mensagem(self, mensagem):
        chave = self.derivar_chave(self.senha)
        nonce = mensagem[:12]
        tag = mensagem[12:28]
        mensagem = mensagem[28:]
        cipher = AES.new(chave, AES.MODE_GCM, nonce=nonce)
        mensagem_desencriptada = cipher.decrypt_and_verify(mensagem, tag)
        return mensagem_desencriptada.decode('utf-8')

    def start(self):
        try:
            self.cliente_socket.connect((self.host, self.port))
            self.cliente_socket.send("/get".encode('utf-8'))
            #self.output_function(f"Conectado ao servidor em {self.host}:{self.port}")

            # Criar threads para envio e recebimento de mensagens
            thread_receber = threading.Thread(target=self.receber_mensagens)
            thread_receber.start()

            thread_receber.join()

        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
        finally:
            self.cliente_socket.close()
    
    def disconnect(self):
        try:
            self.cliente_socket.shutdown(socket.SHUT_RDWR)  # Fecha a conexão de leitura e escrita
        except Exception as e:
            self.output_function(f"Erro ao desconectar: {e}")
        finally:
            self.cliente_socket.close()

    @staticmethod
    def derivar_chave(senha):
        return hashlib.blake2b(senha.encode('utf-8')).digest()[:32]
