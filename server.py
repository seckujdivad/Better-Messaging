global sdata
import os, socket, threading
#os.system('color a') #For that computery look - if you want it, uncomment it

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((socket.gethostname(), 5000))

class sdata:
    clients = []
    cfg = {}

file = open('server/config.txt', 'r')
f = file.read()
file.close()
for line in f.split('\n'):
    line = line.split(':')
    sdata.cfg[line[0]] = line[1]

ipids = {}

def get_ip_ids():
    global ipids
    file = open('server/ipids.txt', 'r')
    f = file.read()
    file.close()
    for line in f.split('\n'):
        line = line.split(':')
        ipids[line[0]] = line[1]

get_ip_ids()

server.listen(5)
print('Server online')
def multi(server):
    global sdata
    def session(client, address):
        global sdata
        print('Connected to', address[0])
        while True:
            data = client.recv(1024).decode()
            print(data)
            cmd = data[:3]
            try:
                arg = data[3:]
            except IndexError:
                arg = None
            get_ip_ids()
            if cmd == '000':
                if 'clist' in sdata.cfg:
                    client.send(sdata.cfg['clist'].encode())
                else:
                    client.send(b"online")
            elif cmd == '001' and not arg == None:
                if os.path.isdir('server/chats/' + arg):
                    client.send('200')
                else:
                    os.mkdir('server/chats/' + arg)
                    file = open('server/chats/' + arg + '/history.txt', 'w')
                    if address[0] in ipids:
                        file.write('Room made by ' + ipids[address[0]])
                    else:
                        file.write('Room made by ' + address[0])
                    file.close()
                    file = open('server/chats/' + arg + '/people.txt', 'w')
                    file.write('["' + address[0] + '"]')
                    file.close()
    while True:
        client, address = server.accept()
        sdata.clients.append(address)
        thread = threading.Thread(target=session, args=[client, address], name=address)
        thread.start()
thread = threading.Thread(target=multi, args=[server], name='Server handler')
thread.start()
