import socket

class TcpServer:

    def __init__(self, sock=None):
        self.con  = ''
        self.addr = ''
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        print("Waiting for connection...")
        self.sock.bind((host, port))
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()
        print("Connected to client!")

    def send_data(self, msg):
        msgLenBytes = int(len(msg)).to_bytes(2, byteorder='big')
        msgLen = len(msg)
        self.conn.send(msgLenBytes)

        totalsent = 0
        while totalsent < msgLen:
            sent = self.conn.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent

    def recv_data(self):
        msgLen = self.sock.recv(2)

        chunks = []
        bytes_recd = 0
        while bytes_recd < msgLen:
            chunk = self.sock.recv(min(msgLen - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def close(self):
        self.sock.close()