import socket
import threading
import hashlib
import random
from RSA import RSA
class Server:
    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.public_keys = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.rsa = RSA()

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')

            self.username_lookup[c] = username
            self.clients.append(c)
            c.send(f"{self.rsa.public_key[0]},{self.rsa.public_key[1]}".encode())

            pub_key_str = c.recv(1024).decode()
            e, n = map(int, pub_key_str.split(","))
            self.public_keys[c] = (e, n)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str, sender=None):
        h = hashlib.sha256(msg.encode()).hexdigest()
        for client in self.clients:
            if client != sender:
                encrypted = self.rsa.encrypt(msg, self.public_keys[client])
                to_send = f"{h}|{','.join(map(str, encrypted))}"
                client.send(to_send.encode())

    def handle_client(self, c: socket.socket, addr):
        while True:
            try:
                msg = c.recv(4096).decode()
                if not msg:
                    break
                print(msg)
                hash_sent, encrypted = msg.split("|")
                encrypted_msg = list(map(int, encrypted.split(",")))
                decrypted_msg = self.rsa.decrypt(encrypted_msg)

                h_calculated = hashlib.sha256(decrypted_msg.encode()).hexdigest()

                if h_calculated == hash_sent:
                    print(f"[{self.username_lookup[c]}]: {decrypted_msg}")
                    self.broadcast(f"{self.username_lookup[c]}: {decrypted_msg}", sender=c)
                else:
                    print("[warning] message hash mismatch – possibly altered")
            except:
                break

if __name__ == "__main__":
    s = Server(9001)
    s.start()
