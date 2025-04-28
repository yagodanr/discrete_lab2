import hashlib
import random
import socket
import threading

from RSA import RSA


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.rsa = RSA()

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # receive server public key
        server_key_str = self.s.recv(1024).decode()
        self.server_public_key = tuple(map(int, server_key_str.split(",")))

        # send own public key
        self.s.send(f"{self.rsa.public_key[0]},{self.rsa.public_key[1]}".encode())

        threading.Thread(target=self.read_handler).start()
        threading.Thread(target=self.write_handler).start()

    def read_handler(self):
        while True:
            try:
                data = self.s.recv(4096).decode()
                h_received, encrypted_str = data.split("|")
                encrypted_msg = list(map(int, encrypted_str.split(",")))
                decrypted_msg = self.rsa.decrypt(encrypted_msg)

                h_calculated = hashlib.sha256(decrypted_msg.encode()).hexdigest()

                if h_received == h_calculated:
                    print(decrypted_msg)
                else:
                    print("[warning] received message failed integrity check")
            except:
                break

    def write_handler(self):
        while True:
            message = input()
            h = hashlib.sha256(message.encode()).hexdigest()
            encrypted = self.rsa.encrypt(message, self.server_public_key)
            to_send = f"{h}|{','.join(map(str, encrypted))}"
            self.s.send(to_send.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
