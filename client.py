global fonts
import tkinter as tk
import socket

servers = [('david-juckes', 5000, 'For testing')]
server = None

class fonts:
    normal = ('', 12)

def pick_server(serverlist):
    try:
        choice = serverlist.curselection()[0]
    except IndexError:
        print('IE')
    finally:
        print(choice)

root = tk.Tk()

selectorframe = tk.Frame(root)
serverlist = tk.Listbox(selectorframe, height=len(servers) + 5, width=70, font=fonts.normal)
chooseserver = tk.Button(selectorframe, text='Connect', font=fonts.normal, command=lambda: pick_server(serverlist))

for item in servers:
    serverlist.insert(tk.END, item[0] + ' - ' + item[2])

selectorframe.pack(fill=tk.BOTH)
serverlist.pack(fill=tk.BOTH)
chooseserver.pack(fill=tk.X)

root.mainloop()
