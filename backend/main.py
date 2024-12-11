from fastapi import FastAPI
from automaton import Automaton
from pydantic import BaseModel
import json


automatons: dict[Automaton] = dict()
app = FastAPI()

class create_automata(BaseModel):
    aut_id: str
    alph: list[str]
    Q: list[str]
    F: list[str]
    q0: str




@app.post("/create/{aut_id}")
async def create_automaton(autom : create_automata):
    
    automatons[autom.aut_id] = Automaton(
        id=autom.aut_id, 
        alph=autom.alph,
        Q=autom.Q,
        F=autom.F,
        q0=autom.q0
    )
    
    return {"message": "Automata Creado correctamente!"}

class add_transition(BaseModel):
    char: str
    state_from: str
    state_to: str

@app.post("/automata/{aut_id}/add_transition")
async def create_automaton(aut_id, transition:add_transition ):
    automatons[aut_id].add_transition(
        transition.char,
        transition.state_from,
        transition.state_to
    )
    
    return automatons[aut_id].transitions[(transition.state_from,transition.char)]
    

@app.get("/automata/{aut_id}/test/{string_to_test}")
async def create_automaton(aut_id, string_to_test ):
    print(f"ID: {aut_id}, String: {string_to_test}")
    steps = automatons[aut_id].test_string(string_to_test)
    return steps
    


        