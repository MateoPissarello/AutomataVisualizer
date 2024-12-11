
let automataId = "Automaton";
let steps = []
const BASE_URL = "http://localhost:8000";

function parseTransitions(states) {
  // Obtener el contenido del textarea
  const text = document.getElementById("transitions").value;

  // Crear un objeto para almacenar las transiciones
  let transitions = {};

  // Usar una expresión regular para encontrar todas las transiciones
  const regex = /\(\s*([a-zA-Z]+\d+)\s*,\s*([a-zA-Z])\s*\)\s*->\s*(q\d+)/g;
  let match;

  // Iterar sobre todas las coincidencias
  while ((match = regex.exec(text)) !== null) {
    const fromState = match[1]; // Estado de origen (q0, q1, q2, ...)
    if (states.indexOf(fromState) == -1) {
      alert("El estado " + fromState + " no ha sido creado aun");
      continue;
    }
    const char = match[2]; // Carácter (a, b, c, ...)
    const toState = match[3]; // Estado de destino (q1, q2, q3, ...)

    // Asegurarse de que el estado de origen exista en el objeto
    if (!transitions[fromState]) {
      transitions[fromState] = [];
    }

    // Agregar la transición al estado de origen
    transitions[fromState].push({
      char: char,
      from: fromState,
      to: toState,
    });
  }

  return transitions;
}

async function addTransition(autId, transition) {

  
  try {
    const response = await fetch(
      `${BASE_URL}/automata/${autId}/add_transition`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(transition),
      }
    );

    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    console.log(
      `Transition ${JSON.stringify(transition)} added successfully:`,
      data
    );
  } catch (error) {
    console.error(
      `Failed to add transition ${JSON.stringify(transition)}:`,
      error
    );
  }
}

