import tkinter as tk
from controllers.LanguageTypeController import LanguageTypeController


class LanguageTypeView:
    """Clase para la vista de Tipo de Lenguaje."""

    def __init__(self, root):
        # Crear una nueva ventana secundaria
        self.window = tk.Toplevel(root)
        self.window.title("Tipo de Lenguaje")
        self.window.geometry("400x300")

        # Contenido de la ventana
        self.label = tk.Label(
            self.window, text="Determina el tipo de lenguaje", font=("Arial", 14)
        )
        self.label.pack(pady=20)

        self.entry = tk.Entry(self.window, width=40)
        self.entry.pack(pady=20)

        self.entry_btn = tk.Button(
            self.window, text="Determinar", command=self.handle_btn_click
        )
        self.entry_btn.pack(pady=10)
        # Botón para cerrar
        self.close_button = tk.Button(
            self.window, text="Cerrar", command=self.window.destroy
        )
        self.close_button.pack(pady=10)
        self.controller = LanguageTypeController(self)

    def handle_btn_click(self):
        self.controller.determine_language_type()


# # Ventana principal
# root = tk.Tk()
# root.title("Menú Principal")
# root.geometry("400x300")

# # Botón en el menú principal para abrir la vista de tipo de lenguaje
# btn_language_type = tk.Button(root, text="Tipo de Lenguaje", command=abrir_language_type_view)
# btn_language_type.pack(pady=50)

# root.mainloop()
