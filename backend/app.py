from flask import Flask, request, jsonify, session
from PushdownAutomaton import PushdownAutomaton  # Asumimos que la clase PushdownAutomaton está en pushdown_automaton.py
from flask_cors import CORS
import uuid



app = Flask(__name__)

# Habilitar CORS para todos los orígenes
CORS(app)
app.secret_key = str(uuid.uuid4())  # Clave secreta para gestionar sesiones

@app.route('/initialize', methods=['POST'])
def initialize():
    """
    Inicializa el autómata con el lenguaje y la cadena de entrada
    """
    try:
        # Obtener datos del front-end
        data = request.get_json()
        language_type = data.get('language_type')
        input_string = data.get('input_string')

        # Crear una nueva instancia del autómata
        pda = PushdownAutomaton()
        pda.initialize(language_type, input_string)

        # Guardar el autómata en la sesión para mantener el estado
        session['pda'] = pda

        return jsonify({"message": "Autómata inicializado correctamente"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/process', methods=['POST'])
def process():
    """
    Procesa un símbolo de entrada y devuelve el estado actual y el contenido de la pila
    """
    try:
        # Verificar si el autómata ya ha sido inicializado en la sesión
        if 'pda' not in session:
            return jsonify({"error": "El autómata no ha sido inicializado"}), 400

        # Obtener el símbolo a procesar
        data = request.get_json()
        symbol = data.get('symbol')

        # Recuperar el autómata de la sesión
        pda = session['pda']

        # Procesar el símbolo
        result = pda.process(symbol)

        # Devuelve el resultado al front-end
        return jsonify({
            "current_state": result.current_state,
            "stack": result.stack,
            "transitions": result.transitions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/acceptance', methods=['GET'])
def check_acceptance():
    """
    Verifica si la cadena ha sido aceptada por el autómata
    """
    try:
        # Verificar si el autómata ya ha sido inicializado en la sesión
        if 'pda' not in session:
            return jsonify({"error": "El autómata no ha sido inicializado"}), 400

        # Recuperar el autómata de la sesión
        pda = session['pda']

        # Verificar si la cadena es aceptada
        accepted = pda.is_accepted()

        # Devuelve el resultado
        return jsonify({"accepted": accepted})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/reset', methods=['POST'])
def reset():
    """
    Resetea el autómata y limpia la sesión
    """
    try:
        # Verificar si el autómata ya ha sido inicializado
        if 'pda' not in session:
            return jsonify({"error": "El autómata no ha sido inicializado"}), 400

        # Recuperar el autómata y resetearlo
        pda = session['pda']
        pda.reset()

        # Guardar el autómata resetado en la sesión
        session['pda'] = pda

        return jsonify({"message": "Autómata reseteado correctamente"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
