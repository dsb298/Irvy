from client import TcpClient
import time

HOST = '127.0.0.1'
PORT = 12345

def main():
    myClient = TcpClient()
    myClient.connect(HOST, PORT)

    # run_code = True
    # while(run_code):
    msg = myClient.recv_data()
    print(msg)
    time.sleep(1)

if __name__ == "__main__":
    main()