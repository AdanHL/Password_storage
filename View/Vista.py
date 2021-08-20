from tkinter import ttk as tk
from tkinter import *


class Vista:
    """Se generan los elementos visuales para que el usuario pueda interactuar con el sistema"""
    add_edit_page = None
    primer_acceso_page = None
    contenedor = None
    cuenta = None
    plata = None
    conta = None
    econt = None

    def __init__(self, root, control):
        """Se genera la pantalla de ingreso al sistema"""
        self.c = control
        self.r = root
        self.r.geometry('350x110')
        self.r.resizable(False, False)
        self.r.iconbitmap('res/LogoPassSecure.ico')
        self.r.title('Password Storage')
        # Se declaran los elementos visuales
        frame = LabelFrame(self.r, text='Ingresa la clave de acceso')
        self.enclave = Entry(frame, show='*')
        self.enclave.focus()
        btnentra = Button(frame, text='Ingresar', padx=10, command=lambda: self.c.validar_acceso(self.enclave.get()))
        # Se imprimen los elementos visuales
        frame.pack(fill='both', expand='true', ipadx=20, padx=5, pady=5, ipady=5)
        self.enclave.pack(pady=13)
        btnentra.pack(side='right', padx=5)

    def primer_acceso(self):
        """Se genera la pantalla de creación de clave maestra"""
        self.primer_acceso_page = Toplevel()
        self.primer_acceso_page.iconbitmap('res/LogoPassSecure.ico')
        # Se declaran los elementos viusales
        frame = LabelFrame(self.primer_acceso_page, text='Contraseña maestra de primer acceso')
        self.econt = Entry(frame, width=20)
        self.econt.focus()
        # Se imprimen los elementos visuales
        frame.pack(pady=5, padx=20)
        self.econt.pack(pady=5)
        Button(frame, text='Aceptar', command=lambda: self.c.guardar_master()).pack(pady=5)
        # Se controla el cierre de la aplicación
        self.primer_acceso_page.protocol("WM_DELETE_WINDOW", lambda: self.r.destroy())

    def main_page(self):
        """Se genera la pantalla principal del sistema"""
        # Se esconde la ventana de inicio
        self.r.withdraw()
        # Se declaran los elementos visuales
        mainpage = Toplevel()
        mainpage.iconbitmap('res/LogoPassSecure.ico')
        frame = Frame(mainpage)
        miniframe = Frame(frame)
        self.contenedor = tk.Treeview(frame, columns=("id", "cuenta", "plataforma"))
        btnsalvar = Button(miniframe, text='Contraseña', width=20, command=lambda: self.c.salvar_conta())
        btnsalvar2 = Button(miniframe, text='Cuenta', width=20, command=lambda: self.c.salvar_cuenta())
        btneliminar = Button(frame, text='Eliminar', width=20, command=lambda: self.c.eliminar())
        btneditar = Button(frame, text='Editar', width=20, command=lambda: self.c.segunda_vent(1))
        btnagregar = Button(frame, text='Agregar', width=20, command=lambda: self.c.segunda_vent(0))
        # Se configuran los elementos correspondientes
        self.contenedor.column("#0", width=0)
        self.contenedor.column("id", width=30)
        self.contenedor.column("cuenta", width=280)
        self.contenedor.column("plataforma", width=180)
        self.contenedor.heading("#0", text='')
        self.contenedor.heading("id", text='Id')
        self.contenedor.heading("cuenta", text='Cuenta')
        self.contenedor.heading("plataforma", text='Plataforma')
        # Se imprimen los elementos visuales
        frame.pack(fill='both', expand='true', padx=10, pady=10)
        self.contenedor.grid(column=0, row=0, columnspan=2)
        miniframe.grid(column=0, row=1, pady=2)
        btnsalvar.grid(column=0, row=0)
        btnsalvar2.grid(column=1, row=0)
        btneliminar.grid(column=1, row=1, pady=2)
        btneditar.grid(column=0, row=2, pady=2)
        btnagregar.grid(column=1, row=2, pady=2)
        # Se controla el cierre de la aplicación
        mainpage.protocol("WM_DELETE_WINDOW", lambda: self.r.destroy())

    def add_edit(self, opc, dat):
        """Se genera la pantalla que nos permite editar una cuenta existente o agregar una nueva"""
        self.add_edit_page = Toplevel()
        self.add_edit_page.iconbitmap('res/LogoPassSecure.ico')
        # Se declaran los elementos visuales
        frame = LabelFrame(self.add_edit_page, text='Datos de la cuenta')
        self.cuenta = Entry(frame, width=30)
        self.plata = Entry(frame, width=30)
        self.conta = Entry(frame, width=30)
        # Se imprimen los elementos visuales
        frame.pack(pady=5, padx=5, ipadx=5, ipady=5)
        Label(frame, text='Cuenta').grid(column=0, row=0, sticky='W')
        self.cuenta.insert(0, dat[0])
        self.cuenta.grid(column=1, row=0)
        Label(frame, text='Plataforma').grid(column=0, row=1, sticky='W')
        self.plata.insert(0, dat[1])
        self.plata.grid(column=1, row=1)
        Label(frame, text='Contraseña').grid(column=0, row=2, sticky='W')
        self.conta.insert(0, dat[2])
        self.conta.grid(column=1, row=2)
        Button(frame, text='Aceptar',
               command=lambda x=opc: self.c.agregar() if x == 0 else self.c.editar()).grid(column=2, row=3)
        Button(frame, text='Generar contraseña', command=lambda: self.c.generar_cont()).grid(column=1, row=3)
