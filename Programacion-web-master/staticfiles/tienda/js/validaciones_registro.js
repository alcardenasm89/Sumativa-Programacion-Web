const form = document.getElementById('registroForm');
const password = document.getElementById('password');
const confirmarPassword = document.getElementById('confirmarPassword');
const passwordError = document.getElementById('password-error');
const confirmarPasswordError = document.getElementById('confirmarPassword-error');
const emailInput = document.getElementById('email');
const emailError = document.getElementById('email-error');
const fechaNacimiento = document.getElementById('fechaNacimiento');
const fechaError = document.getElementById('fecha-error');
const nombreInput = document.getElementById('nombre');
const nombreError = document.getElementById('nombre-error');
const usernameInput = document.getElementById('username');
const usernameError = document.getElementById('username-error');

// Establecer la fecha máxima (hoy)
const hoy = new Date();
const minimo = new Date();
minimo.setFullYear(hoy.getFullYear() - 100); // Límite de 100 años hacia atrás

fechaNacimiento.max = hoy.toISOString().split('T')[0];
fechaNacimiento.min = minimo.toISOString().split('T')[0];

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById('toggleIcon-' + inputId);
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function validarContraseñas() {
    if (password.value.length < 6) {
        passwordError.textContent = 'La contraseña debe tener al menos 6 caracteres';
        passwordError.style.display = 'block';
        return false;
    } else {
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    }

    if (password.value !== confirmarPassword.value) {
        confirmarPasswordError.textContent = 'Las contraseñas no coinciden';
        confirmarPasswordError.style.display = 'block';
        return false;
    } else {
        confirmarPasswordError.textContent = '';
        confirmarPasswordError.style.display = 'none';
        return true;
    }
}

function validarContraseña(contraseña) {
    const tieneNumero = /[0-9]/.test(contraseña);
    const tieneMayuscula = /[A-Z]/.test(contraseña);
    const longitudCorrecta = contraseña.length >= 6 && contraseña.length <= 18;
    const tieneCaracterEspecial = /[.,!@#$%^&*]/.test(contraseña);

    const reqLength = document.getElementById('req-length');
    const reqNumber = document.getElementById('req-number');
    const reqMayus = document.getElementById('req-mayus');
    const reqSpecial = document.getElementById('req-special');

    reqLength.className = longitudCorrecta ? 'valido' : 'invalido';
    reqNumber.className = tieneNumero ? 'valido' : 'invalido';
    reqMayus.className = tieneMayuscula ? 'valido' : 'invalido';
    reqSpecial.className = tieneCaracterEspecial ? 'valido' : 'invalido';

    return longitudCorrecta && tieneNumero && tieneMayuscula && tieneCaracterEspecial;
}

function validarFecha() {
    const fecha = new Date(fechaNacimiento.value);
    const edad = hoy.getFullYear() - fecha.getFullYear();
    const mes = hoy.getMonth() - fecha.getMonth();
    
    if (fecha > hoy) {
        fechaError.textContent = 'La fecha no puede ser futura';
        fechaError.style.display = 'block';
        return false;
    }
    
    if (edad < 13 || (edad === 13 && mes < 0)) {
        fechaError.textContent = 'Debes tener al menos 13 años para registrarte';
        fechaError.style.display = 'block';
        return false;
    }
    
    if (edad > 100) {
        fechaError.textContent = 'Por favor, ingresa una fecha válida';
        fechaError.style.display = 'block';
        return false;
    }
    
    fechaError.textContent = '';
    fechaError.style.display = 'none';
    return true;
}

function validarEmail(email) {
    const formatoValido = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
    const caracteresPermitidos = /^[a-zA-Z0-9._%+-@]+$/.test(email.split('@')[0]);
    const dominioValido = /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split('@')[1]);

    const reqFormato = document.getElementById('req-email-formato');
    const reqCaracteres = document.getElementById('req-email-caracteres');
    const reqDominio = document.getElementById('req-email-dominio');

    reqFormato.className = formatoValido ? 'valido' : 'invalido';
    reqCaracteres.className = caracteresPermitidos ? 'valido' : 'invalido';
    reqDominio.className = dominioValido ? 'valido' : 'invalido';

    return formatoValido && caracteresPermitidos && dominioValido;
}

