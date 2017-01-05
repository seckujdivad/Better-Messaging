print('Server')
import os, socket, threading
#os.system('color a') #For that computery look - if you want it, uncomment it

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((socket.gethostname(), 5000))

server.listen(5)
print('Server online')
def multi(server):
    def session(client, address):
        print('Connected to', address[0])
        data = client.recv(1024).decode()
        print(data)
        if data == 'clist_text':
            client.send(b"HP Omen X")
    while True:
        print('!')
        client, address = server.accept()
        thread = threading.Thread(target=session, args=[client, address], name=address)
        thread.start()
thread = threading.Thread(target=multi, args=[server], name='Server handler')
thread.start()
