import select
import socket

BUFSIZE = 2048


class SocketWrapper:
    def __init__(self, *socket_args, timeout=0.3):
        self.socket_args = socket_args
        self.socket = None
        self.timeout = timeout

    def __enter__(self):
        self.socket = socket.socket(*self.socket_args)
        self.socket.settimeout(self.timeout)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(1)
        self.socket.close()

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, msg):
        msg_len = len(msg)
        total_sent = 0
        while total_sent < msg_len:
            sent = self.socket.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError('Socket connection broken.')
            total_sent += sent

    def receive(self):
        rlist, _, _ = select.select([self.socket], [], [])

        for s in rlist:
            chunks = []

            while True:
                chunk = s.recv(BUFSIZE)

                if chunk == b'':
                    break

                chunks.append(chunk)

            return b''.join(chunks)

        return b''


