
class Automaton:
    def __init__(self,id, Q,q0, alph, F):
        self.id = id
        self.Q = Q        
        self.q0 = q0        
        self.alph = alph        
        self.F = F
        self.transitions = dict()
        
    def add_transition( self, char, fromState, toState ):
        self.transitions[(fromState, char)] = toState
        return True



    def test_string(self, string:str) -> bool:
        steps  = {
            "accepted":None,
            "message":"",
            "steps":[]
        }
        currState = self.q0
        for i, char in enumerate(string):
            
            if char not in self.alph:
                steps["accepted"] = False
                steps["message"] = f"Error: {char} not in alphabet"
                steps["steps"].append({
                    "char":char,
                    "currState": currState,
                    "nextState": None,
                    "position": i
                })
                return steps
                
            
            try:
                nextState = self.transitions[(currState , char)]
                print(f"({ currState },{ char }) -> {nextState}")
            except Exception: 
                print(f"Estado muerto ({ currState },{ char })")
                steps["steps"].append({
                    "char":char,
                    "currState": currState,
                    "nextState": None,
                    "position": i
                })
                steps["accepted"] = False
                steps["message"] = f"Estado muerto ({ currState },{ char }) -> ?"
                return steps
            
            if nextState:
                steps["steps"].append({
                    "char":char,
                    "currState": currState,
                    "nextState": nextState,
                    "position": i
                })
                
                currState = nextState
                
            
        if currState in self.F:
            steps["message"] = f"Cadena aceptada"
            steps["accepted"] = True
            return steps
        else:
            steps["message"] = f"Cadena NO aceptada"
            steps["accepted"] = False
            return steps
        