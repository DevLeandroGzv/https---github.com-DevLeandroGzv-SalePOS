from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from PIL import Image,ImageTk
import threading
import sys
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.articulos_combobox()
        self.cargar_articulos()
        self.timer_articulos = None
        
        
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder) 
        
    def widgets(self):
        
        #====================================================================================
        canvas_articulo = tk.LabelFrame(self,text="Articulos",font="arial 14 bold",bg="#C6D9E3")
        canvas_articulo.place(x=300,y=10,width=780,height=580)
        
        self.canvas = tk.Canvas(canvas_articulo,bg="#C6D9E3")
        self.scrollbar = tk.Scrollbar(self.canvas,orient="vertical",command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas,bg="#C6D9E3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e:self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
                )
        )
        
        self.canvas.create_window((0,0),window=self.scrollable_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)
    #====================================================================================
        lblframe_buscar = LabelFrame(self,text="Buscar",font="arial 14 bold",bg="#C6D9E3")
        lblframe_buscar.place(x=10,y=10,width=280,height=80)
        
        self.comboboxbuscar = ttk.Combobox(lblframe_buscar,font="arial 14")
        self.comboboxbuscar.place(x=5,y=5,width=260,height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>",self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>",self.filtrar_articulos)
    #====================================================================================
        lblframe_seleccion = LabelFrame(self,text="Selección",font="arial 14 bold",bg="#C6D9E3")
        lblframe_seleccion.place(x=10,y=95,width=280,height=190)
        
        self.label1 = tk.Label(lblframe_seleccion,text="Articulo :", font="arial 12",bg="#C6D9E3",wraplength=300)
        self.label1.place(x=5,y=5)
        
        self.label2 = tk.Label(lblframe_seleccion,text="Precio :", font="arial 12",bg="#C6D9E3")
        self.label2.place(x=5,y=40)
        
        self.label3 = tk.Label(lblframe_seleccion,text="Costo :", font="arial 12",bg="#C6D9E3")
        self.label3.place(x=5,y=70)
        
        self.label4 = tk.Label(lblframe_seleccion,text="Stock :", font="arial 12",bg="#C6D9E3")
        self.label4.place(x=5,y=100)
        
        self.label5 = tk.Label(lblframe_seleccion,text="Estado :", font="arial 12",bg="#C6D9E3")
        self.label5.place(x=5,y=130)
    #====================================================================================
        lblframe_botones = tk.LabelFrame(self,bg="#C6D9E3",text="Opciones",font="arial 14 bold")
        lblframe_botones.place(x=10,y=290, width=280,height=300)
        
        btn1 = tk.Button(lblframe_botones,text="Agregar",font="arial 14 bold",command=self.agregar_articulo)
        btn1.place(x=20,y=20,width=200,height=40)
        
        btn2 = tk.Button(lblframe_botones,text="Editar",font="arial 14 bold",command=self.editar_articulo)
        btn2.place(x=20,y=80,width=200,height=40)
        
    def load_image(self):
            file_path =filedialog.askopenfilename()
            if file_path:
                image = Image.open(file_path)
                image = image.resize((200,200), Image.LANCZOS)
                image_name = os.path.basename(file_path)
                image_save_path = os.path.join(self.image_folder, image_name)
                image.save(image_save_path)
                
                self.image_tk = ImageTk.PhotoImage(image)
                self.product_image  = self.image_tk
                self.image_path = image_save_path
                
                img_label = tk.Label(self.frameimg, image = self.image_tk)
                img_label.place(x=0,y=0,width=200,height=200)
    
    def articulos_combobox(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos
        
    def agregar_articulo(self):
        top = tk.Toplevel(self)
        top.title("Agregar articulo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False,False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        tk.Label(top,text="Articulo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20,y=20,width=80,height=25)
        entry_articulo  = ttk.Entry(top,font="arial 12 bold")
        entry_articulo.place(x=120,y=20,width=250,height=30)
        
        tk.Label(top,text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20,y=60,width=80,height=25)
        entry_precio  = ttk.Entry(top,font="arial 12 bold")
        entry_precio.place(x=120,y=60,width=250,height=30)
        
        tk.Label(top,text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20,y=100,width=80,height=25)
        entry_costo  = ttk.Entry(top,font="arial 12 bold")
        entry_costo.place(x=120,y=100,width=250,height=30)
        
        tk.Label(top,text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20,y=140,width=80,height=25)
        entry_stock  = ttk.Entry(top,font="arial 12 bold")
        entry_stock.place(x=120,y=140,width=250,height=30)
        
        tk.Label(top,text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20,y=180,width=80,height=25)
        entry_estado  = ttk.Entry(top,font="arial 12 bold")
        entry_estado.place(x=120,y=180,width=250,height=30)
        
        self.frameimg = tk.Frame(top,bg="white",highlightbackground="gray",highlightthickness=1)
        self.frameimg.place(x=440,y=30,width=200,height=200)
        
        btn_image = tk.Button(top, text="Cargar imagen",font="arial 12 bold",command=self.load_image)
        btn_image.place(x=470,y=260,width=150,height=40)
        
        def guardar():
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()
            
            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error","Todos los campos deben ser completados")
                return
            try:
                precio = float(precio)
                costo= float(costo)
                stock =int(stock)
            except ValueError:
                messagebox.showerror("Error","precio, costo y stock deben estar en mayuscula")
                return
            
            if hasattr(self,'image_path'):
                image_path =self.image_path
            else:
                image_path = (r"fotos/default.jpg")
                
            try:
                self.cur.execute("INSERT INTO articulos (articulo,precio,costo,stock,estado,imagen_path) VALUES (?,?,?,?,?,?)",
                                 ( articulo,precio,costo,stock,estado,image_path))
                self.con.commit()
                messagebox.showinfo("Exito","Articulo agregado correctamenta")
                top.destroy()
                self.cargar_articulos()
                self.articulos_combobox()
            except sqlite3.Error as e:
                print(f"Error al cargar el articulo:",e)
                messagebox.showerror("Error","Error al agregar el articulo")
        tk.Button(top,text="Guardar",font="arial 12 bold",command=guardar).place(x=50,y=260,width=150,height=40)
        tk.Button(top,text="Cancelar",font="arial 12 bold",command=top.destroy).place(x=260,y=260,width=150,height=40)
        
    def cargar_articulos(self,filtro= None,categoria=None):
        self.after(0,self._cargar_articulos,filtro,categoria)
    
    def _cargar_articulos(self,filtro = None,categoria = None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        query = "SELECT articulo,precio,imagen_path FROM articulos"
        params= []
        if filtro:
            query +=" WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')
        
        self.cur.execute(query,params)
        articulos = self.cur.fetchall()
        self.row = 0
        self.column = 0
        
        for articulo,precio,image_path in articulos:
            self.mostrar_articulo(articulo,precio,image_path)
        
    def mostrar_articulo(self,articulo,precio,image_path):
        article_frame= tk.Frame(self.scrollable_frame,bg="white",relief="solid")
        article_frame.grid(row=self.row,column=self.column,padx=10,pady=10)
        
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((150,150),Image.Resampling.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(article_frame,image=imagen)
            image_label.image = imagen
            image_label.pack(expand=True,fill="both")
            
            
        name_label = tk.Label(article_frame,text=articulo,bg="white",anchor="w",wraplength=150,font="arial 10 bold")
        name_label.pack(side="top",fill="x")
        
        precio_label = tk.Label(article_frame,text=f"Precio: ${precio:.2f}",bg="white",anchor="w",wraplength=150,font="arial 8 bold")
        precio_label.pack(side="bottom",fill="x")
        
        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1
            
    def on_combobox_select(self,event):
        self.actualizar_label()
    
    def actualizar_label(self,event = None):
        articulo_seleccionado = self.comboboxbuscar.get()
        
        try:
            self.cur.execute("SELECT articulo,precio,costo,stock,estado FROM articulos WHERE articulo=?",(articulo_seleccionado,))
            resultado = self.cur.fetchone()
            
            if resultado is not None:
                articulo,precio,costo,stock,estado = resultado
                
                self.label1.config(text=f"Articulo : {articulo}")
                self.label2.config(text=f"Precio : {precio}")
                self.label3.config(text=f"Costo : {costo}")
                self.label4.config(text=f"Stock : {stock}")
                
                self.label5.config(text=f"Estado : {estado}")
                if estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.label1.config(text="Articulo : No encontrado")
                self.label2.config(text="Precio : No encontrado")
                self.label3.config(text="Costo : No encontrado")
                self.label4.config(text="Stock : No encontrado")
                self.label5.config(text="Estado : No encontrado")
        
        except sqlite3.Error as e :
            print(f"Error al obtener los datos del articulo:",e)
            messagebox.showerror("Error","Error al obtener los datos del articulo")   
    def filtrar_articulos(self,event):
            if self.timer_articulos:
                self.timer_articulos.cancel()
            self.timer_articulos = threading.Timer(1,self._filter_articulos) 
            self.timer_articulos.start()
            
    def _filter_articulos(self):
        typed = self.comboboxbuscar.get()
        
        if typed == '':
            data = self.articulos
        else:
            data = [item for item in self.articulos if typed.lower() in item.lower()]
            
        if data :
            self.comboboxbuscar['values'] = data
            self.comboboxbuscar.event_generate('<Down>')
        else:
            self.comboboxbuscar['values'] = ['No results on']
            self.comboboxbuscar.event_generate('<Down>')
        
        self.cargar_articulos(filtro=typed)
    
    def editar_articulo(self):
        selected_item = self.comboboxbuscar.get()
        if not selected_item:
            messagebox.showerror("Error","Selecciona un articulo para editar")
            return
        
        self.cur.execute("SELECT articulo,precio,costo,stock,estado, imagen_path FROM articulos WHERE articulo = ?",(selected_item,))    
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error","Articulo no encontrado")
            return
        top = tk.Toplevel(self)
        top.title("Editar articulo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False,False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        (articulo,precio,costo,stock,estado,image_path) = resultado
        tk.Label(top,text="Articulo: ",font="arial 12 bold",bg="#C6D9E3").place(x=20,y=20,width=80,height=25)
        entry_articulo = ttk.Entry(top,font="arial 12 bold")
        entry_articulo.place(x=120,y=20,width=250,height=30)
        entry_articulo.insert(0,articulo)
        
        
        tk.Label(top,text="Precio: ",font="arial 12 bold",bg="#C6D9E3").place(x=20,y=60,width=80,height=25)
        entry_precio = ttk.Entry(top,font="arial 12 bold")
        entry_precio.place(x=120,y=60,width=250,height=30)
        entry_precio.insert(0,precio) 
        
        tk.Label(top,text="Costo: ",font="arial 12 bold",bg="#C6D9E3").place(x=20,y=100,width=80,height=25)
        entry_costo = ttk.Entry(top,font="arial 12 bold")
        entry_costo.place(x=120,y=100,width=250,height=30)
        entry_costo.insert(0,costo) 
    
        tk.Label(top,text="Stock: ",font="arial 12 bold",bg="#C6D9E3").place(x=20,y=140,width=80,height=25)
        entry_stock = ttk.Entry(top,font="arial 12 bold")
        entry_stock.place(x=120,y=140,width=250,height=30)
        entry_stock.insert(0,stock)
        
        tk.Label(top,text="Estado: ",font="arial 12 bold",bg="#C6D9E3").place(x=20,y=180,width=80,height=25)
        entry_estado = ttk.Entry(top,font="arial 12 bold")
        entry_estado.place(x=120,y=180,width=250,height=30)
        entry_estado.insert(0,estado)  
        
        self.frameimg = tk.Frame(top,bg="white",highlightbackground="gray",highlightthickness=1)
        self.frameimg.place(x=440,y=30,width=200,height=200)
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200,200),Image.Resampling.LANCZOS)
            self.product_image = ImageTk.PhotoImage(image)
            self.image_path = image_path
            image_label = tk.Label(self.frameimg,image=self.product_image)
            image_label.pack(expand=True, fill="both")
        
        btnImagen = tk.Button(top,text="Cargar imagen",font="arial 12 bold",command=self.load_image)
        btnImagen.place(x=470,y=260,width=150,height=40)
        
        def guardar():
            nuevo_articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()
            
            if not nuevo_articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error","Todos los campos debe ser completados")
                return
            try:
                precio = float(precio)
                costo =float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error","precio,costo y stock deben ser numeros validos")
                
            if hasattr(self,'image_path'):
                image_path =self.image_path
            else:
                image_path = (r"fotos/default.jpg")
                
            self.cur.execute("UPDATE articulos SET articulo=?, precio=?,costo=?,stock=?,estado=?, imagen_path=? WHERE articulo=?",
                             (nuevo_articulo,precio,costo,stock,estado,image_path,selected_item))
            self.con.commit()
            
            self.articulos_combobox()
            self.after(0,lambda:self.cargar_articulos(filtro=nuevo_articulo))
            
            top.destroy()
            messagebox.showinfo("Exito","Articulo editado exitosamente")
        btn_guardar = tk.Button(top,text="Guardar",font="arial 12 bold",command=guardar)
        btn_guardar.place(x=260,y=260,width=150,height=40)
                