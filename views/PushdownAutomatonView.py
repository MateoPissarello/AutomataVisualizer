import tkinter as tk
import graphviz
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
from controllers.PushdownAutomaton import PushdownAutomaton  # Importa tu módulo de PDA

class PushdownAutomatonView:
    def __init__(self, root):
        """
        Inicializa la vista del Autómata de Pila.
        """
        self.root = tk.Toplevel(root)
        self.root.title("Autómata de Pila")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.pda = PushdownAutomaton()  # Instancia del autómata de pila

        self.create_controls()
        self.create_text_area()
        self.create_canvas()

    def create_controls(self):
        """Crea el marco con los botones para interactuar con el autómata."""
        marco_controles = tk.Frame(self.root)
        marco_controles.pack(pady=10)

        buttons = [
            ("Agregar Estado", self.add_state_dialog),
            ("Agregar Transición", self.add_transition_dialog),
            ("Visualizar", self.visualize_automaton),
            ("Probar Cadena", self.test_string_dialog),
        ]

        for text, command in buttons:
            tk.Button(marco_controles, text=text, command=command, width=20).pack(side=tk.LEFT, padx=5)

    def create_text_area(self):
        """Crea el área de texto para mostrar el estado actual del autómata."""
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=10, width=80)
        self.text_area.pack(pady=10)
        self.update_text_area()

    def create_canvas(self):
        """Crea el lienzo donde se visualiza el autómata en tiempo real."""
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=300, bg="white")
        self.canvas.pack()

    def update_text_area(self):
        """
        Actualiza el área de texto para mostrar el estado actual del autómata.
        """
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Estados: {str(self.pda.states)}\n")
        self.text_area.insert(tk.END, f"Estado Inicial: {str(self.pda.start_state)}\n")
        self.text_area.insert(tk.END, f"Estados Finales: {str(self.pda.final_states)}\n")
        self.text_area.insert(tk.END, "Transiciones:\n")
        
        for estado, transiciones in self.pda.transitions.items():
            for t in transiciones:
                transicion = f"  {estado} --({t['input'] or 'ε'}, {t['stack_top']})--> {t['next_state']} [{','.join(t['stack_push']) or 'ε'}]\n"
                self.text_area.insert(tk.END, transicion)

    def update_canvas(self):
        """
        Actualiza la visualización del autómata en el canvas después de cada cambio.
        """
        self.canvas.delete("all")  # Limpiar el canvas antes de redibujar
        dot = graphviz.Digraph(comment='Autómata de Pila')

        for estado in self.pda.states:
            if estado in self.pda.final_states:
                dot.node(estado, estado, shape='doublecircle')
            elif estado == self.pda.start_state:
                dot.node(estado, estado, shape='box')
            else:
                dot.node(estado, estado)

        for estado, transiciones in self.pda.transitions.items():
            for t in transiciones:
                etiqueta = f"{t['input'] or 'ε'}:{t['stack_top']}->{','.join(t['stack_push']) or 'ε'}"
                dot.edge(estado, t['next_state'], label=etiqueta)

        nombre_archivo = "temp_automaton.png"
        dot.render(nombre_archivo, view=False, format='png')

        # Cargar y mostrar la imagen del autómata en el canvas
        img = PhotoImage(file=nombre_archivo)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img  # Referencia a la imagen para evitar que se elimine

    def add_state_dialog(self):
        """Muestra un diálogo para agregar un estado."""
        dialogo = self.create_dialog("Agregar Estado")
        
        tk.Label(dialogo, text="Nombre del Estado:").pack()
        entrada_estado = tk.Entry(dialogo)
        entrada_estado.pack()

        es_inicial = tk.BooleanVar()
        es_final = tk.BooleanVar()

        tk.Checkbutton(dialogo, text="Estado Inicial", variable=es_inicial).pack()
        tk.Checkbutton(dialogo, text="Estado Final", variable=es_final).pack()

        def guardar_estado():
            estado = entrada_estado.get().strip()
            if estado:
                self.pda.add_state(estado, es_inicial.get(), es_final.get())
                self.update_text_area()
                self.update_canvas()  # Actualizar visualización
                dialogo.destroy()
            else:
                messagebox.showwarning("Error", "El nombre del estado no puede estar vacío.")

        tk.Button(dialogo, text="Guardar", command=guardar_estado).pack(pady=5)

    def add_transition_dialog(self):
        """Muestra un diálogo para agregar una transición."""
        dialogo = self.create_dialog("Agregar Transición")
        
        tk.Label(dialogo, text="Estado Actual:").pack()
        entrada_estado_actual = tk.Entry(dialogo)
        entrada_estado_actual.pack()

        tk.Label(dialogo, text="Símbolo de Entrada (opcional):").pack()
        entrada_simbolo = tk.Entry(dialogo)
        entrada_simbolo.pack()

        tk.Label(dialogo, text="Símbolo en la Cima de la Pila:").pack()
        entrada_tope_pila = tk.Entry(dialogo)
        entrada_tope_pila.pack()

        tk.Label(dialogo, text="Estado Siguiente:").pack()
        entrada_estado_siguiente = tk.Entry(dialogo)
        entrada_estado_siguiente.pack()

        tk.Label(dialogo, text="Símbolos a Apilar (separados por coma):").pack()
        entrada_simbolos_apilar = tk.Entry(dialogo)
        entrada_simbolos_apilar.pack()

        def guardar_transicion():
            estado_actual = entrada_estado_actual.get().strip()
            if estado_actual:
                self.pda.add_transition(
                    estado_actual, 
                    entrada_simbolo.get() or None, 
                    entrada_tope_pila.get(), 
                    entrada_estado_siguiente.get(), 
                    entrada_simbolos_apilar.get().split(',') if entrada_simbolos_apilar.get() else []
                )
                self.update_text_area()
                self.update_canvas()  # Actualizar visualización
                dialogo.destroy()
            else:
                messagebox.showwarning("Error", "El estado actual no puede estar vacío.")

        tk.Button(dialogo, text="Guardar", command=guardar_transicion).pack(pady=5)

    def test_string_dialog(self):
        """Muestra un diálogo para probar una cadena de entrada."""
        dialogo = self.create_dialog("Probar Cadena")
        
        tk.Label(dialogo, text="Cadena de Entrada:").pack()
        entrada_cadena = tk.Entry(dialogo)
        entrada_cadena.pack()

        def probar_cadena():
            cadena = entrada_cadena.get().strip()
            if cadena:
                resultado = self.pda.process_input(cadena)
                messagebox.showinfo("Resultado", f"Cadena {'Aceptada' if resultado else 'Rechazada'}")
                dialogo.destroy()
            else:
                messagebox.showwarning("Error", "La cadena de entrada no puede estar vacía.")

        tk.Button(dialogo, text="Probar", command=probar_cadena).pack(pady=5)

    def create_dialog(self, title):
        """Crea y retorna un diálogo de entrada común."""
        dialogo = tk.Toplevel(self.root)
        dialogo.title(title)
        dialogo.geometry("300x250")
        return dialogo

    def visualize_automaton(self):
        """Visualiza el autómata usando Graphviz."""
        self.update_canvas()  # Actualizar visualización en el canvas