async function createAutomaton(createAutomatonData) {
  if (!createAutomatonData.q0) {
    alert("No hay estado inicial");
    return;
  }
  try {
    const response = await fetch(
      `${BASE_URL}/create/${createAutomatonData.aut_id}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(createAutomatonData),
      }
    );

    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    console.log("Automaton created successfully:", data);
  } catch (error) {
    console.error("Failed to create automaton:", error);
  }
}

// Obtener los datos del formulario
function getAutomatonData() {
  const states = document
    .getElementById("Q")
    .value.split(",")
    .map((s) => s.trim());
  const alphabet = document
    .getElementById("alphabet")
    .value.split(",")
    .map((s) => s.trim());
  const initialState = document.getElementById("initialState").value.trim();
  const finalStates = document
    .getElementById("finalStates")
    .value.split(",")
    .map((s) => s.trim());
  const transitionsInput = document.getElementById("transitions").value.trim();
  const transitions = parseTransitions(states, transitionsInput);

  if (!alphabet.length || !initialState || !finalStates.length) {
    alert("Por favor, completa todos los campos correctamente.");
    return null;
  }

  return {
    Q: states,
    Σ: alphabet,
    q0: initialState,
    F: finalStates,
    δ: transitions,
  };
}

// Dibujar un autómata usando Vis.js
function drawAutomaton(containerId, automaton) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`No se encontró el contenedor con ID: ${containerId}`);
    return;
  }

  const nodes = automaton.Q.map((state) => ({
    id: state,
    label: state,
    shape: automaton.F.includes(state) ? "ellipse" : "circle",
    font: { size: 14 },
    color: automaton.F.includes(state)
            ? { border: "black", background: "#ccffcc" }
            : automaton.Q.includes(state)
            ? { border: "black", background: "#ccff00" }
            : undefined,
    }));

  let edges = [];
  for (let stateId in automaton.δ) {
    edges.push(
      automaton.δ[stateId].map((transition) => {
        addTransition(automataId, {
          char: transition.char,
          state_from: transition.from,
          state_to: transition.to,
        });

        return {
          from: transition.from,
          to: transition.to,
          label: transition.char,
          arrows: "to",
        };
      })
    );
  }

  edges = edges.flat();

  const data = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges),
  };

  const options = {
    nodes: {
      borderWidth: 2,
    },
    edges: {
      font: { align: "middle" },
    },
    physics: {
      enabled: false, // Desactivamos la física para evitar atracción
    },
    layout: {
      improvedLayout: true, // Diseño mejorado para distribución automática
    },
  };

  new vis.Network(container, data, options);
}

// Pintar el autómata inicial
function drawInitialAutomaton() {
  const automaton = getAutomatonData();

  if (!automaton) return 
  const { Q, Σ, q0, F, δ } = automaton;
  
  const createAutomatonData = {
    aut_id: "Automaton",
    alph: Σ,
    Q,
    F,
    q0: q0,
  };
  drawAutomaton("graph-initial", automaton);
  createAutomaton(createAutomatonData);
}

// Function to test strings with the automaton
async function testString(autId, string) {
  try {
    const response = await fetch(
      `${BASE_URL}/automata/${autId}/test/${string}`
    );

    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    return  data
  } catch (error) {
    console.error(`Failed to test string '${string}':`, error);
  }
}

document
  .getElementById("testStringInput")
  .addEventListener("keyup", async (e) => {
    const automaton = getAutomatonData();
    
    if (!automaton) return;

    const { Q, Σ, q0, F, δ } = automaton;

    const createAutomatonData = {
      aut_id: automataId,
      alph: Σ,
      Q,
      F,
      q0: q0,
    };

    await createAutomaton(createAutomatonData);

    for (let stateId in automaton.δ) {
      for (let transition of automaton.δ[stateId]) {
        await addTransition(automataId, {
          char: transition.char,
          state_from: transition.from,
          state_to: transition.to,
        });
      }
    }

    if (e.target.value.length > 1) {
      try {
        // Asegúrate de esperar la respuesta
        const response = await testString(automataId, e.target.value);

        // Usa el contenido de la respuesta
        document.getElementById("serverResponse").textContent = response.message;

        steps = response.steps
        document.getElementById("serverResponse").classList.add(
         response.accepted ? "text-green-700": "text-red-700"
        )

      } catch (error) {
        console.error("Error testing string:", error);
        document.getElementById("serverResponse").textContent = "Error al procesar la cadena.";
        document.getElementById("serverResponse").classList.add("text-red-700")
 
      }
    }
  });

function showTestStringModule() {
  document.getElementById("testStringContainer").classList.toggle("hidden");
}


function loadStringTestAnimation(){
  document.getElementById("loadStringTestAnimationButton").setAttribute("disabled","")
  console.log(steps);
  
  let counter = 0
  const intervalId = setInterval(() => {
    if (counter >= steps.length) {
        clearInterval(intervalId); // Detiene la ejecución después de n veces
        console.log("Execution completed.");
        document.getElementById("loadStringTestAnimationButton").removeAttribute("disabled")

        return;
    }

    animateStep(counter); // Ejecuta la función con el elemento actual
    counter++; // Incrementa el contador
}, 2000); // Intervalo de 1 segundo

}



function animateStep(stepIndex){


  const stringArr = document.getElementById("testStringInput").value.split("")
  const fragment = document.createDocumentFragment()
  const currentStep = steps[stepIndex]



  for( let charInd in stringArr){
    const span = document.createElement("span")
    span.classList.add("p-2" ,"bg-slate-300" )
    if(charInd == stepIndex){
      span.classList.replace("bg-slate-300", "bg-green-400")
      span.classList.add( 'text-white' ,'font-bold' )

      if( steps[stepIndex].nextState == undefined){
        setTimeout(()=>{
          span.classList.replace("bg-green-400",'bg-red-300')
        },1500)
      }
    }
    span.textContent = stringArr[charInd]
    fragment.appendChild(span)
    
  }

  document.getElementById("estadoActual").textContent = steps[stepIndex].currState
  document.getElementById("proximoEstado").textContent = steps[stepIndex].nextState ?? "???"
  
  document.getElementById("testStringVisualString").replaceChildren(fragment)

}