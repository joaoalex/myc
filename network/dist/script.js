const nodeFilterSelector = document.getElementById("nodeFilterSelect");
const edgeFilters = document.getElementsByName("edgesFilter");

function startNetwork(data) {
  const container = document.getElementById("mynetwork");
  const options = {};
  const network = new vis.Network(container, data, options);
  
  network.on('drequipand', (e) => {
    if (e.nodes && e.nodes.length) {
      network.storePositions()
    }
  })
}

/**
 * In this example we do not mutate nodes or edges source data.
 */
const nodes = new vis.DataSet([
  { id: 1, label: "Projeto A", equipa: "SGOA", tribo: "CENTRAL" },
  { id: 2, label: "Projeto B", equipa: "POUPANCAS", tribo: "CANAIS" },
  { id: 3, label: "Iniciativa X", equipa: "DAILY B", tribo: "CANAIS" },
  { id: 4, label: "Solução Segurança", equipa: "PSI", tribo: "DSI" },
  { id: 5, label: "Pedido B", equipa: "OFERTA", tribo: "DMPN" },
  { id: 6, label: "Desenvolvimento C", equipa: "SGOA", tribo: "CENTRAL" },
  { id: 7, label: "Desenvolvimento DD", equipa: "CREDITO", tribo: "CANAIS" },
  { id: 8, label: "Pedido F", equipa: "CLIENTES", tribo: "DSI" },
  
]);

const edges = new vis.DataSet([
  {
    from: 1,
    to: 2,
    relation: "interessado",
    arrows: "to, from",
    color: { color: "red" },
  },
  {
    from: 1,
    to: 3,
    relation: "interessado",
    arrows: "to, from",
    color: { color: "red" },
  },
  {
    from: 2,
    to: 3,
    relation: "interessado",
    arrows: "to, from",
    color: { color: "red" },
  },
  {
    from: 2,
    to: 5,
    relation: "dependente",
    arrows: "to",
    color: { color: "green" },
  },
  {
    from: 4,
    to: 1,
    relation: "parte",
    arrows: "to",
    color: { color: "blue" },
  },
  {
    from: 4,
    to: 2,
    relation: "parte",
    arrows: "to",
    color: { color: "blue" },
  },
  {
    from: 4,
    to: 3,
    relation: "parte",
    arrows: "to",
    color: { color: "blue" },
  },
  {
    from: 6,
    to: 2,
    relation: "dependente",
    arrows: "to",
    color: { color: "green" },
  },
  {
	from: 8,
    to: 6,
    relation: "dependente",
    arrows: "to",
    color: { color: "green" },
  },
  {
	from: 7,
    to: 1,
    relation: "dependente",
    arrows: "to",
    color: { color: "green" },
  }
]);

/**
 * filter values are updated in the outer scope.
 * in order to apply filters to new values, DataView.refresh() should be called
 */
let nodeFilterValue = "";
const edgesFilterValues = {
  interessado: true,
  parte: true,
  dependente: true,
};

/*
      filter function should return true or false
      based on whether item in DataView satisfies a given condition.
    */
const nodesFilter = (node) => {
  if (nodeFilterValue === "") {
    return true;
  }
  switch (nodeFilterValue) {
    case "CANAIS":
      return node.tribo === "CANAIS";
	case "DSI":
      return node.tribo === "DSI";
	case "CENTRAL":
      return node.tribo === "CENTRAL";
	case "DMPN":
      return node.tribo === "DMPN";
    case "SGOA":
      return node.equipa === "SGOA";
	case "CLIENTES":
      return node.equipa === "CLIENTES";

	case "PSI":
      return node.equipa === "PSI";

    default:
      return true;
  }
};

const edgesFilter = (edge) => {
  return edgesFilterValues[edge.relation];
};

const nodesView = new vis.DataView(nodes, { filter: nodesFilter });
const edgesView = new vis.DataView(edges, { filter: edgesFilter });

nodeFilterSelector.addEventListener("change", (e) => {
  // set new value to filter variable
  nodeFilterValue = e.target.value;
  /*
        refresh DataView,
        so that its filter function is re-calculated with the new variable
      */
  nodesView.refresh();
});

edgeFilters.forEach((filter) =>
  filter.addEventListener("change", (e) => {
    const { value, checked } = e.target;
    edgesFilterValues[value] = checked;
    edgesView.refresh();
  })
);

startNetwork({ nodes: nodesView, edges: edgesView });