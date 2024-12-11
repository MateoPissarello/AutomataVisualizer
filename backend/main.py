from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import json


from automaton import Automaton
from controllers.PushdownAutomaton import PushdownAutomaton
# Diccionarios donde almacenamos los autómatas por su ID
automatons: Dict[str, Automaton] = {}
pda_automatons: Dict[str, PushdownAutomaton] = {}

# Crear la instancia de FastAPI
app = FastAPI()
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================== Autómata Regular (Automaton) ==============================

# Modelo para crear un autómata regular
class create_automata(BaseModel):
    aut_id: str
    alph: List[str]
    Q: List[str]
    F: List[str]
    q0: str

@app.post("/create/{aut_id}")
async def create_automaton_route(autom: create_automata):
    """
    Crear un autómata regular y almacenarlo por su ID.
    """
    automatons[autom.aut_id] = Automaton(
        id=autom.aut_id, 
        alph=autom.alph,
        Q=autom.Q,
        F=autom.F,
        q0=autom.q0
    )
    
    return {"message": "Automata Regular Creado correctamente!"}

# Modelo para agregar una transición al autómata regular
class add_transition(BaseModel):
    char: str
    state_from: str
    state_to: str

@app.post("/automata/{aut_id}/add_transition")
async def add_transition_route(aut_id: str, transition: add_transition):
    """
    Agregar una transición al autómata regular.
    """
    if aut_id not in automatons:
        return {"error": f"Automata con ID {aut_id} no encontrado"}
    
    automatons[aut_id].add_transition(
        transition.char,
        transition.state_from,
        transition.state_to
    )
    
    return {"message": "Transición agregada correctamente", "transitions": automatons[aut_id].transitions}

# Ruta para probar una cadena en el autómata regular
@app.get("/automata/{aut_id}/test/{string_to_test}")
async def test_string_route(aut_id: str, string_to_test: str):
    """
    Probar una cadena en el autómata regular y devolver los pasos.
    """
    if aut_id not in automatons:
        return {"error": f"Automata con ID {aut_id} no encontrado"}
    
    steps = automatons[aut_id].test_string(string_to_test)
    
    return {"steps": steps}


# ============================== Autómata de Pila (PushdownAutomaton) ==============================

# Modelo para crear un autómata de pila
class create_pushdown_automaton(BaseModel):
    aut_id: str
    language_type: str  # Acepta tipos como 'a^n b^n', 'a^n b^n c^n', etc.
    input_string: str

@app.post("/creation/pushdown/")
async def create_pushdown_automaton_route(autom: create_pushdown_automaton):
    """
    Crear un autómata de pila y almacenarlo por su ID.
    """
    automaton = PushdownAutomaton()
    automaton.initialize(autom.language_type, autom.input_string)
    pda_automatons[autom.aut_id] = automaton
    return {"message": "Automata de Pila Creado correctamente!"}

# Modelo para agregar una transición al autómata de pila
class add_pushdown_transition(BaseModel):
    symbol: str
    state_from: str
    stack_top: str
    next_state: str
    stack_push: List[str]

@app.post("/add_transition/pushdown")
async def add_pushdown_transition_route(aut_id: str, transition: add_pushdown_transition):
    """
    Agregar una transición al autómata de pila.
    """
    if aut_id not in pda_automatons:
        return {"error": f"Automata de Pila con ID {aut_id} no encontrado"}
    
    automaton = pda_automatons[aut_id]
    automaton.add_transition(
        transition.state_from,
        transition.symbol,
        transition.stack_top,
        transition.next_state,
        transition.stack_push
    )
    
    return {"message": "Transición agregada correctamente", "transitions": automaton.transitions}

# Ruta para probar una cadena en el autómata de pila
@app.get("/test/pushdown{string_to_test}")
async def test_pushdown_string_route(aut_id: str, string_to_test: str):
    """
    Probar una cadena en el autómata de pila y devolver los pasos.
    """
    if aut_id not in pda_automatons:
        return {"error": f"Automata de Pila con ID {aut_id} no encontrado"}
    
    automaton = pda_automatons[aut_id]
    steps = automaton.test_string(string_to_test)
    
    return {"steps": steps}
