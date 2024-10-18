import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Tkinter")

# Crear un cuadro de texto
text_input = tk.Entry(root)
text_input.pack(pady=10)

# Función que muestra un mensaje al presionar el botón
def show_message():
    message = text_input.get()  # Obtiene el texto del cuadro de texto
    messagebox.showinfo("Mensaje", f"Has escrito: {message}")  # Muestra el texto en un cuadro de diálogo

# Crear un botón que muestra el mensaje
button = tk.Button(root, text="Mostrar Mensaje", command=show_message)
button.pack(pady=10)

# Ejecutar el bucle principal de la ventana
root.mainloop()