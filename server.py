global sdata
import os, socket, threading
#os.system('color a') #For that computery look - if you want it, uncomment it

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((socket.gethostname(), 5000))

class sdata:
    clients = []

server.listen(5)
print('Server online')
def multi(server):
    global sdata
    def session(client, address):
        global sdata
        print('Connected to', address[0])
        data = client.recv(1024).decode()
        print(data)
        if data == 'clist_text':
            client.send(b"Is it thelegend27?")
    while True:
        print('!')
        client, address = server.accept()
        sdata.clients.append(address)
        thread = threading.Thread(target=session, args=[client, address], name=address)
        thread.start()
thread = threading.Thread(target=multi, args=[server], name='Server handler')
thread.start()
