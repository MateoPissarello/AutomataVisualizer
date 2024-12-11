// Selección de elementos del DOM
const lenguajeForm = document.getElementById("lenguaje-form");
const lenguajeInput = document.getElementById("lenguaje");
const resultadoDiv = document.getElementById("resultado-maquina-turing");
const descripcionMaquina = document.getElementById("descripcion-maquina");
const cintaDiv = document.getElementById("cinta");
const simularBtn = document.getElementById("simular");
const pasosDiv = document.getElementById("pasos-simulacion");
const entradaCadenaDiv = document.getElementById("entrada-cadena");
const cadenaInput = document.getElementById("cadena-input");
const tablaCinta = document.getElementById("tabla-cinta");
const cuerpoCinta = document.createElement("tbody");

// Objeto para almacenar la máquina de Turing
let maquinaTuring = {};
let cinta = [];
let posicionCabezal = 0;

// Escucha el evento de envío del formulario
lenguajeForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const lenguaje = lenguajeInput.value.trim();

    if (!lenguaje) {
        alert("Por favor, ingrese un lenguaje válido.");
        return;
    }

    // Crear la Máquina de Turing
    maquinaTuring = crearMaquinaTuring(lenguaje);

    // Mostrar información de la máquina
    descripcionMaquina.innerHTML = `
        Detalles de la Máquina:
        <br>Estados: ${maquinaTuring.estados.join(", ")}
        <br>Alfabeto de entrada: ${maquinaTuring.alfabetoEntrada.join(", ")}
        <br>Alfabeto de cinta: ${maquinaTuring.alfabetoCinta.join(", ")}
        <br>Estado inicial: ${maquinaTuring.estadoInicial}
        <br>Estado final: ${maquinaTuring.estadoFinal}
        <br>Transiciones:
        ${Object.entries(maquinaTuring.transiciones).map(
        ([key, value]) =>
            `<br>δ(${key}) = (${value.estado}, ${value.escribir}, ${value.mover})`
    ).join("")}
    `;
    resultadoDiv.classList.remove("hidden");
    entradaCadenaDiv.classList.remove("hidden");
    simularBtn.disabled = false;
});

// Función para crear la Máquina de Turing de forma dinámica
function crearMaquinaTuring(lenguaje) {
    const alfabetoEntrada = new Set();
    const alfabetoCinta = new Set(["_"]);
    const palabras = lenguaje.split(",").map(palabra => palabra.trim());
    const estados = [`q0`, `qf`]; // Estado inicial y estado final
    const transiciones = {};

    palabras.forEach((palabra) => {
        let estadoActual = "q0";  // Empezamos desde el estado inicial
        for (let i = 0; i < palabra.length; i++) {
            const simbolo = palabra[i];
            alfabetoEntrada.add(simbolo);
            alfabetoCinta.add(simbolo);
            const siguienteEstado = `q${i + 1}`;

            // Asegurarse de agregar el estado
            if (!estados.includes(siguienteEstado)) {
                estados.push(siguienteEstado);
            }

            // Generar transiciones dinámicas según la palabra
            transiciones[`${estadoActual},${simbolo}`] = {
                estado: siguienteEstado,
                escribir: simbolo,
                mover: "R"
            };
            estadoActual = siguienteEstado;
        }

        // Última transición: Si encontramos un "_", volvemos al estado final qf
        transiciones[`${estadoActual},_`] = {
            estado: "qf",
            escribir: "_",
            mover: "L"
        };
    });

    // Eliminar la transición de regreso al estado inicial desde qf
    // No se vuelve a q0 desde qf, ya que la cadena debe ser aceptada en qf
    transiciones["qf,_"] = { estado: "qf", escribir: "_", mover: "S" };

    return {
        estados,
        alfabetoEntrada: Array.from(alfabetoEntrada),
        alfabetoCinta: Array.from(alfabetoCinta),
        transiciones,
        estadoInicial: "q0",
        estadoFinal: "qf" // Ahora el estado final es qf
    };
}