// Event Listeners
password.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        passwordError.textContent = 'Por favor, ingrese una contraseña válida';
        passwordError.style.display = 'block';
    } else {
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    }
});

confirmarPassword.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        confirmarPasswordError.textContent = 'Por favor, confirme su contraseña';
        confirmarPasswordError.style.display = 'block';
    } else {
        confirmarPasswordError.textContent = '';
        confirmarPasswordError.style.display = 'none';
    }
});

fechaNacimiento.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        fechaError.textContent = 'Por favor, seleccione su fecha de nacimiento';
        fechaError.style.display = 'block';
    } else {
        fechaError.textContent = '';
        fechaError.style.display = 'none';
    }
});

emailInput.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        emailError.textContent = 'Por favor, ingrese un correo electrónico válido';
        emailError.style.display = 'block';
    } else {
        emailError.textContent = '';
        emailError.style.display = 'none';
    }
});

emailInput.addEventListener('input', function() {
    const esValido = validarEmail(this.value);
    if (!esValido) {
        emailError.textContent = 'Por favor, cumple todos los requisitos del correo electrónico';
        emailError.style.display = 'block';
    } else {
        emailError.textContent = '';
        emailError.style.display = 'none';
    }
});

usernameInput.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        usernameError.textContent = 'Por favor, ingrese un nombre de usuario';
        usernameError.style.display = 'block';
    } else {
        usernameError.textContent = '';
        usernameError.style.display = 'none';
    }
});

nombreInput.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        nombreError.textContent = 'Por favor, ingrese su nombre completo';
        nombreError.style.display = 'block';
    } else {
        nombreError.textContent = '';
        nombreError.style.display = 'none';
    }
});

// Event Listeners para validación en tiempo real
password.addEventListener('input', function() {
    const esValida = validarContraseña(this.value);
    if (!esValida) {
        passwordError.textContent = 'Por favor, cumple todos los requisitos de la contraseña';
        passwordError.style.display = 'block';
    } else {
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    }
    validarContraseñas();
});

confirmarPassword.addEventListener('input', validarContraseñas);

fechaNacimiento.addEventListener('change', validarFecha);


form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!nombreInput.validity.valid) {
        nombreError.textContent = 'Por favor, ingrese su nombre completo';
        nombreError.style.display = 'block';
        return;
    }

    if (!usernameInput.validity.valid) {
        usernameError.textContent = 'Por favor, ingrese un nombre de usuario';
        usernameError.style.display = 'block';
        return;
    }
    
    if (!emailInput.validity.valid) {
        emailError.textContent = 'Por favor, ingrese un correo electrónico válido';
        emailError.style.display = 'block';
        return;
    }

    if (!validarContraseña(password.value)) {
        return;
    }

    if (password.value !== confirmarPassword.value) {
        confirmarPassword.setCustomValidity('Las contraseñas no coinciden');
        return;
    }

    if (!validarFecha()) {
        return;
    }

    // Mostrar los datos en la página
    mostrarDatos(e);
});

function mostrarDatos(e) {
    e.preventDefault();
    
    // Obtener los valores del formulario
    const nombre = document.getElementById('nombre').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const fechaNacimiento = document.getElementById('fechaNacimiento').value;
    const direccion = document.getElementById('direccion').value;

    // Crear el HTML para mostrar los datos
    const datosHTML = `
        <div class="datos-mostrados">
            <h2>Datos registrados:</h2>
            <p><strong>Nombre:</strong> ${nombre}</p>
            <p><strong>Usuario:</strong> ${username}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Fecha de nacimiento:</strong> ${fechaNacimiento}</p>
            <p><strong>Dirección:</strong> ${direccion}</p>
            <p><strong>Contraseña:</strong> [Protegida]</p>
            <div class="button-container">
                <a href="login.html" class="submit-btn">Iniciar Sesión</a>
            </div>
        </div>
    `;

    // Ocultar el formulario y mostrar los datos
    document.querySelector('.form-box').innerHTML = datosHTML;
}