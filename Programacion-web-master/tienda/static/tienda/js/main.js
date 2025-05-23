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

function agregarAlCarrito(id, titulo, precio) {
    const item = {
        id: id,
        titulo: titulo,
        precio: precio,
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
            <div class="carrito-item-info">
                <div class="carrito-item-titulo">${item.titulo}</div>
                <div class="carrito-item-precio">CLP$ ${item.precio.toLocaleString()}</div>
                <div class="carrito-item-cantidad" style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
                    <button class="carrito-cantidad-btn" onclick="cambiarCantidad(${idx}, -1)" style="background: #00ffb3; color: #1a2236; border: none; border-radius: 5px; width: 30px; height: 30px; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center;">-</button>
                    <span style="color: #fff; font-size: 1.1rem; min-width: 30px; text-align: center;">${item.cantidad}</span>
                    <button class="carrito-cantidad-btn" onclick="cambiarCantidad(${idx}, 1)" style="background: #00ffb3; color: #1a2236; border: none; border-radius: 5px; width: 30px; height: 30px; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center;">+</button>
                    <button class="carrito-item-eliminar" onclick="eliminarDelCarrito(${idx})" style="background: #ff4757; color: white; border: none; border-radius: 5px; width: 30px; height: 30px; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: 0.5rem;">×</button>
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

function vaciarCarrito() {
    if (confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
        carrito = [];
        guardarCarrito();
        actualizarCarrito();
        cerrarCarrito();
    }
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

    // Delegación de eventos para todos los botones de agregar al carrito
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('agregar-carrito-btn')) {
            const btn = e.target;
            const id = btn.getAttribute('data-id');
            const titulo = btn.getAttribute('data-titulo');
            const precio = parseInt(btn.getAttribute('data-precio'));
            agregarAlCarrito(id, titulo, precio);
        }
    });

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