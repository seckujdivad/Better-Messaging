global fonts, connection, root
import tkinter as tk
import socket, time

servers = [['DAVID-JUCKES', 5000, 'For testing']]
server = None

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for x in range(len(servers)):
    s = servers[x]
    try:
        connection.connect((s[0], s[1]))
        connection.send(b'clist_text')
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
        selectorframe.destroy()
        frame = tk.Frame(root)
        scrollbar = tk.Scrollbar(frame)
        msg_output = tk.Listbox(frame, height=30, width=150, yscrollcommand=scrollbar.set)
        msg_output.pack(fill=tk.BOTH, side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(fill=tk.BOTH)
        for t in range(100):
            msg_output.insert(tk.END, t)

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
