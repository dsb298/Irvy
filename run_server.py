from server import TcpServer
import time

HOST = '127.0.0.1'
PORT = 12345

def main():
    myServer = TcpServer()
    myServer.connect(HOST, PORT)

    msg = b"Hello from server!"

    # run_code = True
    # while(run_code):
    myServer.send_data(msg)
    time.sleep(1)

if __name__ == "__main__":
    main()