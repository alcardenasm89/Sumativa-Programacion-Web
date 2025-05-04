// Variables globales
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
    actualizarContenidoCarrito();
}

function cerrarCarrito() {
    carritoModal.style.display = 'none';
}

function guardarCarrito() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

// Agregar un juego al carrito
function agregarAlCarrito(id, titulo, precio, imagen) {
    // Buscar si el juego ya existe en el carrito
    const itemExistente = carrito.find(item => item.id === id);
    
    if (itemExistente) {
        // Si el juego existe, incrementar la cantidad
        itemExistente.cantidad += 1;
    } else {
        // Si el juego no existe, agregarlo al carrito
        carrito.push({
            id: id,
            titulo: titulo,
            precio: precio,
            imagen: imagen,
            cantidad: 1
        });
    }
    
    // Guardar el carrito actualizado
    guardarCarrito();
    
    // Actualizar el contador del carrito
    actualizarContadorCarrito();
    
    // Mostrar mensaje de éxito
    alert('¡Producto agregado al carrito!');
    
    // Actualizar el contenido del carrito si está abierto
    if (carritoModal && carritoModal.style.display === 'block') {
        actualizarContenidoCarrito();
    }
}

// Actualizar el contador del carrito
function actualizarContadorCarrito() {
    if (contadorCarrito) {
        const totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);
        contadorCarrito.textContent = totalItems;
    }
}

// Actualizar el contenido del carrito
function actualizarContenidoCarrito() {
    if (!carritoItems) return;

    // Limpiar el contenido actual
    carritoItems.innerHTML = '';
    
    // Calcular totales
    let subtotal = 0;
    
    // Agregar cada item al carrito
    carrito.forEach((item, idx) => {
        const itemElement = document.createElement('div');
        itemElement.className = 'carrito-item';
        itemElement.innerHTML = `
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
        carritoItems.appendChild(itemElement);
        
        subtotal += item.precio * item.cantidad;
    });
    
    // Calcular el IVA (19% del subtotal)
    const iva = Math.round(subtotal * 0.19);
    
    // Actualizar los totales
    if (subtotalSpan) subtotalSpan.textContent = `CLP$ ${subtotal.toLocaleString()}`;
    if (ivaSpan) ivaSpan.textContent = `CLP$ ${iva.toLocaleString()}`;
    if (totalSpan) totalSpan.textContent = `CLP$ ${(subtotal + iva).toLocaleString()}`;
}

// Cambiar la cantidad de un item
function cambiarCantidad(idx, delta) {
    carrito[idx].cantidad += delta;
    if (carrito[idx].cantidad <= 0) {
        carrito.splice(idx, 1);
    }
    guardarCarrito();
    actualizarContenidoCarrito();
    actualizarContadorCarrito();
}

// Eliminar un item del carrito
function eliminarDelCarrito(idx) {
    carrito.splice(idx, 1);
    guardarCarrito();
    actualizarContenidoCarrito();
    actualizarContadorCarrito();
}

// Proceder al pago
function procederPago() {
    alert('¡Gracias por tu compra! (Simulación)');
    carrito = [];
    guardarCarrito();
    actualizarContenidoCarrito();
    actualizarContadorCarrito();
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
    actualizarContadorCarrito();

    // Delegación de eventos para todos los botones de agregar al carrito
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('agregar-carrito-btn')) {
            const btn = e.target;
            const id = btn.getAttribute('data-id');
            const titulo = btn.getAttribute('data-titulo');
            const precio = parseInt(btn.getAttribute('data-precio'));
            const imagen = btn.getAttribute('data-imagen');
            agregarAlCarrito(id, titulo, precio, imagen);
        }
    });
});

window.agregarAlCarrito = agregarAlCarrito;
window.cambiarCantidad = cambiarCantidad;
window.eliminarDelCarrito = eliminarDelCarrito;
window.cerrarCarrito = cerrarCarrito;
window.procederPago = procederPago; 