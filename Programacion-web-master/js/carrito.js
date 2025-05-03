// Inicializar el carrito en localStorage si no existe
function inicializarCarrito() {
    if (!localStorage.getItem('carrito')) {
        localStorage.setItem('carrito', JSON.stringify([]));
    }
}

// Obtener el carrito actual
function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || [];
}

// Agregar un juego al carrito
function agregarAlCarrito(id, nombre, precio, imagen) {
    // Inicializar el carrito si no existe
    inicializarCarrito();
    
    // Obtener el carrito actual
    let carrito = obtenerCarrito();
    
    // Buscar si el juego ya existe en el carrito
    let juegoExistente = carrito.find(item => item.id === id);
    
    if (juegoExistente) {
        // Si el juego existe, incrementar la cantidad
        juegoExistente.cantidad += 1;
    } else {
        // Si el juego no existe, agregarlo al carrito
        carrito.push({
            id: id,
            nombre: nombre,
            precio: precio,
            imagen: imagen,
            cantidad: 1
        });
    }
    
    // Guardar el carrito actualizado en localStorage
    localStorage.setItem('carrito', JSON.stringify(carrito));
    
    // Actualizar el contador del carrito
    actualizarContadorCarrito();
    
    // Mostrar mensaje de éxito
    mostrarMensajeExito();
    
    // Actualizar el contenido del carrito si está abierto
    const modal = document.getElementById('carritoModal');
    if (modal && modal.classList.contains('activo')) {
        actualizarContenidoCarrito();
    }
}

// Actualizar el contador del carrito
function actualizarContadorCarrito() {
    let carrito = obtenerCarrito();
    let totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);
    
    const contador = document.getElementById('contador-carrito');
    if (contador) {
        if (totalItems > 0) {
            contador.textContent = totalItems;
            contador.classList.add('visible');
        } else {
            contador.classList.remove('visible');
        }
    }
}

// Mostrar mensaje de éxito
function mostrarMensajeExito() {
    
    // Crear el elemento del mensaje
    const mensaje = document.createElement('div');
    mensaje.className = 'mensaje-exito';
    mensaje.textContent = '¡Juego agregado al carrito!';
    
    // Agregar el mensaje al body
    document.body.appendChild(mensaje);
    
    // Remover el mensaje después de 3 segundos
    setTimeout(() => {
        mensaje.remove();
    }, 3000);
}

// Abrir el modal del carrito
function abrirCarrito() {
    const modal = document.getElementById('carritoModal');
    if (modal) {
        modal.classList.add('activo');
        actualizarContenidoCarrito();
    }
}

// Cerrar el modal del carrito
function cerrarCarrito() {
    const modal = document.getElementById('carritoModal');
    if (modal) {
        modal.classList.remove('activo');
    }
}

// Actualizar el contenido del carrito
function actualizarContenidoCarrito() {
    const carritoItems = document.getElementById('carritoItems');
    if (!carritoItems) return;

    const carrito = obtenerCarrito();
    
    // Limpiar el contenido actual
    carritoItems.innerHTML = '';
    
    // Calcular totales
    let subtotal = 0;
    
    // Agregar cada item al carrito
    carrito.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'carrito-item';
        itemElement.innerHTML = `
            <img src="${item.imagen}" alt="${item.nombre}">
            <div class="item-details">
                <h3>${item.nombre}</h3>
                <p class="item-price">CLP$ ${item.precio.toLocaleString()}</p>
                <div class="cantidad-controls">
                    <button onclick="actualizarCantidad('${item.id}', ${item.cantidad - 1})">-</button>
                    <span>${item.cantidad}</span>
                    <button onclick="actualizarCantidad('${item.id}', ${item.cantidad + 1})">+</button>
                </div>
            </div>
        `;
        carritoItems.appendChild(itemElement);
        
        // El precio mostrado en la página incluye el IVA
        const precioConIVA = item.precio;
        // Calcular el subtotal (precio sin IVA)
        const precioSinIVA = Math.round(precioConIVA / 1.19);
        subtotal += precioSinIVA * item.cantidad;
    });
    
    // Calcular el IVA (19% del subtotal)
    const iva = Math.round(subtotal * 0.19);
    
    // Actualizar los totales con formato de moneda chilena
    const subtotalElement = document.getElementById('subtotal');
    const ivaElement = document.getElementById('iva');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) subtotalElement.textContent = `CLP$ ${subtotal.toLocaleString('es-CL')}`;
    if (ivaElement) ivaElement.textContent = `CLP$ ${iva.toLocaleString('es-CL')}`;
    if (totalElement) totalElement.textContent = `CLP$ ${(subtotal + iva).toLocaleString('es-CL')}`;
}

// Actualizar la cantidad de un item
function actualizarCantidad(id, nuevaCantidad) {
    if (nuevaCantidad < 1) {
        eliminarDelCarrito(id);
    } else {
        let carrito = obtenerCarrito();
        let item = carrito.find(item => item.id === id);
        if (item) {
            item.cantidad = nuevaCantidad;
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarContadorCarrito();
            actualizarContenidoCarrito();
        }
    }
}

// Eliminar un item del carrito
function eliminarDelCarrito(id) {
    let carrito = obtenerCarrito();
    carrito = carrito.filter(item => item.id !== id);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarContadorCarrito();
    actualizarContenidoCarrito();
}

// Proceder al pago
function procederPago() {
    window.location.href = 'pago.html';
}

// Inicializar el contador del carrito cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    actualizarContadorCarrito();
    
    // Agregar evento para abrir el carrito
    const carritoBtn = document.getElementById('carritoBtn');
    if (carritoBtn) {
        carritoBtn.addEventListener('click', (e) => {
            e.preventDefault();
            abrirCarrito();
        });
    }
}); 