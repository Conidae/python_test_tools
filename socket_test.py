import os
import socket

class BlockingServerBase:
    def __init__(self, timeout:int=60, buffer:int=1024):
        print('server start')
        self.__socket = None
        self.__timeout = timeout
        self.__buffer = buffer
        self.close()

    def __del__(self):
        self.close()

    def close(self) -> None:
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass

    def accept(self, address, family:int, typ:int, proto:int) -> None:
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.bind(address)
        self.__socket.listen(1)
        print("Server started :", address)
        while True:
            conn, _ = self.__socket.accept()
            print('accepted!')
            while True:
                try:
                    message_recv = conn.recv(self.__buffer).decode('utf-8')
                    if message_recv == '':
                        break
                    if  'quit' in message_recv:
                        return
                    _ = self.onRecieved(message_recv)
                    message_resp = ""
                    conn.send(message_resp.encode('utf-8'))
                    #change member 'self.need_send' True if need to send something, in 'onRecieved()' method.
                except ConnectionResetError:
                    break
                except BrokenPipeError:
                    break
            #self.close()

    def onRecieved(self, message:str) -> str:
        print(message)
        return ""

if __name__ == "__main__":
    server = BlockingServerBase()
    ip = input("Input address")
    port = int(input("Input port number"))
    address = (ip,port)
    server.accept(address,socket.AF_INET,socket.SOCK_STREAM,0)

