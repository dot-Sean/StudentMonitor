import tkinter
from tkinter import ttk
from multiprocessing import Process
from config import HOST, PORT
import server


class App(object):

    def __init__(self):
        self.s = None
        self.root = tkinter.Tk()
        self.root.title("ServerSM")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        frm = ttk.Frame(self.root)
        frm.pack(expand=True, fill='both')

        tkinter.Label(frm, text="port").grid(row=0, sticky=tkinter.E)
        tkinter.Label(frm, text="IP").grid(row=1, sticky=tkinter.E)

        self.port_text = tkinter.Text(frm, width=5, height=1)
        self.port_text.insert('1.0', PORT)
        self.port_text.grid(row=0, column=1, sticky=tkinter.W)

        self.ip_text = tkinter.Text(frm, width=15, height=1)
        self.ip_text.insert('1.0', HOST)
        self.ip_text.grid(row=1, column=1)

        self.connect_button = ttk.Button(frm, text="Połącz", command=self.run_server)
        self.connect_button.grid(row=3, padx=5)

        self.disconnect_button = ttk.Button(frm, text="Rozłącz", command=self.disconnect_server, state=tkinter.DISABLED)
        self.disconnect_button.grid(row=3, column=1)

        self.webapp_button = ttk.Button(frm, text="Uruchom webapp", command=self.run_webapp)
        self.webapp_button.grid(row=3, column=2)

    def run_webapp(self):
        import web_app.run as r
        self.webapp_button['state'] = tkinter.DISABLED
        p = Process(target=r.run)
        p.start()

    def on_closing(self):
        self.root.destroy()

    def run_server(self):
        self.connect_button['state'] = tkinter.DISABLED
        self.disconnect_button['state'] = tkinter.ACTIVE

        self.s = server.ServerSM(self.ip_text.get(1.0, tkinter.INSERT), self.port_text.getint())
        p = Process(target=self.s.wait_for_clients, args=())
        p.start()

    def disconnect_server(self):
        self.s.stopped = True
        self.connect_button['state'] = tkinter.ACTIVE
        self.disconnect_button['state'] = tkinter.DISABLED
        self.s = None


if __name__ == '__main__':
    app = App()
    app.root.mainloop()