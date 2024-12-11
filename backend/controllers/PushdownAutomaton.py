import asyncio
import websockets
import json

class PushdownAutomaton:
    def __init__(self):
        """
        Inicializa un Autómata de Pila (PDA) con sus componentes esenciales.
        """
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = {}
        self.current_state = None
        self.stack = []
        self.input_string = None
        self.transition_log = []

    def initialize(self, language_type, input_string):
        """
        Inicializa el autómata para un tipo de lenguaje específico.
        """
        self.reset()

        # Configuración según el tipo de lenguaje
        if language_type.lower() == 'a^n b^n':
            self._setup_balanced_language(input_string)
        elif language_type.lower() == 'a^n b^n c^n':
            self._setup_three_characters_language(input_string)
        elif language_type.lower() == 'a^n b^n c^n d^n':
            self._setup_four_characters_language(input_string)  # Nuevo lenguaje
        else:
            raise ValueError(f"Lenguaje no soportado: {language_type}")

        self.input_string = list(input_string)
        return self

    def _setup_balanced_language(self, input_string):
        """
        Configura un autómata para lenguaje a^n b^n.
        """
        # Agregar estados
        self.add_state('q0', is_initial=True)
        self.add_state('q1')
        self.add_state('q2')
        self.add_state('q3', is_final=True)

        # Transiciones para a^n b^n
        self.add_transition('q0', 'a', 'Z0', 'q1', ['A', 'Z0'])
        self.add_transition('q1', 'a', 'A', 'q1', ['A', 'A'])
        self.add_transition('q1', 'b', 'A', 'q2', [])
        self.add_transition('q2', 'b', 'A', 'q2', [])
        self.add_transition('q2', None, 'Z0', 'q3', ['Z0'])

    def _setup_three_characters_language(self, input_string):
        """
        Configura un autómata para lenguaje a^n b^n c^n.
        """
        # Agregar estados
        self.add_state('q0', is_initial=True)
        self.add_state('q1')
        self.add_state('q2')
        self.add_state('q3')
        self.add_state('q4', is_final=True)

        # Transiciones para a^n b^n c^n
        self.add_transition('q0', 'a', 'Z0', 'q1', ['A', 'Z0'])
        self.add_transition('q1', 'a', 'A', 'q1', ['A', 'A'])
        self.add_transition('q1', 'b', 'A', 'q2', [])
        self.add_transition('q2', 'b', 'A', 'q2', [])
        self.add_transition('q2', 'c', 'A', 'q3', [])
        self.add_transition('q3', 'c', 'A', 'q3', [])
        self.add_transition('q3', None, 'Z0', 'q4', ['Z0'])

    def _setup_four_characters_language(self, input_string):
        """
        Configura un autómata para lenguaje a^n b^n c^n d^n.
        """
        # Agregar estados
        self.add_state('q0', is_initial=True)
        self.add_state('q1')
        self.add_state('q2')
        self.add_state('q3')
        self.add_state('q4')
        self.add_state('q5', is_final=True)

        # Transiciones para a^n b^n c^n d^n
        self.add_transition('q0', 'a', 'Z0', 'q1', ['A', 'Z0'])
        self.add_transition('q1', 'a', 'A', 'q1', ['A', 'A'])
        self.add_transition('q1', 'b', 'A', 'q2', [])
        self.add_transition('q2', 'b', 'A', 'q2', [])
        self.add_transition('q2', 'c', 'A', 'q3', [])
        self.add_transition('q3', 'c', 'A', 'q3', [])
        self.add_transition('q3', 'd', 'A', 'q4', [])
        self.add_transition('q4', 'd', 'A', 'q4', [])
        self.add_transition('q4', None, 'Z0', 'q5', ['Z0'])

    def process(self, symbol=None):
        """
        Procesa un símbolo de entrada.
        """
        if symbol is not None:
            self.input_string.append(symbol)

        result = self._process_symbol()

        return type('ProcessResult', (), {
            'current_state': self.current_state,
            'stack': self.stack.copy(),
            'transitions': self.transition_log
        })

    def _process_symbol(self):
        """
        Procesamiento interno de símbolos.
        """
        if not self.input_string:
            return False

        symbol = self.input_string.pop(0)
        stack_top = self.stack[-1] if self.stack else 'Z0'

        # Buscar transición válida
        key = (self.current_state, symbol, stack_top)
        transitions = self.transitions.get(key, [])

        if not transitions:
            raise ValueError(f"Transición no válida: {key}")

        # Tomar la primera transición (puede extenderse para múltiples)
        transition = transitions[0]

        # Actualizar estado y pila
        self.current_state = transition['next_state']

        if stack_top != 'Z0':  # Solo desapilar si no es el símbolo base 'Z0'
            self.stack.pop()  # Desapilar un símbolo

        # Apilar nuevos símbolos (en reversa)
        self.stack.extend(reversed(transition['stack_push']))  # Apilar los nuevos símbolos

        # Registrar transición
        self.transition_log.append([f"{self.current_state}", f"Symbol: {symbol}", f"Stack: {self.stack}"])

        return True

    def reset(self):
        """
        Reinicia el estado del autómata.
        """
        self.current_state = self.start_state
        self.stack = ['Z0']

    def add_state(self, state, is_initial=False, is_final=False):
        """
        Agrega un estado al autómata.
        """
        self.states.add(state)
        if is_initial:
            self.start_state = state
        if is_final:
            self.final_states.add(state)

    def add_transition(self, from_state, symbol, stack_top, to_state, stack_push):
        """
        Agrega una transición al autómata.
        """
        key = (from_state, symbol, stack_top)
        if key not in self.transitions:
            self.transitions[key] = []
        self.transitions[key].append({'next_state': to_state, 'stack_push': stack_push})

async def handle_client(websocket, path):
    aut = PushdownAutomaton()

    # Inicializar autómata con lenguaje y cadena recibidos del cliente
    async for message in websocket:
        data = json.loads(message)
        language_type = data['language_type']
        input_string = data['input_string']

        aut.initialize(language_type, input_string)

        response = aut.process()

        # Enviar estado actual, pila y transiciones al cliente
        await websocket.send(json.dumps({
            'current_state': response.current_state,
            'stack': response.stack,
            'transitions': response.transitions
        }))

async def main():
    server = await websockets.serve(handle_client, "localhost", 8000)
    await server.wait_closed()

asyncio.run(main())
