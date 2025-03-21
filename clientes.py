from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image,ImageTk

class Clientes(tk.Frame):
    db_name = ("database.db")
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_datos()
    def widgets(self):
        self.labelframe = tk.LabelFrame(self,text="Clientes",font="sans 20 bold ",bg="#4f95c9")
        self.labelframe.place(x=20,y=20,width=250,height=560)
        
        lblnombre =tk.Label(self.labelframe,text="Nombre ",font="sans 14 bold ",bg="#4f95c9")
        lblnombre.place(x=10,y=20)
        self.nombre = ttk.Entry(self.labelframe,font="sans 12 bold")
        self.nombre.place(x=10,y=50,width=220,height=40)
        
        lblcedula =tk.Label(self.labelframe,text="Cedula ",font="sans 14 bold ",bg="#4f95c9")
        lblcedula.place(x=10,y=100)
        self.cedula = ttk.Entry(self.labelframe,font="sans 12 bold")
        self.cedula.place(x=10,y=130,width=220,height=40)
        
        lblcelular =tk.Label(self.labelframe,text="Celular ",font="sans 14 bold ",bg="#4f95c9")
        lblcelular.place(x=10,y=180)
        self.celular = ttk.Entry(self.labelframe,font="sans 12 bold")
        self.celular.place(x=10,y=210,width=220,height=40)
        
        lbldireccion =tk.Label(self.labelframe,text="Direccion ",font="sans 14 bold ",bg="#4f95c9")
        lbldireccion.place(x=10,y=260)
        self.direccion = ttk.Entry(self.labelframe,font="sans 12 bold")
        self.direccion.place(x=10,y=290,width=220,height=40)
        
        lblemail =tk.Label(self.labelframe,text="Email ",font="sans 14 bold ",bg="#4f95c9")
        lblemail.place(x=10,y=340)
        self.email = ttk.Entry(self.labelframe,font="sans 12 bold")
        self.email.place(x=10,y=370,width=220,height=40)
        
        image_pil = Image.open("img/agg.png")
        imagen_resize = image_pil.resize((30,30))
        image_tk = ImageTk.PhotoImage(imagen_resize)
        
        btnguardar = Button(self.labelframe, fg="Black",text="Ingresar",font="sans 16 bold",command=self.registrar)
        btnguardar.config(image=image_tk,compound=LEFT,padx=20)
        btnguardar.image = image_tk
        btnguardar.place(x=10,y=420,width=220,height=40)
        
        image_pil = Image.open("img/editar.png")
        imagen_resize = image_pil.resize((30,30))
        image_tk = ImageTk.PhotoImage(imagen_resize)
        
        btnmodificar = Button(self.labelframe, fg="Black",text="Modificar",font="sans 16 bold",command=self.modificar)
        btnmodificar.config(image=image_tk,compound=LEFT,padx=20)
        btnmodificar.image = image_tk
        btnmodificar.place(x=10,y=470,width=220,height=40)
        
        treFrame= Frame(self, bg="white")
        treFrame.place(x=280,y=20,width=800,height=560)
        
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT,fill=Y)
        
        scrol_x = ttk.Scrollbar(treFrame,orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM,fill=X)
        
        self.tre = ttk.Treeview(treFrame,xscrollcommand=scrol_x,yscrollcommand=scrol_y,height=40,
                                columns=("ID","Nombre","Cedula","Celular","Direccion","Correo"),show="headings")
        
        self.tre.pack(expand=True,fill=BOTH)
        
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        self.tre.heading("ID",text="ID")
        self.tre.heading("Nombre",text="Nombre")
        self.tre.heading("Cedula",text="Cedula")
        self.tre.heading("Celular",text="Celular")
        self.tre.heading("Direccion",text="Direccion")
        self.tre.heading("Correo",text="Correo")
        
        self.tre.column("ID",width=50,anchor="center")
        self.tre.column("Nombre",width=150,anchor="center")
        self.tre.column("Cedula",width=120,anchor="center")
        self.tre.column("Celular",width=120,anchor="center")
        self.tre.column("Direccion",width=200,anchor="center")
        self.tre.column("Correo",width=200,anchor="center")
       
    def validar_campos(self):
         if not self.nombre.get() or not self.cedula.get() or not self.celular.get() or not self.direccion.get() or not self.email.get():
             messagebox.showerror("Error","Debe ingresar todos los campos")
             return False
         return True
     
    def registrar(self):
        if not self.validar_campos():
            return
        
        nombre = self.nombre.get()
        cedula = self.cedula.get()
        celular = self.celular.get()
        direccion = self.direccion.get()
        correo = self.email.get()
        
        try:    
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("INSERT INTO clientes (Nombre,Cedula,Celular,Direccion,Correo) VALUES (?, ?, ?, ?, ?)",(nombre,cedula,celular,direccion,correo))
            conn.commit()
            messagebox.showinfo("Exito","Registrado exitosamente")
            self.limpiar_treeview()
            self.limpiar_campos()
            self.cargar_datos()
        except sqlite3.Error as e:
            messagebox.showinfo("Error",f"no se puedo registrar{e}")

        
    def cargar_datos(self):
        try:
            conn =sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM clientes")
            rows = c.fetchall()
            
            for row in rows:
                self.tre.insert("","end",values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showinfo("Error",f"no se pudo mostrar los registros{e}")
            
    def limpiar_treeview(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
    
    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.cedula.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.email.delete(0, END)
            
    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error","No ha seleccionado ningun cliente")
        
        item = self.tre.selection()[0]
        id_cliente = self.tre.item(item,'values')[0]
        
        nombre_actual = self.tre.item(item,'values')[1]
        cedula_actual = self.tre.item(item,'values')[2]
        celular_actual = self.tre.item(item,'values')[3]
        direccion_actual = self.tre.item(item,'values')[4]
        correo_actual = self.tre.item(item,'values')[5]
            
        top_modificar = Toplevel(self)
        top_modificar.title("Modificar Cliente")
        top_modificar.geometry("400x400+400+50")
        top_modificar.config(bg="#4f95c9")
        top_modificar.resizable(False,False)
        top_modificar.transient(self.master)
        top_modificar.grab_set()
        top_modificar.focus_set()
        top_modificar.lift()
        
        tk.Label(top_modificar,text="Nombre: ", font="sans 14 bold",bg="#4f95c9").grid(row=0,column=0,padx=10,pady=5)
        nombre_nuevo = ttk.Entry(top_modificar,font="sans 14 bold")
        nombre_nuevo.insert(0,nombre_actual)
        nombre_nuevo.grid(row=0,column=1,padx=10,pady=5)
        
        tk.Label(top_modificar,text="Cedula: ", font="sans 14 bold",bg="#4f95c9").grid(row=1,column=0,padx=10,pady=5)
        cedula_nuevo = ttk.Entry(top_modificar,font="sans 14 bold")
        cedula_nuevo.insert(0,cedula_actual)
        cedula_nuevo.grid(row=1,column=1,padx=10,pady=5)
        
        tk.Label(top_modificar,text="Celular: ", font="sans 14 bold",bg="#4f95c9").grid(row=2,column=0,padx=10,pady=5)
        celular_nuevo = ttk.Entry(top_modificar,font="sans 14 bold")
        celular_nuevo.insert(0,celular_actual)
        celular_nuevo.grid(row=2,column=1,padx=10,pady=5)
        
        tk.Label(top_modificar,text="Direccion: ", font="sans 14 bold",bg="#4f95c9").grid(row=3,column=0,padx=10,pady=5)
        direccion_nuevo = ttk.Entry(top_modificar,font="sans 14 bold")
        direccion_nuevo.insert(0,direccion_actual)
        direccion_nuevo.grid(row=3,column=1,padx=10,pady=5)
        
        tk.Label(top_modificar,text="Correo: ", font="sans 14 bold",bg="#4f95c9").grid(row=4,column=0,padx=10,pady=5)
        correo_nuevo = ttk.Entry(top_modificar,font="sans 14 bold")
        correo_nuevo.insert(0,correo_actual)
        correo_nuevo.grid(row=4,column=1,padx=10,pady=5)
        
        def guardar_modificaciones():
            nuevo_nombre = nombre_nuevo.get()
            nuevo_cedula = cedula_nuevo.get()
            nuevo_celular = celular_nuevo.get()
            nuevo_direccion =direccion_nuevo.get()
            nuevo_correo = correo_nuevo.get()
            
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("""UPDATE clientes SET Nombre= ?, Cedula = ?,Celular = ?,Direccion = ?, Correo =? WHERE id =?""",
                               (nuevo_nombre,nuevo_cedula,nuevo_celular,nuevo_direccion,nuevo_correo,id_cliente))
                conn.commit()
                conn.close()
                messagebox.showinfo("Exito","Se realizo la actualizacion del cliente")
                self.limpiar_treeview()
                self.cargar_datos()
                top_modificar.destroy()
            except sqlite3.Error as e:
                messagebox.showinfo("Error","no se pudo actualizar el cliente")
        btnguardar = Button(top_modificar,text="Guardar cambios",font="sans 14 bold",command=guardar_modificaciones)
        btnguardar.grid(row=5,column=0,columnspan=2,pady=20)
            
            
            
        
                     
       
        
        
