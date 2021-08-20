from tkinter import *
from Controller.Controlador import Controlador

if __name__ == '__main__':
    raiz = Tk()
    view = Controlador(raiz)
    raiz.mainloop()
