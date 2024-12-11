from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from fastapi import Body, Path
from fastapi import status as status_code
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
        id=autom.aut_id, alph=autom.alph, Q=autom.Q, F=autom.F, q0=autom.q0
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
        transition.char, transition.state_from, transition.state_to
    )

    return {
        "message": "Transición agregada correctamente",
        "transitions": automatons[aut_id].transitions,
    }


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


@app.post("/pushdown/initialize/{aut_id}", status_code=status_code.HTTP_201_CREATED)
async def initialize_pushdown_automat(
    aut_id: str = Path(...),
    create_pushdown_automaton: create_pushdown_automaton = Body(...),
):
    try:
        pda = PushdownAutomaton()
        language_type = create_pushdown_automaton.language_type
        input_string = create_pushdown_automaton.input_string

        pda.initialize(language_type, input_string)

        pda_automatons[create_pushdown_automaton.aut_id] = pda

        return {"message": "Autómata de Pila inicializado correctamente!"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/pushdown/process/{aut_id}")
async def process_pushdown()
    ...