class PushdownAutomaton:
    def __init__(self):
        """
        Inicializa un Autómata de Pila con sus elementos básicos:
        - estados: Conjunto de todos los estados del autómata.
        - alfabeto_entrada: Conjunto de símbolos que el autómata puede leer como entrada.
        - alfabeto_pila: Conjunto de símbolos que pueden ser almacenados en la pila.
        - transiciones: Diccionario que define las reglas de transición.
        - estado_inicial: Estado de inicio del autómata.
        - simbolo_inicial_pila: Símbolo que se encuentra inicialmente en la pila.
        - estados_finales: Conjunto de estados de aceptación.
        - pila: Lista que simula la pila del autómata.
        """
        self.estados = set()
        self.alfabeto_entrada = set()
        self.alfabeto_pila = set()
        self.transiciones = {}
        self.estado_inicial = None
        self.simbolo_inicial_pila = None
        self.estados_finales = set()
        self.pila = []

    def agregar_estado(self, estado, es_inicial=False, es_final=False):
        """
        Agrega un estado al autómata y lo marca como inicial o final si corresponde.
        
        Parámetros:
        - estado: Nombre o identificador del estado.
        - es_inicial: Booleano para indicar si este estado es el inicial.
        - es_final: Booleano para indicar si este estado es final.
        """
        self.estados.add(estado)
        if es_inicial:
            self.estado_inicial = estado
        if es_final:
            self.estados_finales.add(estado)

    def agregar_transicion(self, estado_actual, simbolo_entrada, tope_pila, 
                           siguiente_estado, apilar):
        """
        Define una transición desde un estado a otro basándose en las condiciones.
        
        Parámetros:
        - estado_actual: Estado desde el cual se realiza la transición.
        - simbolo_entrada: Símbolo de entrada necesario para la transición.
        - tope_pila: Símbolo que debe estar en la cima de la pila.
        - siguiente_estado: Estado al que se transita.
        - apilar: Lista de símbolos que se deben apilar tras la transición.
        """
        if estado_actual not in self.transiciones:
            self.transiciones[estado_actual] = []
        
        self.transiciones[estado_actual].append({
            'entrada': simbolo_entrada,
            'tope_pila': tope_pila,
            'siguiente_estado': siguiente_estado,
            'apilar': apilar
        })

    def procesar_cadena(self, cadena_entrada):
        """
        Procesa una cadena de entrada para verificar si es aceptada por el autómata.
        
        Parámetros:
        - cadena_entrada: Cadena que se debe procesar.
        
        Retorna:
        - True si la cadena es aceptada; False en caso contrario.
        """
        estado_actual = self.estado_inicial
        # Inicializa la pila con el símbolo inicial
        self.pila = [self.simbolo_inicial_pila]
        
        # Convierte la cadena en una lista de símbolos para facilitar el manejo
        lista_entrada = list(cadena_entrada)
        
        while True:
            # Intenta encontrar y aplicar transiciones válidas
            if not self._buscar_transiciones_validas(estado_actual, lista_entrada):
                break
        
        # Verifica que se hayan consumido todos los símbolos, que el estado sea final,
        # y que la pila esté vacía
        return (not lista_entrada and 
                estado_actual in self.estados_finales and 
                len(self.pila) == 0)

    def _buscar_transiciones_validas(self, estado_actual, lista_entrada):
        """
        Busca y aplica la primera transición válida basada en el estado actual, 
        el símbolo de entrada y el tope de la pila.
        
        Parámetros:
        - estado_actual: El estado actual del autómata.
        - lista_entrada: Lista de símbolos restantes en la entrada.
        
        Retorna:
        - True si se aplicó una transición válida; False en caso contrario.
        """
        # Obtiene el símbolo en la cima de la pila (o None si está vacía)
        tope_pila = self.pila[-1] if self.pila else None
        # Obtiene el primer símbolo de la lista de entrada (o None si está vacía)
        simbolo_actual = lista_entrada[0] if lista_entrada else None
        
        # Recorre las transiciones posibles desde el estado actual
        for transicion in self.transiciones.get(estado_actual, []):
            # Verifica si la transición es válida:
            # 1. El símbolo de entrada coincide o es epsilon (None).
            # 2. El tope de la pila coincide con el definido en la transición.
            if (transicion['entrada'] == simbolo_actual or 
                transicion['entrada'] is None) and \
               transicion['tope_pila'] == tope_pila:
                
                # Cambia al siguiente estado
                estado_actual = transicion['siguiente_estado']
                
                # Actualiza la pila: elimina el tope y apila los nuevos símbolos
                self.pila.pop()
                self.pila.extend(reversed(transicion['apilar']))
                
                # Si la transición consumía un símbolo de entrada, se elimina
                if transicion['entrada'] is not None:
                    lista_entrada.pop(0)
                
                return True  # Se aplicó una transición válida
        
        return False  # No se encontró ninguna transición válida
