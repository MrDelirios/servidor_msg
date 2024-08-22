import socket
import threading
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Cliente:
    def __init__(self, Host, port = 12345):
        self.host = Host 
        self.port = port
        self.senha = ""
        self.sala = []
        self.salaAtual = ""
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Estado = 0

    def receber_mensagens(self):
        while True:
            try:
                # Receber dados binários em vez de string
                dados = self.cliente_socket.recv(1024)
                if not dados:
                    print("Conexão encerrada pelo servidor.")
                    break
                dados = dados.decode('utf-8')
                if dados.startswith('/salas'):
                    _, lista_de_salas = dados.split(' ', 1)
                    self.sala = eval(lista_de_salas)
                else:
                    mensagem = self.descriptografar_mensagem(dados)
                    print(f"Mensagem recebida: {mensagem}")
            except Exception as e:
                print(f"Erro ao receber a mensagem: {e}")
                break

    def enviar_mensagens(self, mensagem):
        hash_mensagem = self.encriptar_mensagem(mensagem)
        try:
            self.cliente_socket.send(f"/mensagem {hash_mensagem}".encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar a mensagem: {e}")

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
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            
            self.Estado = 1
            
            # Criar threads para envio e recebimento de mensagens
            thread_receber = threading.Thread(target=self.receber_mensagens)
            thread_receber.start()

            thread_receber.join()

        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
        finally:
            self.cliente_socket.close()
    
    def IniciarMSG(self):
        thread_enviar = threading.Thread(target=self.enviar_mensagens)
        thread_enviar.start()
        #thread_enviar.join()

    def disconnect(self):
        try:
            self.cliente_socket.shutdown(socket.SHUT_RDWR)  # Fecha a conexão de leitura e escrita
        except Exception as e:
            print(f"Erro ao desconectar: {e}")
        finally:
            self.cliente_socket.close()

    @staticmethod
    def derivar_chave(senha):
        return hashlib.blake2b(senha.encode('utf-8')).digest()[:32]
if __name__ == "__main__":
    print("======== BlakeMSG ======== ")
    host = input("Digite o Ip do servidor no qual deseja se conectar: ")
    port = int(input("Digite a Porta: "))
    
    cliente = Cliente(host, port=port)
    Tcliente = threading.Thread(target=cliente.start)
    Tcliente.start()
    
    while cliente.Estado != 99:
        
        if cliente.Estado == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("======== BlakeMSG ========")
            cliente.senha = input("Escolha uma senha: ")
            cliente.Estado = 2
        
        elif cliente.Estado == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("======== BlakeMSG ========")
            print("Salas Disponiveis: ")
            for salas in cliente.sala:
                print(f"{salas}\n")
            In = int(input("1: Entrar 2: Criar Sala 3: Sair"))
            if In not in [1, 2, 3]:
                input("Opção invalida")

            elif In == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("======== BlakeMSG ========")
                print("Salas Disponiveis: ")
                
                for i, sala in enumerate(cliente.sala):
                    print(f"{i}: {sala}")
                try:
                    S = int(input("Escolher: "))
                    if S < 0 or S >= len(cliente.sala):
                        input("Opção inválida")
                    else:
                        cliente.Estado = 3
                        cliente.salaAtual = cliente.sala[S]
                        cliente.cliente_socket.send(f"/entrar_sala {cliente.sala[S]}".encode('utf-8'))
                except ValueError:
                    input("Opção inválida")

            elif In == 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("======== BlakeMSG ========")
                nome = input("Nome da Sala: ")
                comando = f"/criar_sala {nome}"
                cliente.cliente_socket.send(comando.encode('utf-8'))
            else:
                cliente.Estado = 99
        
        elif cliente.Estado == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"======== {cliente.salaAtual} ========")
            while cliente.Estado == 3:
                mensagem = input("Eu: ")
                mensagem = "/mensagem" + mensagem
                cliente.enviar_mensagens(mensagem)

    #cliente.disconnect()
                