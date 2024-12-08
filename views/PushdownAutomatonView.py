import tkinter as tk
import graphviz
from tkinter import messagebox, filedialog
from  controllers.PushdownAutomaton import PushdownAutomaton  # Importa tu módulo de PDA

class PushdownAutomatonView:
    def __init__(self, root):
        """
        Inicializa la vista del Autómata de Pila
        """
        self.root = tk.Toplevel(root)
        self.root.title("Autómata de Pila")
        self.root.geometry("800x600")

        self.pda = PushdownAutomaton()  # Instancia del autómata de pila

        # Marco para controles
        marco_controles = tk.Frame(self.root)
        marco_controles.pack(pady=10)

        # Botones para interactuar con el autómata
        tk.Button(marco_controles, text="Agregar Estado", 
                  command=self.add_state_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(marco_controles, text="Agregar Transición", 
                  command=self.add_transition_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(marco_controles, text="Visualizar", 
                  command=self.visualize_automaton).pack(side=tk.LEFT, padx=5)
        tk.Button(marco_controles, text="Probar Cadena", 
                  command=self.test_string_dialog).pack(side=tk.LEFT, padx=5)

        # Área de texto para mostrar información del autómata
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.text_area.pack(pady=10)
        self.update_text_area()

    def update_text_area(self):
        """
        Actualiza el área de texto para mostrar el estado actual del autómata
        """
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Estados: " + str(self.pda.states) + "\n")
        self.text_area.insert(tk.END, "Estado Inicial: " + str(self.pda.start_state) + "\n")
        self.text_area.insert(tk.END, "Estados Finales: " + str(self.pda.final_states) + "\n")
        self.text_area.insert(tk.END, "Transiciones:\n")
        for estado, transiciones in self.pda.transitions.items():
            for t in transiciones:
                transicion = f"  {estado} --({t['input'] or 'ε'}, {t['stack_top']})--> {t['next_state']} [{','.join(t['stack_push']) or 'ε'}]\n"
                self.text_area.insert(tk.END, transicion)

    def add_state_dialog(self):
        """
        Diálogo para agregar un estado
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Estado")

        tk.Label(dialogo, text="Nombre del Estado:").pack()
        entrada_estado = tk.Entry(dialogo)
        entrada_estado.pack()

        es_inicial = tk.BooleanVar()
        es_final = tk.BooleanVar()

        tk.Checkbutton(dialogo, text="Estado Inicial", 
                       variable=es_inicial).pack()
        tk.Checkbutton(dialogo, text="Estado Final", 
                       variable=es_final).pack()

        def guardar_estado():
            estado = entrada_estado.get()
            self.pda.add_state(estado, es_inicial.get(), es_final.get())
            self.update_text_area()
            dialogo.destroy()

        tk.Button(dialogo, text="Guardar", command=guardar_estado).pack()

    def add_transition_dialog(self):
        """
        Diálogo para agregar transiciones
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Transición")

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
            self.pda.add_transition(
                entrada_estado_actual.get(), 
                entrada_simbolo.get() or None, 
                entrada_tope_pila.get(), 
                entrada_estado_siguiente.get(), 
                entrada_simbolos_apilar.get().split(',') if entrada_simbolos_apilar.get() else []
            )
            self.update_text_area()
            dialogo.destroy()

        tk.Button(dialogo, text="Guardar", command=guardar_transicion).pack()

    def test_string_dialog(self):
        """
        Diálogo para probar una cadena de entrada
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Probar Cadena")

        tk.Label(dialogo, text="Cadena de Entrada:").pack()
        entrada_cadena = tk.Entry(dialogo)
        entrada_cadena.pack()

        def probar_cadena():
            resultado = self.pda.process_input(entrada_cadena.get())
            messagebox.showinfo("Resultado", f"Cadena {'Aceptada' if resultado else 'Rechazada'}")
            dialogo.destroy()

        tk.Button(dialogo, text="Probar", command=probar_cadena).pack()

    def visualize_automaton(self):
        """
        Visualiza el autómata usando Graphviz
        """
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

        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".png")
        if nombre_archivo:
            dot.render(nombre_archivo, view=True, format='png')
