document.addEventListener('DOMContentLoaded', () => {
    cargarResumenCarrito();
    configurarFormularioPago();
});

// Función para mostrar números en formato de pesos chilenos
function formatearPrecio(precio) {
    return precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function cargarResumenCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const cartSummaryElement = document.getElementById('cartSummary');
    const totalAmountElement = document.getElementById('totalAmount');
    let total = 0;

    cartSummaryElement.innerHTML = '';

    carrito.forEach(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;

        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <img src="${item.imagen}" alt="${item.nombre}">
            <div class="cart-item-details">
                <h3>${item.nombre}</h3>
                <p>Cantidad: ${item.cantidad}</p>
                <p>Precio unitario: $${formatearPrecio(item.precio)}</p>
                <p>Subtotal: $${formatearPrecio(subtotal)}</p>
            </div>
        `;

        cartSummaryElement.appendChild(itemElement);
    });

    totalAmountElement.textContent = `Total a pagar: $${formatearPrecio(total)}`;
}

// Función para crear y manejar mensajes de error
function crearMensajeError(input, mensaje) {
    let errorDiv = input.parentNode.querySelector('.error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        input.parentNode.appendChild(errorDiv);
    }
    return errorDiv;
}

function configurarFormularioPago() {
    const form = document.getElementById('paymentForm');
    
    // Validación tipo de tarjeta
    const cardTypeSelect = document.getElementById('cardType');
    const cardTypeError = crearMensajeError(cardTypeSelect);
    
    cardTypeSelect.addEventListener('change', () => {
        if (cardTypeSelect.value) {
            cardTypeError.textContent = '';
        }
    });

    // Validación nombre en la tarjeta
    const cardNameInput = document.getElementById('cardName');
    const cardNameError = crearMensajeError(cardNameInput);
    
    cardNameInput.addEventListener('input', () => {
        if (cardNameInput.value.trim()) {
            cardNameError.textContent = '';
        }
    });

    // Formato y validación número de tarjeta
    const cardNumberInput = document.getElementById('cardNumber');
    const cardNumberError = crearMensajeError(cardNumberInput);

    cardNumberInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        value = value.slice(0, 16);
        
        let formattedValue = '';
        for (let i = 0; i < value.length; i++) {
            if (i > 0 && i % 4 === 0) {
                formattedValue += ' ';
            }
            formattedValue += value[i];
        }
        
        e.target.value = formattedValue;

        if (value.length > 0 && value.length < 16) {
            cardNumberError.textContent = 'El número de tarjeta debe tener 16 dígitos';
        } else {
            cardNumberError.textContent = '';
        }
    });

    // Formato y validación fecha de vencimiento
    const expiryDateInput = document.getElementById('expiryDate');
    const expiryError = crearMensajeError(expiryDateInput);

    expiryDateInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.slice(0, 2) + '/' + value.slice(2, 4);
        }
        e.target.value = value;

        if (value.length === 5) {
            const [month, year] = value.split('/');
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear() % 100;
            const currentMonth = currentDate.getMonth() + 1;
            const maxYear = (currentDate.getFullYear() + 10) % 100;

            const inputMonth = parseInt(month);
            const inputYear = parseInt(year);

            if (inputMonth < 1 || inputMonth > 12) {
                expiryError.textContent = 'Mes inválido';
            } else if (inputYear < currentYear || (inputYear === currentYear && inputMonth < currentMonth)) {
                expiryError.textContent = 'La tarjeta está vencida';
            } else if (inputYear > maxYear) {
                expiryError.textContent = 'La fecha no puede exceder 10 años';
            } else {
                expiryError.textContent = '';
            }
        }
    });

    // Formato y validación CVV
    const cvvInput = document.getElementById('cvv');
    const cvvError = crearMensajeError(cvvInput);

    cvvInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '').slice(0, 3);
        e.target.value = value;
        
        if (value.length > 0 && value.length < 3) {
            cvvError.textContent = 'El CVV debe tener 3 dígitos';
        } else {
            cvvError.textContent = '';
        }
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let hasErrors = false;

        // Validar tipo de tarjeta
        if (!cardTypeSelect.value) {
            cardTypeError.textContent = 'Por favor seleccione un tipo de tarjeta';
            hasErrors = true;
        }

        // Validar nombre en la tarjeta
        if (!cardNameInput.value.trim()) {
            cardNameError.textContent = 'Por favor ingrese el nombre en la tarjeta';
            hasErrors = true;
        }

        // Validar número de tarjeta
        const cardNumber = cardNumberInput.value.replace(/\s/g, '');
        if (cardNumber.length !== 16) {
            cardNumberError.textContent = 'Por favor ingrese un número de tarjeta';
            hasErrors = true;
        }

        // Validar fecha de vencimiento
        if (!expiryDateInput.value || expiryDateInput.value.length !== 5) {
            expiryError.textContent = 'Por favor ingrese una fecha de vencimiento';
            hasErrors = true;
        } else {
            const [month, year] = expiryDateInput.value.split('/');
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear() % 100;
            const currentMonth = currentDate.getMonth() + 1;
            const maxYear = (currentDate.getFullYear() + 10) % 100;

            const inputMonth = parseInt(month);
            const inputYear = parseInt(year);

            if (inputMonth < 1 || inputMonth > 12) {
                expiryError.textContent = 'Mes inválido';
                hasErrors = true;
            } else if (inputYear < currentYear || (inputYear === currentYear && inputMonth < currentMonth)) {
                expiryError.textContent = 'La tarjeta está vencida';
                hasErrors = true;
            } else if (inputYear > maxYear) {
                expiryError.textContent = 'La fecha no puede exceder 10 años';
                hasErrors = true;
            }
        }

        // Validar CVV
        if (!cvvInput.value || cvvInput.value.length !== 3) {
            cvvError.textContent = 'Por favor ingrese un CVV';
            hasErrors = true;
        }

        if (!hasErrors) {
            // Limpiar el carrito
            localStorage.setItem('carrito', JSON.stringify([]));
            
            // Mostrar el modal de éxito
            const modal = document.getElementById('successModal');
            modal.classList.add('show');
        }
    });
}

// Función para volver al inicio
function volverAlInicio() {
    window.location.href = 'index.html';
}
