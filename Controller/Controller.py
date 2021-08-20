from tkinter import messagebox
from tkinter import *
from cryptography.fernet import Fernet
import pyperclip as clipboard
import random as rand
import os
from Model.Modelo import Modelo
from View.Vista import Vista
from Controller import ControlExceptions as Ex


class Controlador:
    """La clase controlador permite gestionar el flujo de negocio de la solución a desarrollar. Este desarrollo
    esta basado en el marco de referencia MVC, por lo tanto la clase controlador maneja la interacción entre
    la interfaz de usuario y la lógica detrás de ella"""
    model = Modelo()
    conaccess = None

    def __init__(self, root):
        """Inicia la ejeución de la interfaz de usuario, así como comprueba que exista la clave maestra"""
        self.root = root
        self.view = Vista(root=self.root, control=self)
        try:
            self.conaccess = open('save/master.log', 'rb')
        except:
            self.view.primer_acceso()

    def guardar_master(self):
        """Realiza al usuario la petición de la clave maestra y la almacena encriptada"""
        os.mkdir('save')
        self.model.genera_clave()
        clave = self.encriptar(self.view.econt.get())
        self.conaccess = open('save/master.log', 'wb')
        self.conaccess.write(clave)
        self.conaccess.close()
        self.view.primer_acceso_page.destroy()

    def validar_acceso(self, clave):
        """Realiza la validación de la clave introducida"""
        access = self.desencriptar(self.model.cargar_master())
        if clave == access:
            self.view.main_page()
            self.llenar_tabla()
        else:
            messagebox.showerror(title='Error de acceso', message='Clave de acceso incorrecta. Inténtalo de nuevo.')
            self.view.enclave.delete(0, END)

    def llenar_tabla(self):
        """Llena los elementos del TreeView con las cuentas y la plataforma correspondiente"""
        # Limpiamos tabla
        records = self.view.contenedor.get_children()
        for element in records:
            self.view.contenedor.delete(element)
        # Llenamos tabla
        tabla = self.model.get_database()
        for dato in tabla:
            self.view.contenedor.insert(parent='', index=END, iid=dato[0], text='', values=(dato[0], dato[1], dato[2]))

    def segunda_vent(self, opc):
        """Verifica la opción a realizar, ya sea agregar una nueva cuenta o editar una existente"""
        if opc == 0:
            self.view.add_edit(opc, ("", "", ""))
        elif opc == 1:
            try:
                sel = str(self.view.contenedor.selection()[0])
                if messagebox.askyesno(title='Confirmación', message='¿Cuenta seleccionada a editar?'):
                    datos = self.model.get_row(sel)
                    clave = self.desencriptar(datos[2])
                    self.view.add_edit(opc, (datos[0], datos[1], clave))
            except Ex.NoSelection:
                messagebox.showwarning(title='Sin selección', message='No se ha seleccionado algún registro. '
                                                                      'Inténtalo de nuevo.')

    def agregar(self):
        """Función que nos permite argegar una nueva cuenta"""
        try:
            clave = self.encriptar(self.view.conta.get())
            self.model.ope_noret(0, (self.view.cuenta.get(), self.view.plata.get(), clave))
            self.llenar_tabla()
            self.view.add_edit_page.destroy()
        except Ex.AccountNotAdded:
            messagebox.showwarning(title='Sin selección', message='No se ha agregado la cuenta')

    def editar(self):
        """Función que nos ayuda a editar elementos de una cuenta específica"""
        try:
            sel = str(self.view.contenedor.selection()[0])
            clave = self.encriptar(self.view.conta.get())
            self.model.ope_noret(2, (self.view.cuenta.get(), self.view.plata.get(), clave, sel))
            self.llenar_tabla()
            self.view.add_edit_page.destroy()
        except Ex.NoSelection:
            messagebox.showwarning(title='Sin selección', message='No se ha seleccionado algún registro. '
                                                                  'Inténtalo de nuevo.')

    def eliminar(self):
        """Función que se encarga de eliminar una cuenta"""
        try:
            sel = str(self.view.contenedor.selection()[0])
            conf = messagebox.askyesno(title='Confirmación', message='¿Está seguro de eliminar la cuenta seleccionada?')
            if conf:
                self.model.ope_noret(1, sel)
                self.llenar_tabla()
        except Ex.NoSelection:
            messagebox.showwarning(title='Sin selección', message='No se ha seleccionado algún registro. '
                                                                  'Inténtalo de nuevo.')

    def salvar_conta(self):
        """Se obtiene la contraseña desencriptada correspondiente a la cuenta """
        try:
            sel = str(self.view.contenedor.selection()[0])
            clave = self.desencriptar(self.model.get_password(sel))
            clipboard.copy(clave)
            if messagebox.showinfo(title='Contraseña salvada', message='Presiona aceptar '
                                                                       'una vez utilizada la contraseña'):
                clipboard.copy('Overtime')
        except Ex.NoSelection:
            messagebox.showwarning(title='Sin selección', message='No se ha seleccionado algún registro. '
                                                                  'Inténtalo de nuevo.')

    def salvar_cuenta(self):
        """Se obtiene la contraseña de una cuenta específica"""
        try:
            sel = str(self.view.contenedor.selection()[0])
            cuenta = self.model.get_account(sel)
            clipboard.copy(cuenta)
        except Ex.NoSelection:
            messagebox.showwarning(title='Sin selección', message='No se ha seleccionado algún registro. '
                                                                  'Inténtalo de nuevo.')

    def generar_cont(self):
        """Funcion que genera una contraseña aleatoria para una cuenta"""
        cont = ''
        for i in range(14):
            cont = cont + str(chr(rand.randint(33, 125)))
        self.view.conta.delete(0, END)
        self.view.conta.insert(0, cont)

    def encriptar(self, dato):
        """Se encarga de encriptar las contraseñas con la clave codificada"""
        master = dato.encode()
        fe = Fernet(self.model.cargar_clave())
        encript = fe.encrypt(master)
        return encript

    def desencriptar(self, dato):
        """Se encarga de desencripatar las contraseñas con la palabra clave codificada"""
        fe = Fernet(self.model.cargar_clave())
        master = fe.decrypt(dato)
        master = master.decode('utf-8')
        return master
