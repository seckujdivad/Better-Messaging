global sdata
import os, socket, threading, time
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

#get_ip_ids()

server.listen(5)
print('Server online')
def multi(server):
    global sdata
    def session(client, address):
        global sdata
        print('Connected to', address[0])
        board = None
        while True:
            data = client.recv(1024).decode()
            if data == None or data == '':
                time.sleep(0.05)
                continue
            print(data)
            cmd = data[:3]
            try:
                arg = data[3:]
            except IndexError:
                arg = None
            #get_ip_ids()
            if cmd == '000':
                if 'clist' in sdata.cfg:
                    client.send(sdata.cfg['clist'].encode())
                else:
                    client.send(b"online")
            elif cmd == '001': #Show all boards
                li = os.listdir('server/chats/')
                client.send(bytes('101' + str(li), 'UTF-8'))
            elif cmd == '002' and not arg == None: #Set board
                if os.path.isdir('server/chats/' + arg):
                    board = arg
                    print('board is', board)
                else:
                    client.send(b'201')
            elif cmd == '003' and not arg == None: #Make new board
                if os.path.isdir('server/chats/' + arg):
                    client.send(b'200')
                else:
                    os.mkdir('server/chats/' + arg)
                    file = open('server/chats/' + arg + '/history.txt', 'w')
                    if address[0] in ipids:
                        file.write('Board made by ' + ipids[address[0]])
                    else:
                        file.write('Board made by ' + address[0])
                    file.close()
                    file = open('server/chats/' + arg + '/people.txt', 'w')
                    file.write('["' + address[0] + '"]')
                    file.close()
            elif cmd == '004' and not board == None and os.path.isdir('server/chats/' + arg):
                file = open('server/chats/' + board + '/history.txt', 'r')
                fc = file.read()
                file.close()
                client.send(b'100')
                for line in fc.split('\n'):
                    client.send(bytes('103' + line, 'UTF-8'))
                    print(line)
                print(board, 'sent')
            elif cmd == '005' and not board == None and not arg == None:
                file = open('server/chats/' + board + '/history.txt', 'a')
                file.write('\n' + arg)
                file.close()
                print(arg, 'added to', board)
    while True:
        client, address = server.accept()
        sdata.clients.append(address)
        thread = threading.Thread(target=session, args=[client, address], name=address)
        thread.start()
thread = threading.Thread(target=multi, args=[server], name='Server handler')
thread.start()
