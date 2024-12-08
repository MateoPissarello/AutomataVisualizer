import tkinter as tk
from automata.fa.dfa import DFA
# from LanguageType import LanguageType
from views.LanguageTypeView import LanguageTypeView
from views.PushdownAutomatonView import PushdownAutomatonView

class MainView:
    def __init__(self, root):
        self.root = root

        self.root.title("Menú principal")
        self.root.geometry("400x200")
        self.title_label = tk.Label(root, text="Menú principal", font=("Arial", 16))
        self.title_label.pack()

        self.language_type_btn = tk.Button(
            root, text="Tipo de lenguaje", command=self.language_type
        )
        self.language_type_btn.pack()

        self.dfa_btn = tk.Button(
            root,
            text="Autómata Finito Determinista",
            command=self.deterministic_finite_automata,
        )
        self.dfa_btn.pack()

        self.reduce_automata_btn = tk.Button(
            root, text="Reducir autómata", command=self.reduce_automata
        )
        self.reduce_automata_btn.pack()

        self.pushdown_automata_btn = tk.Button(
            root, text="Autómata de Pila", command=self.pushdown_automata
        )
        self.pushdown_automata_btn.pack()

        self.turing_machine_btn = tk.Button(
            root, text="Máquina de Turing", command=self.turing_machine
        )

    def language_type(self):
        LanguageTypeView(self.root)
        print()

    def deterministic_finite_automata(self):
        print("Deterministic Finite Automata")

    def reduce_automata(self):
        print("Reduce Automata")

    def pushdown_automata(self):
        # Abrir la vista del Autómata de Pila
        PushdownAutomatonView(self.root)

    def turing_machine(self):
        print("Turing Machine")

root = tk.Tk()
MainView(root)
root.mainloop()
