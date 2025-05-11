// Funcionalidad del carrito
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
const carritoBtn = document.getElementById('carritoBtn');
const carritoModal = document.getElementById('carritoModal');
const carritoItems = document.getElementById('carritoItems');
const contadorCarrito = document.getElementById('contador-carrito');
const subtotalSpan = document.getElementById('subtotal');
const ivaSpan = document.getElementById('iva');
const totalSpan = document.getElementById('total');

// Funciones del carrito
function abrirCarrito() {
    carritoModal.style.display = 'block';
    actualizarCarrito();
}

function cerrarCarrito() {
    carritoModal.style.display = 'none';
}

function guardarCarrito() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function agregarAlCarrito(id, titulo, precio, imagen) {
    const item = {
        id: id,
        titulo: titulo,
        precio: precio,
        imagen: imagen,
        cantidad: 1
    };
    
    // Verificar si el item ya existe en el carrito
    const itemExistente = carrito.find(i => i.id === id);
    if (itemExistente) {
        itemExistente.cantidad += 1;
    } else {
        carrito.push(item);
    }
    
    guardarCarrito();
    actualizarCarrito();
    
    // Mostrar mensaje de éxito
    alert('¡Producto agregado al carrito!');
}

function actualizarCarrito() {
    if (!carritoItems) return;

    // Limpiar el contenido actual
    carritoItems.innerHTML = '';
    
    // Calcular totales
    let subtotal = 0;
    let totalCantidad = 0;
    
    // Agregar cada item al carrito
    carrito.forEach((item, idx) => {
        subtotal += item.precio * item.cantidad;
        totalCantidad += item.cantidad;
        
        const div = document.createElement('div');
        div.className = 'carrito-item';
        div.innerHTML = `
            <img src="${item.imagen}" class="carrito-item-img" alt="${item.titulo}">
            <div class="carrito-item-info">
                <div class="carrito-item-titulo">${item.titulo}</div>
                <div class="carrito-item-precio">CLP$ ${item.precio.toLocaleString()}</div>
                <div class="carrito-item-cantidad">
                    <button class="carrito-cantidad-btn" onclick="cambiarCantidad(${idx}, -1)">-</button>
                    <span>${item.cantidad}</span>
                    <button class="carrito-cantidad-btn" onclick="cambiarCantidad(${idx}, 1)">+</button>
                    <button class="carrito-item-eliminar" onclick="eliminarDelCarrito(${idx})">&times;</button>
                </div>
            </div>
        `;
        carritoItems.appendChild(div);
    });
    
    // Actualizar contador y totales
    if (contadorCarrito) contadorCarrito.textContent = totalCantidad;
    if (subtotalSpan) subtotalSpan.textContent = 'CLP$ ' + subtotal.toLocaleString();
    const iva = Math.round(subtotal * 0.19);
    if (ivaSpan) ivaSpan.textContent = 'CLP$ ' + iva.toLocaleString();
    if (totalSpan) totalSpan.textContent = 'CLP$ ' + (subtotal + iva).toLocaleString();
}

function cambiarCantidad(idx, delta) {
    carrito[idx].cantidad += delta;
    if (carrito[idx].cantidad <= 0) {
        carrito.splice(idx, 1);
    }
    guardarCarrito();
    actualizarCarrito();
}

function eliminarDelCarrito(idx) {
    carrito.splice(idx, 1);
    guardarCarrito();
    actualizarCarrito();
}

function procederPago() {
    alert('¡Gracias por tu compra! (Simulación)');
    carrito = [];
    guardarCarrito();
    actualizarCarrito();
    cerrarCarrito();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    if (carritoBtn) {
        carritoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            abrirCarrito();
        });
    }
    actualizarCarrito();

    // Event Listeners para búsqueda
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', buscarJuegos);
    }
});

// Funcionalidad de búsqueda
function buscarJuegos() {
    const input = document.getElementById('searchInput');
    const termino = input.value.toLowerCase();
    const juegos = document.querySelectorAll('.juego-card');
    
    juegos.forEach(juego => {
        const titulo = juego.querySelector('h3').textContent.toLowerCase();
        if (titulo.includes(termino)) {
            juego.style.display = 'block';
        } else {
            juego.style.display = 'none';
        }
    });
} 