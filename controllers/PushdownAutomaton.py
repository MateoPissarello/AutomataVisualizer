class PushdownAutomaton:
    def __init__(self):
        """
        Inicializa un Autómata de Pila con sus elementos básicos
        """
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = {}

    def add_state(self, state, is_initial=False, is_final=False):
        """
        Agrega un estado al autómata y lo marca como inicial o final si corresponde.
        
        Parámetros:
        - state: Nombre o identificador del estado.
        - is_initial: Booleano para indicar si este estado es el inicial.
        - is_final: Booleano para indicar si este estado es final.
        """
        self.states.add(state)
        if is_initial:
            self.start_state = state
        if is_final:
            self.final_states.add(state)

    def add_transition(self, current_state, input_symbol, stack_top, 
                       next_state, stack_push):
        """
        Define una transición desde un estado a otro basándose en las condiciones.
        
        Parámetros:
        - current_state: Estado desde el cual se realiza la transición.
        - input_symbol: Símbolo de entrada necesario para la transición.
        - stack_top: Símbolo que debe estar en la cima de la pila.
        - next_state: Estado al que se transita.
        - stack_push: Lista de símbolos que se deben apilar tras la transición.
        """
        if current_state not in self.transitions:
            self.transitions[current_state] = []
        
        self.transitions[current_state].append({
            'input': input_symbol,
            'stack_top': stack_top,
            'next_state': next_state,
            'stack_push': stack_push
        })

    def process_input(self, input_string):
        """
        Procesa una cadena de entrada para verificar si es aceptada por el autómata.
        
        Parámetros:
        - input_string: Cadena que se debe procesar.
        
        Retorna:
        - True si la cadena es aceptada; False en caso contrario.
        """
        current_state = self.start_state
        stack = ['Z0']  # Símbolo inicial de pila
        
        # Convierte la cadena en una lista de símbolos para facilitar el manejo
        input_list = list(input_string)
        
        while True:
            # Intenta encontrar y aplicar transiciones válidas
            if not self._find_valid_transition(current_state, input_list, stack):
                break
        
        # Verifica que se hayan consumido todos los símbolos, que el estado sea final,
        # y que la pila esté vacía
        return (not input_list and 
                current_state in self.final_states and 
                len(stack) == 0)

    def _find_valid_transition(self, current_state, input_list, stack):
        """
        Busca y aplica la primera transición válida basada en el estado actual, 
        el símbolo de entrada y el tope de la pila.
        
        Parámetros:
        - current_state: El estado actual del autómata.
        - input_list: Lista de símbolos restantes en la entrada.
        - stack: Pila actual del autómata.
        
        Retorna:
        - True si se aplicó una transición válida; False en caso contrario.
        """
        # Obtiene el símbolo en la cima de la pila (o None si está vacía)
        stack_top = stack[-1] if stack else None
        # Obtiene el primer símbolo de la lista de entrada (o None si está vacía)
        current_symbol = input_list[0] if input_list else None
        
        # Recorre las transiciones posibles desde el estado actual
        for transition in self.transitions.get(current_state, []):
            # Verifica si la transición es válida:
            # 1. El símbolo de entrada coincide o es epsilon (None).
            # 2. El tope de la pila coincide con el definido en la transición.
            if (transition['input'] == current_symbol or 
                transition['input'] is None) and \
               transition['stack_top'] == stack_top:
                
                # Cambia al siguiente estado
                current_state = transition['next_state']
                
                # Actualiza la pila: elimina el tope y apila los nuevos símbolos
                stack.pop()
                stack.extend(reversed(transition['stack_push']))
                
                # Si la transición consumía un símbolo de entrada, se elimina
                if transition['input'] is not None:
                    input_list.pop(0)
                
                return True  # Se aplicó una transición válida
        
        return False  # No se encontró ninguna transición válidaclass PushdownAutomaton:
    def __init__(self):
        """
        Inicializa un Autómata de Pila (PDA) con sus componentes esenciales:
        - Conjunto de estados.
        - Estado inicial.
        - Conjunto de estados finales.
        - Diccionario de transiciones.
        """
        self.states = set()  # Conjunto de todos los estados posibles.
        self.start_state = None  # Estado inicial del autómata.
        self.final_states = set()  # Conjunto de estados finales.
        self.transitions = {}  # Diccionario de transiciones.

    def add_state(self, state, is_initial=False, is_final=False):
        """
        Agrega un estado al autómata. Además, marca si es un estado inicial o final.
        
        Parámetros:
        - state: Nombre del estado.
        - is_initial: Indica si este estado es el estado inicial (True/False).
        - is_final: Indica si este estado es un estado final (True/False).
        """
        self.states.add(state)  # Agrega el estado al conjunto de estados.
        
        if is_initial:
            if self.start_state:
                raise ValueError(f"Ya existe un estado inicial: {self.start_state}")  # No se permite más de un estado inicial.
            self.start_state = state  # Define el estado inicial.

        if is_final:
            self.final_states.add(state)  # Agrega el estado a los estados finales.

    def add_transition(self, current_state, input_symbol, stack_top, next_state, stack_push):
        """
        Define una transición entre dos estados, especificando el símbolo de entrada y la pila.
        
        Parámetros:
        - current_state: El estado actual desde el cual se realiza la transición.
        - input_symbol: El símbolo de entrada necesario para hacer la transición.
        - stack_top: El símbolo en la cima de la pila que se necesita para hacer la transición.
        - next_state: El estado al que se transita si la transición es válida.
        - stack_push: Una lista de símbolos que se deben apilar en la pila tras la transición.
        """
        if current_state not in self.states:
            raise ValueError(f"El estado actual '{current_state}' no existe.")
        if next_state not in self.states:
            raise ValueError(f"El estado siguiente '{next_state}' no existe.")
        
        # Crea una clave única para cada transición basada en el estado, el símbolo de entrada y la cima de la pila.
        key = (current_state, input_symbol, stack_top)
        if key not in self.transitions:
            self.transitions[key] = []  # Si no existe la clave, crea una lista para las transiciones.

        # Agrega la transición al conjunto de transiciones.
        self.transitions[key].append({'next_state': next_state, 'stack_push': stack_push})

    def process_input(self, input_string):
        """
        Procesa una cadena de entrada y verifica si es aceptada por el autómata.
        
        Parámetros:
        - input_string: Cadena que se debe procesar.
        
        Retorna:
        - True si la cadena es aceptada, es decir, si llega a un estado final con la pila vacía.
        - False en caso contrario.
        """
        if not self.start_state:
            raise ValueError("El autómata no tiene un estado inicial definido.")  # Verifica que exista un estado inicial.

        current_state = self.start_state  # Empieza desde el estado inicial.
        stack = ['Z0']  # La pila comienza con el símbolo inicial 'Z0'.
        
        # Convierte la cadena de entrada en una lista para procesar cada símbolo.
        input_list = list(input_string)
        
        while input_list:  # Mientras haya símbolos de entrada por procesar.
            # Intenta encontrar una transición válida con el estado actual, símbolo de entrada y cima de la pila.
            if not self._find_valid_transition(current_state, input_list, stack):
                return False  # Si no hay transiciones válidas, la entrada no es aceptada.

        # La entrada es aceptada si:
        # 1. El estado actual es un estado final.
        # 2. La pila está vacía (sin símbolos).
        return current_state in self.final_states and not stack

    def _find_valid_transition(self, current_state, input_list, stack):
        """
        Busca y aplica la primera transición válida basada en el estado actual, el símbolo de entrada 
        y el símbolo en la cima de la pila.
        
        Parámetros:
        - current_state: El estado actual en el autómata.
        - input_list: La lista de símbolos restantes de la entrada.
        - stack: La pila actual que el autómata maneja.
        
        Retorna:
        - True si se encontró una transición válida y se aplicó.
        - False si no se encontró ninguna transición válida.
        """
        stack_top = stack[-1] if stack else None  # Obtiene el símbolo en la cima de la pila (None si está vacía).
        current_symbol = input_list[0] if input_list else None  # Obtiene el primer símbolo de la entrada (None si está vacía).
        
        # Busca transiciones posibles usando la tupla (estado, símbolo de entrada, símbolo en la pila).
        key = (current_state, current_symbol, stack_top)
        transitions = self.transitions.get(key, [])  # Si no hay transiciones para la clave, retorna una lista vacía.

        for transition in transitions:
            next_state = transition['next_state']  # El estado al que se transita.
            stack_push = transition['stack_push']  # Los símbolos que se deben apilar.

            # Realiza la transición, actualizando el estado y la pila.
            current_state = next_state
            stack.pop()  # Elimina el símbolo de la cima de la pila.
            stack.extend(reversed(stack_push))  # Apila los nuevos símbolos en el orden correcto.

            # Si la transición consumió un símbolo de entrada, lo eliminamos.
            if current_symbol is not None:
                input_list.pop(0)
            
            return True  # Transición válida aplicada.

        return False  # No se encontró ninguna transición válida.

    def get_transitions(self):
        """
        Retorna un diccionario con todas las transiciones del autómata.
        """
        return self.transitions

    def __str__(self):
        """
        Devuelve una representación en cadena del autómata para facilitar la depuración.
        """
        result = f"Estado inicial: {self.start_state}\n"
        result += f"Estados finales: {', '.join(self.final_states)}\n"
        result += "Transiciones:\n"
        
        # Muestra todas las transiciones en formato legible.
        for (state, symbol, stack_top), transitions in self.transitions.items():
            for t in transitions:
                result += f"{state} --({symbol}, {stack_top})--> {t['next_state']} [{','.join(t['stack_push'])}]\n"
        
        return result

