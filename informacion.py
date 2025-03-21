from tkinter import *
import tkinter as tk

class Informacion(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        labelframe = tk.LabelFrame(self,text="INFORMACION",font="sans 16 bold",background="#4f95c9",)
        labelframe.place(x=150,y=30,width=800,height=420)
        
        label_1 = tk.Label(labelframe,text="                                                                       SALEPOS",font="Segoe 14 bold", bg="#4f95c9")
        label_1.place(x=10,y=11)

        label_2 = tk.Label(labelframe,text="Esta aplicación fue creada con el fin de resolver el problema de realizar ventas seguras",font="Segoe 14", bg="#4f95c9",fg="white")
        label_2.place(x=10,y=40)
        
        label_3 = tk.Label(labelframe,text="contando con reportes de ventas, stock y facturas.",font="Segoe 14", bg="#4f95c9",fg="white")
        label_3.place(x=10,y=70)
        
        label_4 = tk.Label(labelframe,text="Guia de uso: La aplicación cuenta con una seccion de ventas donde podras manipular",font="Segoe 14", bg="#4f95c9",fg="white")
        label_4.place(x=10,y=110)
        
        label_5 = tk.Label(labelframe,text="las ventas de la mejor manera, una seccion de inventario para almacenar tus productos",font="Segoe 14", bg="#4f95c9",fg="white")
        label_5.place(x=10,y=140)
        
        label_6 = tk.Label(labelframe,text="y una seccion de clientes para que puedas saber a quien le vendes tus productos",font="Segoe 14", bg="#4f95c9",fg="white")
        label_6.place(x=10,y=170)
        
        label_7 = tk.Label(labelframe,text="SOPORTE TECNICO :",font="Segoe 14 bold", bg="#4f95c9")
        label_7.place(x=10,y=210)
        
        label_8 = tk.Label(labelframe,text="TELEFONO: 3175487922",font="Segoe 14", bg="#4f95c9",fg="white")
        label_8.place(x=10,y=240)
        
        label_9 = tk.Label(labelframe,text="CORREO: yepeto1321@gmail.com",font="Segoe 14", bg="#4f95c9",fg="white")
        label_9.place(x=10,y=270)
        
        label_10 = tk.Label(labelframe,text="Políticas y Seguridad: Mantén credenciales seguras, usa conexiones protegidas,define permisos por roles y realiza copias de seguridad",font="Segoe 9", bg="#4f95c9",fg="white")
        label_10.place(x=10,y=340)
        
        label_10 = tk.Label(labelframe,text="periódicas para evitar pérdidas de datos.",font="Segoe 9", bg="#4f95c9",fg="white")
        label_10.place(x=10,y=360)
        