// Función para validar que la cadena de entrada esté en el alfabeto de entrada
function validarEntrada(cadena, alfabetoEntrada) {
    const simbolosInvalidos = []; // Array para almacenar símbolos no válidos

    // Comprobar cada símbolo de la cadena
    for (let i = 0; i < cadena.length; i++) {
        if (!alfabetoEntrada.includes(cadena[i])) {
            simbolosInvalidos.push(cadena[i]);
        }
    }

    // Si se encontraron símbolos no válidos, mostrar el mensaje
    if (simbolosInvalidos.length > 0) {
        alert(`Los siguientes símbolos no pertenecen al lenguaje: ${simbolosInvalidos.join(", ")}`);
        return false; // Retorna falso si hay símbolos no válidos
    }

    return true; // Retorna verdadero si todos los símbolos son válidos
}

// Escucha el evento de simulación
simularBtn.addEventListener("click", () => {
    const cadena = cadenaInput.value.trim();
    if (!cadena) {
        alert("Por favor, ingrese una cadena para simular.");
        return;
    }

    // Validar que todos los símbolos de la cadena están en el alfabeto de entrada
    const esValida = validarEntrada(cadena, maquinaTuring.alfabetoEntrada);
    if (!esValida) {
        return; // Si la cadena no es válida, no se simula
    }

    // Inicializar la cinta correctamente
    cinta = cadena.split("");
    cinta.push("_"); // Agregar un espacio en blanco al final
    posicionCabezal = 0;

    // Renderizar la tabla inicial
    renderizarTabla();

    // Ejecutar la simulación
    const pasos = simularMaquinaTuring();
    pasosDiv.textContent = pasos.join("\n");
});


// Función para simular la máquina de Turing con un lenguaje dinámico
function simularMaquinaTuring() {
    let estadoActual = maquinaTuring.estadoInicial;
    const pasos = [];
    let maxPasos = 100; // Límite máximo de pasos para evitar ciclos infinitos
    let contadorPasos = 0;

    while (estadoActual !== maquinaTuring.estadoFinal) {
        const simboloActual = cinta[posicionCabezal];
        const transicion = maquinaTuring.transiciones[`${estadoActual},${simboloActual}`];

        if (!transicion) {
            pasos.push(`Error: No se encontró una transición válida desde (${estadoActual}, ${simboloActual}).`);
            break;
        }

        // Aplicar la transición
        cinta[posicionCabezal] = transicion.escribir;
        estadoActual = transicion.estado;
        pasos.push(renderCinta(posicionCabezal, estadoActual));

        // Mover el cabezal
        if (transicion.mover === "R") {
            posicionCabezal++;
            if (posicionCabezal >= cinta.length) cinta.push("_");
        } else if (transicion.mover === "L") {
            posicionCabezal = Math.max(0, posicionCabezal - 1);
        }

        // Renderizar el estado actual de la tabla
        renderizarTabla();

        contadorPasos++;
        if (contadorPasos >= maxPasos) {
            pasos.push("Error: Se alcanzó el límite máximo de pasos. Posible ciclo infinito.");
            break;
        }
    }

    pasos.push(renderCinta(posicionCabezal, estadoActual));
    pasos.push(
        estadoActual === maquinaTuring.estadoFinal
            ? "La cadena es aceptada por la Máquina de Turing."
            : "La cadena no es aceptada por la Máquina de Turing."
    );

    return pasos;
}

// Función para renderizar el estado de la cinta en la tabla
function renderizarTabla() {
    // Limpiar la tabla antes de renderizar
    cuerpoCinta.innerHTML = "";

    // Crear la fila de símbolos en la cinta
    const filaSimbolos = document.createElement("tr");
    for (let i = 0; i < cinta.length; i++) {
        const celda = document.createElement("td");
        celda.textContent = cinta[i];
        if (i === posicionCabezal) {
            celda.classList.add("cabezal");
        }
        filaSimbolos.appendChild(celda);
    }
    cuerpoCinta.appendChild(filaSimbolos);
}

// Función para renderizar el estado de la cinta
function renderCinta(cabezal, estado) {
    return cinta
        .map((simbolo, index) => (index === cabezal ? `[${simbolo}]` : simbolo))
        .join(" ") + `  Estado actual: ${estado}`;
}
