"use strict";
let addQueue = [];
let relationsList = [];




let $canvas = document.getElementById("grafica");

const nodes = new vis.DataSet();
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

$canvas.addEventListener("click",()=>{
  console.log(network.getSelectedEdges().length);

  if(network.getSelectedEdges().length > 0 ){
    document.getElementById("deleteRelationButton").disabled = false
  }
  else   document.getElementById("deleteRelationButton").disabled = true

})



function ActiveButton(action, value = true) {
  if (action == "edit")
    document.querySelector("button[action='edit']").disabled = !value;
  if (action == "delete")
    document.querySelector("button[action='delete']").disabled = !value;
  if (action == "addRelation")
    document.querySelector("button[action='addRelation']").disabled = !value;
  if (action == "deleteRelation")
    document.querySelector("button[action='deleteRelation']").disabled = !value;
}



function AddNode(idparam = undefined) {
  let $nodeNameInput = document.querySelector("input[name='node-name']");
  let $nodeInitialStateCheckbox = document.querySelector("input[name='addNodeFinalState']");
  let $nodeFinalStateCheckbox = document.querySelector("input[name='addNodeInitialState']");
  let id = idparam ?? $nodeNameInput.value;

  let color;
  
  if (!id) return alert("Agrega un valor al nombre");
  
  if($nodeInitialStateCheckbox.checked){
    let color = "#ffe633";
  }
  else if($nodeFinalStateCheckbox){
    let color = "#61ff33";
  }
  try {
    nodes.add({
      id,
      label: id.toString(),
      color: "#5FDABD",
      font: { color: "white" },
    });

    relationsList.forEach((item) => item.push(undefined));
    relationsList.push([]);
    for (let i = 0; i < relationsList.length; i++) {
      relationsList[relationsList.length - 1].push(undefined);
    }

    addQueue.push(id);
    ActiveButton("edit");
    ActiveButton("delete");
    ActiveButton("addRelation");
    UpdateSelects();
  } catch {
    alert("El nodo ya existe!");
    inputNodeName.value = "";
    return;
  }

  $nodeNameInput.value = "";
}

function EditNode() {
  const NodeId = document.getElementById("edit-select-node").value;
  const NewName = document.getElementById("editInputNodeName").value;
  

  let index = addQueue.indexOf(NodeId);

  let yArray = [...relationsList].splice(index, 1);

  let xArray = [];
  let copy = [...relationsList];

  for (let i = 0; i < copy.length; i++) {
    xArray.push(copy[i][index]);
  }

  relationsList.slice(index, 1);
  relationsList.push(...relationsList.splice(index, 1));
  relationsList.forEach((item, i) => {
    item.push(...item.splice(index, 1));
  });
 
  addQueue.splice(index,1)
  addQueue.push(NewName)

  nodes.remove(NodeId)
  AddNode(NewName)
  DrawRelations()
  
  
}

function DeleteNode(id = undefined) {
  let NodeId = id ?? document.getElementById("deleteSelectNodes").value
  
  let indexInQueue = addQueue.indexOf(NodeId);
  relationsList.splice(indexInQueue, 1);

  relationsList.forEach((arr) => arr.splice(indexInQueue, 1));
  nodes.remove(NodeId)
  addQueue = addQueue.filter( item => item != NodeId);

  if(addQueue.length === 0){
    ActiveButton("edit", false)
    ActiveButton("addRelation", false)
    ActiveButton("delete", false)
    showDeleteNodeModal()
  }

  DrawRelations();
  UpdateSelects();
}


function AddRelation() {
  let from = document.getElementById("from-relation").value;
  let to = document.getElementById("to-relation").value;
  let value = document.getElementById("adding-relation-name").value;

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



// [add, edit, delete, addRelation,delRelation]
let visible = [0, 0, 0, 0, 0 ];
let actionsbuttons = document.querySelector(".actions").children;

function showAddNodeModal() {
  let actions = document.querySelector(".modals").children;
  //visible
  if (visible[0]) {
    actions[0].classList.add("hidden");
    visible = [0, 0, 0, 0 ];
    return;
  }
  actions[0].classList.remove("hidden");
  actions[1].classList.add("hidden");
  actions[2].classList.add("hidden");
  actions[3].classList.add("hidden");
  visible = [1, 0, 0, 0];
}
function showEditNodeModal() {
  let actions = document.querySelector(".modals").children;
  //visible
  if (visible[1]) {
    actions[1].classList.add("hidden");
    visible = [0, 0, 0, 0];
    return;
  }
  actions[0].classList.add("hidden");
  actions[1].classList.remove("hidden");
  actions[2].classList.add("hidden");
  actions[3].classList.add("hidden");
  visible = [0, 1, 0 , 0];
}

function showDeleteNodeModal() {
  let actions = document.querySelector(".modals").children;
  //visible
  if (visible[2]) {
    visible = [0, 0, 0,0];
    actions[2].classList.add("hidden");
    return;
  }
  actions[0].classList.add("hidden");
  actions[1].classList.add("hidden");
  actions[2].classList.remove("hidden");
  actions[3].classList.add("hidden");
  visible = [0, 0, 1, 0];
}


function showAddRelationModal(){
  let actions = document.querySelector(".modals").children;
  //visible
  if (visible[3]) {
    visible = [0, 0, 0, 0];
    actions[3].classList.add("hidden");
    return;
  }
  actions[0].classList.add("hidden");
  actions[1].classList.add("hidden");
  actions[2].classList.add("hidden");
  actions[3].classList.remove("hidden");
  visible = [0, 0, 0 , 1];
}