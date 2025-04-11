import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario por Consolas")
        self.root.geometry("900x550")

        self.datos_por_categoria = {
            "Switch": [],
            "PlayStation": [],
            "Xbox": []
        }

        self.categoria_actual = tk.StringVar(value="Switch")

        # Menú de categorías
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(frame_top, text="Consola:").pack(side=tk.LEFT, padx=5)
        self.combo_categoria = ttk.Combobox(frame_top, textvariable=self.categoria_actual, values=["Switch", "PlayStation", "Xbox"], state="readonly")
        self.combo_categoria.pack(side=tk.LEFT)
        self.combo_categoria.bind("<<ComboboxSelected>>", lambda e: self.actualizar_tabla())

        # Formulario
        frame_form = tk.Frame(self.root)
        frame_form.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_form, text="Producto").grid(row=0, column=0)
        self.entry_producto = tk.Entry(frame_form)
        self.entry_producto.grid(row=0, column=1)

        tk.Label(frame_form, text="Descripción").grid(row=0, column=2)
        self.entry_descripcion = tk.Entry(frame_form)
        self.entry_descripcion.grid(row=0, column=3)

        tk.Label(frame_form, text="Cantidad").grid(row=1, column=0)
        self.entry_cantidad = tk.Entry(frame_form)
        self.entry_cantidad.grid(row=1, column=1)

        tk.Label(frame_form, text="Precio").grid(row=1, column=2)
        self.entry_precio = tk.Entry(frame_form)
        self.entry_precio.grid(row=1, column=3)

        # Botones
        tk.Button(frame_form, text="Agregar", command=self.agregar_producto, bg="green", fg="white").grid(row=2, column=0, pady=5)
        tk.Button(frame_form, text="Modificar", command=self.modificar_producto, bg="orange", fg="white").grid(row=2, column=1, pady=5)
        tk.Button(frame_form, text="Eliminar", command=self.eliminar_producto, bg="red", fg="white").grid(row=2, column=2, pady=5)
        tk.Button(frame_form, text="Guardar PDF", command=self.guardar_pdf, bg="blue", fg="white").grid(row=2, column=3, pady=5)

        # Tabla
        columnas = ("#1", "#2", "#3", "#4", "#5")
        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, titulo in enumerate(["Número", "Producto", "Descripción", "Cantidad", "Precio"], start=1):
            self.tree.heading(f"#{i}", text=titulo)
            self.tree.column(f"#{i}", width=100, anchor="center")

        self.contadores = {
            "Switch": 1,
            "PlayStation": 1,
            "Xbox": 1
        }

    def agregar_producto(self):
        producto = self.entry_producto.get()
        descripcion = self.entry_descripcion.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
        categoria = self.categoria_actual.get()

        if producto and descripcion and cantidad and precio:
            numero = self.contadores[categoria]
            self.datos_por_categoria[categoria].append((numero, producto, descripcion, cantidad, precio))
            self.contadores[categoria] += 1
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        categoria = self.categoria_actual.get()
        for fila in self.datos_por_categoria[categoria]:
            self.tree.insert("", "end", values=fila)

    def eliminar_producto(self):
        selected = self.tree.selection()
        if selected:
            idx = self.tree.index(selected)
            categoria = self.categoria_actual.get()
            del self.datos_por_categoria[categoria][idx]
            self.actualizar_tabla()
            messagebox.showinfo("Eliminado", "Producto eliminado.")
        else:
            messagebox.showwarning("Selecciona", "Selecciona un producto para eliminar.")

    def modificar_producto(self):
        selected = self.tree.selection()
        if selected:
            idx = self.tree.index(selected)
            producto = self.entry_producto.get()
            descripcion = self.entry_descripcion.get()
            cantidad = self.entry_cantidad.get()
            precio = self.entry_precio.get()
            categoria = self.categoria_actual.get()

            if producto and descripcion and cantidad and precio:
                numero = self.datos_por_categoria[categoria][idx][0]
                self.datos_por_categoria[categoria][idx] = (numero, producto, descripcion, cantidad, precio)
                self.actualizar_tabla()
                self.limpiar_campos()
                messagebox.showinfo("Modificado", "Producto actualizado.")
            else:
                messagebox.showwarning("Campos vacíos", "Rellena todos los campos para modificar.")
        else:
            messagebox.showwarning("Selecciona", "Selecciona un producto para modificar.")

    def guardar_pdf(self):
        c = canvas.Canvas("inventario_consolas.pdf", pagesize=letter)
        width, height = letter
        y = height - 40
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "INVENTARIO POR CONSOLA")
        c.setFont("Helvetica", 10)
        y -= 30

        for categoria, datos in self.datos_por_categoria.items():
            if not datos:
                continue
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, f"{categoria}")
            y -= 20
            c.setFont("Helvetica", 9)
            c.drawString(50, y, "N°")
            c.drawString(80, y, "Producto")
            c.drawString(180, y, "Descripción")
            c.drawString(370, y, "Cantidad")
            c.drawString(440, y, "Precio")
            y -= 15

            for fila in datos:
                c.drawString(50, y, str(fila[0]))
                c.drawString(80, y, str(fila[1]))
                c.drawString(180, y, str(fila[2]))
                c.drawString(370, y, str(fila[3]))
                c.drawString(440, y, str(fila[4]))
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50

            y -= 20

        c.save()
        messagebox.showinfo("PDF Guardado", "Se guardó como 'inventario_consolas.pdf'")

    def limpiar_campos(self):
        self.entry_producto.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

# Ejecutar app
root = tk.Tk()
app = InventarioApp(root)
root.mainloop()
