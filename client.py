global fonts, connection, root, connect
import tkinter as tk
import socket, time

servers = [['DAVID-JUCKES', 5000, 'For testing']]
server = None

def connect(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def cmd_handle(listbox, choice):
    server = servers[choice]
    connection.recv(1024).decode()

for x in range(len(servers)):
    s = servers[x]
    try:
        connection = connect(s[0], s[1])
        connection.send(b'000')
        time.sleep(0.5)
        servers[x][2] += ' - ' + connection.recv(1024).decode()
        connection.close()
    except ConnectionRefusedError:
        servers[x][2] += ' (offline)'

class fonts:
    normal = ('', 12)

def pick_server(serverlist, selectorframe):
    try:
        choice = serverlist.curselection()[0]
        if serverlist.get(choice).endswith(' (offline)'):
            raise IndexError
    except IndexError:
        pass
    else:
        print(choice)
        server = servers[choice]
        print(server)
        connection = connect(server[0], server[1])
        connection.send(b'001')
        selectorframe.destroy()
        frame = tk.Frame(root)
        scrollbar = tk.Scrollbar(frame)
        board_list = tk.Listbox(frame, height=30, width=30, yscrollcommand=scrollbar.set)
        board_list.pack(fill=tk.BOTH, side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=board_list.yview)
        frame.pack(fill=tk.BOTH)
        li = connection.recv(1024).decode()
        if li.startswith('101'):
            pli = eval(li[3:])
            for item in pli:
                board_list.insert(tk.END, item)
        else:
            raise Exception('Got message from server - ' + li)

root = tk.Tk()
root.title('Better Messaging')

selectorframe = tk.Frame(root)
serverlist = tk.Listbox(selectorframe, height=len(servers) + 5, width=70, font=fonts.normal)
chooseserver = tk.Button(selectorframe, text='Connect', font=fonts.normal, command=lambda: pick_server(serverlist, selectorframe))

for item in servers:
    serverlist.insert(tk.END, item[0] + ' - ' + item[2])

selectorframe.pack(fill=tk.BOTH)
serverlist.pack(fill=tk.BOTH)
chooseserver.pack(fill=tk.X)

root.mainloop()
