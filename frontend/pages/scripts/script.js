"use strict";
let addQueue = [];
let relationsList = [];

let transitions = {};


let $canvas = document.getElementById("grafica");

const nodes = new vis.DataSet();
const states = [];

const edges = new vis.DataSet();
const data = { nodes, edges };
const options = {
  autoResize: true,
  nodes:{
    shape:"circle",
  },
  interaction: { selectable: true },
  edges: {
    arrows: {
      to: {
        enabled: true,
      },
    },
  },
};

const network = new vis.Network($canvas, data, options);
network.setOptions(options);

// Prevent default
document.querySelectorAll("form button").forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
  });
});



function AddNode(idparam = undefined) {
  let $nodeNameInput = document.querySelector("input[name='node-name']");
  let $nodeInitialStateCheckbox = document.querySelector("input[name='addNodeFinalState']");
  let $nodeFinalStateCheckbox = document.querySelector("input[name='addNodeInitialState']");
  let id = idparam ?? $nodeNameInput.value;

  if(states.indexOf(id) == -1){
    states.push(id)
  }

  let color = "#cccccc";
  
  if (!id) return alert("Agrega un valor al nombre");
  
  if($nodeInitialStateCheckbox.checked){
    color = "#ffe633";
  }
  if($nodeFinalStateCheckbox.checked){
    color = "#61ff33";
  }

  try {
    nodes.add({
      id,
      label: id.toString(),
      color: color,
      font: { color: "white" },
    });

    relationsList.forEach((item) => item.push(undefined));
    relationsList.push([]);
    for (let i = 0; i < relationsList.length; i++) {
      relationsList[relationsList.length - 1].push(undefined);
    }

    addQueue.push(id);
    UpdateSelects();
  } catch {
    alert("El nodo ya existe!");
    inputNodeName.value = "";
    return;
  }

  $nodeNameInput.value = "";
}



function AddRelation(from, to, value) {

  if (!value) return alert("Por favor ingresa un valor valido en valor");
  //alt 789 -> "§"
  edges.add({ from, to, label: value , id:`${from}§${to}`});

  let indexInQueueFrom = addQueue.indexOf(from);
  let indexInQueueto = addQueue.indexOf(to);

  relationsList[indexInQueueFrom][indexInQueueto] = value;
}

function DeleteRelation(){

  const SelectedEdges = network.getSelectedEdges()
  
  if(SelectedEdges.length < 0 ) return document.getElementById("deleteRelationButton").disabled = true
  const  [from, to] = SelectedEdges[0].split("§")

  let fromIndex = addQueue.indexOf(from)
  let toIndex = addQueue.indexOf(to)

  relationsList[fromIndex][toIndex] = undefined

  network.deleteSelected()

}

function DrawRelations() {
  edges.clear();
  for (let y in relationsList) {
    for (let x in relationsList[y]) {
      if (!relationsList[x][y]) continue;

      edges.add({
        from: addQueue[x],
        to: addQueue[y],
        label: relationsList[x][y],
      });
    }
  }
}


function UpdateSelects() {
  let dataSet = nodes.getDataSet().getIds();
  let $selects = document.querySelectorAll("select[data='nodes']");

  $selects.forEach(($select) => {
    $select.innerHTML = "";
    for (let data of dataSet) {
      $select.innerHTML += `<option value="${data}">Nodo ${data}</option>`;
    }
  });
}





function parseTransitions() {
  // Obtener el contenido del textarea
  const text = document.getElementById("transicionesTextArea").value;

  // Crear un objeto para almacenar las transiciones
  transitions = {};

  // Usar una expresión regular para encontrar todas las transiciones
  const regex = /\(\s*([a-zA-Z]+\d+)\s*,\s*([a-zA-Z])\s*\)\s*->\s*(q\d+)/g;
  let match;

  // Iterar sobre todas las coincidencias
  while ((match = regex.exec(text)) !== null) {
    const fromState = match[1];  // Estado de origen (q0, q1, q2, ...)
    if( states.indexOf(fromState) == -1 ){
      alert("El estado " +  fromState + " no ha sido creado aun")
      continue
    }
    const char = match[2];       // Carácter (a, b, c, ...)
    const toState = match[3];    // Estado de destino (q1, q2, q3, ...)

    // Asegurarse de que el estado de origen exista en el objeto
    if (!transitions[fromState]) {
      transitions[fromState] = [];
    }

    AddRelation(fromState, toState, char)
    // Agregar la transición al estado de origen
    transitions[fromState].push({
      char: char,
      to: toState
    });
  }

}





