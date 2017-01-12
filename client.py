global fonts, connection, root, connect, cmd_handle, board_look, send_msg, entry, connection
import tkinter as tk
import socket, time, threading

servers = [['DAVID-JUCKES', 5000, 'For testing']]
server = None

def connect(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def cmd_handle(connection, msg_out):
    while True:
        cmd = connection.recv(1024).decode()
        print(cmd)
        if len(cmd) > 3:
            arg = cmd[3:]
        else:
            arg = None
        cmd = cmd[:3]
        if cmd == '100':
            msg_out.delete(0, tk.END)
        elif cmd == '103':
            msg_out.insert(0, arg)
            print(arg)

def board_look(board_list, connection):
    prev = ()
    while True:
        while board_list.curselection() == prev:
            time.sleep(0.1)
        try:
            prev = board_list.curselection()
            selection = board_list.get(prev[0])
            connection.send(bytes('002' + selection, 'UTF-8'))
            connection.send(b'004')
            print('004')
        except IndexError:
            pass

def send_msg():
    connection.send(bytes('005' + entry.get(), 'UTF-8'))
    print(entry.get())

for x in range(len(servers)):
    s = servers[x]
    try:
        connection = connect(s[0], s[1])
        connection.send(b'000')
        servers[x][2] += ' - ' + connection.recv(1024).decode()
        connection.close()
    except ConnectionRefusedError:
        servers[x][2] += ' (offline)'

class fonts:
    normal = ('', 12)

def pick_server(serverlist, selectorframe):
    global connection, entry
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
        #send frame
        frame3 = tk.Frame(root)
        entry = tk.Entry(frame3, width=135)
        send = tk.Button(frame3, text='Send', relief=tk.FLAT, command=send_msg)
        send.pack(side=tk.RIGHT, fill=tk.X)
        entry.pack(side=tk.LEFT, fill=tk.X)
        frame3.pack(fill=tk.X, side=tk.BOTTOM)
        #rooms
        frame = tk.Frame(root)
        scrollbar = tk.Scrollbar(frame)
        board_list = tk.Listbox(frame, height=30, width=30, yscrollcommand=scrollbar.set)
        board_list.pack(fill=tk.BOTH, side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=board_list.yview)
        frame.pack(fill=tk.BOTH, side=tk.RIGHT)
        #messages
        frame2 = tk.Frame(root)
        scrollbar2 = tk.Scrollbar(frame2)
        msg_out = tk.Listbox(frame2, height=30, width=120, yscrollcommand=scrollbar2.set)
        msg_out.pack(fill=tk.BOTH, side=tk.LEFT)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar2.config(command=msg_out.yview)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT)
        #get list
        li = connection.recv(1024).decode()
        if li.startswith('101'):
            pli = eval(li[3:])
            for item in pli:
                board_list.insert(tk.END, item)
            handler_thread = threading.Thread(target=cmd_handle, args=[connection, msg_out], name='Handler')
            handler_thread.start()
            board_thread = threading.Thread(target=board_look, args=[board_list, connection], name='Board')
            board_thread.start()
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
