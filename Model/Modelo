from cryptography.fernet import Fernet
import sqlite3


class Modelo:
    """Esta clase se encarga de manejar directamente los datos hacia la BD"""
    querys = []
    rutadb = 'save/database.db'
    con = None
    cur = None

    def __init__(self):
        self.get_querys()

    def get_querys(self):
        """Obtiene los querys para el manejo de la información en la BD"""
        conec = open('res/querys.sql', 'r')
        qs = conec.readlines()
        for q in qs:
            self.querys.append(q.strip('\n'))
        conec.close()

    def conectar(self):
        """Establece la conexión con la BD"""
        try:
            self.con = sqlite3.connect(self.rutadb)
            self.cur = self.con.cursor()
            self.cur.execute(self.querys[0])
            self.con.commit()
        except:
            self.cur.execute(self.querys[1])
            self.con.commit()

    def desconectar(self):
        """Elimina la conexión con la BD"""
        self.con.close()

    def ope_noret(self, opc, reg):
        """Ejecuta las acciones de Agregar, Eliminar y actualizar registros"""
        self.conectar()
        if opc == 0:
            # Agregar registro
            self.cur.execute(self.querys[2], reg)
        elif opc == 1:
            # Eliminar registro
            self.cur.execute(self.querys[8] + reg)
        elif opc == 2:
            # Actualizar registro
            self.cur.execute(self.querys[7], reg)
        self.con.commit()
        self.desconectar()

    def get_database(self):
        """Seleccionar todos los registros de la base de datos"""
        self.conectar()
        self.cur.execute(self.querys[3])
        datos = self.cur.fetchall()
        self.desconectar()
        return datos

    def get_row(self, id):
        """Selecciona un registro de la BD según el ID"""
        self.conectar()
        self.cur.execute(self.querys[4] + id)
        datos = self.cur.fetchone()
        self.desconectar()
        return datos

    def get_account(self, id):
        """Selecciona la cuenta correspondiente al id seleccionado en la BD"""
        self.conectar()
        self.cur.execute(self.querys[5] + id)
        cuenta = self.cur.fetchone()[0]
        self.desconectar()
        return cuenta

    def get_password(self, id):
        """Selecciona la contraseña correspondiente al id seleccionado en la BD"""
        self.conectar()
        self.cur.execute(self.querys[6] + id)
        password = self.cur.fetchone()[0]
        self.desconectar()
        return password

    @staticmethod
    def genera_clave():
        """Se genera la clave con la cual se encriptará la información"""
        clave = Fernet.generate_key()
        master = open("save/master.key", "wb")
        master.write(clave)
        master.close()

    @staticmethod
    def cargar_clave():
        """Se carga la clave con la cual se encriptará la información"""
        cmaster = open("save/master.key", "rb")
        master = cmaster.read()
        cmaster.close()
        return master

    @staticmethod
    def cargar_master():
        """Se obtiene la clave maestra para el ingreso al sistema"""
        cmaster = open("save/master.log", 'rb')
        master = cmaster.read()
        cmaster.close()
        return master
