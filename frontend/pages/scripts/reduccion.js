// Obtener los datos del formulario
function getAutomatonData() {
    const states = document.getElementById("Q").value.split(",").map((s) => s.trim());
    const alphabet = document.getElementById("alphabet").value.split(",").map((s) => s.trim());
    const initialState = document.getElementById("initialState").value.trim();
    const finalStates = document.getElementById("finalStates").value.split(",").map((s) => s.trim());
    const transitionsInput = document.getElementById("transitions").value.trim();
  
    const transitions = transitionsInput
      .split("\n")
      .filter((line) => line.trim() !== "")
      .map((line) => {
        const [state_from, input, state_to] = line.split(",").map((s) => s.trim());
        return { state_from, input, state_to };
      });
  
    if (!states.length || !alphabet.length || !initialState || !finalStates.length || !transitions.length) {
      alert("Por favor, completa todos los campos correctamente.");
      return null;
    }
  
    return { Q: states, Σ: alphabet, q0: initialState, F: finalStates, δ: transitions };
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
      color: automaton.F.includes(state) ? { border: "black", background: "#ccffcc" } : undefined,
    }));
  
    const edges = automaton.δ.map((transition) => ({
      from: transition.state_from,
      to: transition.state_to,
      label: transition.input,
      arrows: "to",
    }));
  
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
  
  // Eliminar estados inalcanzables
  function removeUnreachableStates(automaton) {
    const reachableStates = new Set([automaton.q0]);
    const queue = [automaton.q0];
  
    while (queue.length > 0) {
      const currentState = queue.shift();
      automaton.δ
        .filter((t) => t.state_from === currentState)
        .forEach((t) => {
          if (!reachableStates.has(t.state_to)) {
            reachableStates.add(t.state_to);
            queue.push(t.state_to);
          }
        });
    }
  
    const reachableTransitions = automaton.δ.filter((t) => reachableStates.has(t.state_from));
    return {
      Q: automaton.Q.filter((state) => reachableStates.has(state)),
      Σ: automaton.Σ,
      q0: automaton.q0,
      F: automaton.F.filter((state) => reachableStates.has(state)),
      δ: reachableTransitions,
    };
  }
  
  // Verificar si el autómata ya es mínimo
  function isAutomatonMinimal(automaton) {
    const partitions = [new Set(automaton.F), new Set(automaton.Q.filter((s) => !automaton.F.includes(s)))];
    let refined = true;
  
    while (refined) {
      refined = false;
      const newPartitions = [];
  
      for (const group of partitions) {
        const groupsByTransition = new Map();
  
        for (const state of group) {
          const key = automaton.Σ.map((symbol) =>
            partitions.findIndex((p) =>
              p.has(
                automaton.δ.find((t) => t.state_from === state && t.input === symbol)?.state_to || ""
              )
            )
          ).join(",");
  
          if (!groupsByTransition.has(key)) {
            groupsByTransition.set(key, new Set());
          }
          groupsByTransition.get(key).add(state);
        }
  
        newPartitions.push(...groupsByTransition.values());
        if (groupsByTransition.size > 1) {
          refined = true;
        }
      }
  
      partitions.length = 0;
      partitions.push(...newPartitions);
    }
  
    return partitions.length === automaton.Q.length;
  }
  
  // Reducir el autómata a su forma mínima equivalente
  function minimizeAutomaton(automaton) {
    automaton = removeUnreachableStates(automaton);
  
    if (isAutomatonMinimal(automaton)) {
      alert("El autómata ya está en su forma mínima.");
      return automaton;
    }
  
    let partitions = [new Set(automaton.F), new Set(automaton.Q.filter((s) => !automaton.F.includes(s)))];
    let refined = true;
  
    while (refined) {
      refined = false;
      const newPartitions = [];
  
      for (const group of partitions) {
        const groupsByTransition = new Map();
  
        for (const state of group) {
          const key = automaton.Σ.map((symbol) =>
            partitions.findIndex((p) =>
              p.has(
                automaton.δ.find((t) => t.state_from === state && t.input === symbol)?.state_to || ""
              )
            )
          ).join(",");
  
          if (!groupsByTransition.has(key)) {
            groupsByTransition.set(key, new Set());
          }
          groupsByTransition.get(key).add(state);
        }
  
        newPartitions.push(...groupsByTransition.values());
        if (groupsByTransition.size > 1) {
          refined = true;
        }
      }
  
      partitions = newPartitions;
    }
  
    // Crear el nuevo autómata reducido
    const reducedStates = partitions.map((p) => Array.from(p).join(","));
    const reducedTransitions = automaton.δ.map((t) => ({
      state_from: reducedStates.find((s) => s.split(",").includes(t.state_from)),
      input: t.input,
      state_to: reducedStates.find((s) => s.split(",").includes(t.state_to)),
    }));
  
    const reducedFinalStates = partitions
      .filter((p) => Array.from(p).some((state) => automaton.F.includes(state)))
      .map((p) => Array.from(p).join(","));
  
    const reducedInitialState = reducedStates.find((s) => s.split(",").includes(automaton.q0));
  
    return {
      Q: reducedStates,
      Σ: automaton.Σ,
      q0: reducedInitialState,
      F: reducedFinalStates,
      δ: reducedTransitions,
    };
  }
  
  // Pintar el autómata inicial
  function drawInitialAutomaton() {
    const automaton = getAutomatonData();
    if (automaton) {
      drawAutomaton("graph-initial", automaton);
    }
  }
  
  // Pintar el autómata reducido
  function drawReducedAutomaton() {
    const automaton = getAutomatonData();
    if (automaton) {
      const reducedAutomaton = minimizeAutomaton(automaton);
      drawAutomaton("graph-reduced", reducedAutomaton);
    }
  }
  