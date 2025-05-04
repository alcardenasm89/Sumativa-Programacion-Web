const form = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');
const usernameError = document.getElementById('username-error');
const passwordError = document.getElementById('password-error');

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`toggleIcon-${inputId}`);
    const error = document.getElementById(`${inputId}-error`);

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
        error.style.display = 'none';
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function validarContraseña(contraseña) {
    const tieneNumero = /[0-9]/.test(contraseña);
    const tieneMayuscula = /[A-Z]/.test(contraseña);
    const longitudCorrecta = contraseña.length >= 6 && contraseña.length <= 18;
    const tieneCaracterEspecial = /[.,!@#$%^&*]/.test(contraseña);

    if (!longitudCorrecta) {
        passwordError.textContent = 'La contraseña debe tener entre 6 y 18 caracteres';
        passwordError.style.display = 'block';
        return false;
    }

    if (!tieneNumero) {
        passwordError.textContent = 'La contraseña debe contener al menos un número';
        passwordError.style.display = 'block';
        return false;
    }

    if (!tieneMayuscula) {
        passwordError.textContent = 'La contraseña debe contener al menos una letra mayúscula';
        passwordError.style.display = 'block';
        return false;
    }

    if (!tieneCaracterEspecial) {
        passwordError.textContent = 'La contraseña debe contener al menos un carácter especial (.,!@#$%^&*)';
        passwordError.style.display = 'block';
        return false;
    }

    passwordError.style.display = 'none';
    return true;
}

function validarFormulario() {
    let esValido = true;

    // Validar nombre de usuario
    if (username.value.trim() === '') {
        usernameError.textContent = 'Por favor, ingrese su nombre de usuario';
        usernameError.style.display = 'block';
        esValido = false;
    } else {
        usernameError.style.display = 'none';
    }

    // Validar contraseña
    if (password.value.trim() === '') {
        passwordError.textContent = 'Por favor, ingrese su contraseña';
        passwordError.style.display = 'block';
        esValido = false;
    } else {
        passwordError.style.display = 'none';
    }

    return esValido;
}

// Event Listeners

username.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        usernameError.textContent = 'Por favor, ingrese su nombre de usuario';
        usernameError.style.display = 'block';
    } else {
        usernameError.textContent = '';
        usernameError.style.display = 'none';
    }
});

password.addEventListener('invalid', function(e) {
    e.preventDefault();
    if (!this.validity.valid) {
        passwordError.textContent = 'Por favor, ingrese su contraseña';
        passwordError.style.display = 'block';
    } else {
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    }
});

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    let esValido = validarFormulario();
    
    if (esValido) {
        // Simular verificación de credenciales (en un caso real, esto se haría con una API)
        if (username.value === 'admin' && password.value === 'admin123') {
            // Si es el administrador, redirigir al panel de administración
            window.location.href = 'admin.html';
        } else {
            // Verificar si el usuario existe en localStorage (simulación de base de datos)
            const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
            
            const usuario = usuarios.find(u => 
                u.username === username.value && u.password === password.value
            );

            if (usuario) {
                // Guardar información del usuario actual
                const usuarioActual = {
                    id: usuario.id,
                    nombre: usuario.nombre,
                    email: usuario.email,
                    username: usuario.username
                };

                localStorage.setItem('usuarioActual', JSON.stringify(usuarioActual));

                // Si marcó "Recordarme", guardar la sesión
                const rememberMe = document.getElementById('remember-me').checked;
                if (rememberMe) {
                    localStorage.setItem('sesionGuardada', JSON.stringify({
                        username: username.value,
                        rememberMe: true
                    }));
                }

                // Redirigir al panel de usuario
                window.location.href = 'panel-usuario.html';
            } else {
                // Mostrar mensaje de error
                usernameError.textContent = 'Usuario o contraseña incorrectos';
                usernameError.style.display = 'block';
                passwordError.textContent = 'Usuario o contraseña incorrectos';
                passwordError.style.display = 'block';
            }
        }
    }
});

// Verificar si hay una sesión guardada al cargar la página
window.addEventListener('load', function() {
    const sesionGuardada = JSON.parse(localStorage.getItem('sesionGuardada'));
    if (sesionGuardada && sesionGuardada.rememberMe) {
        username.value = sesionGuardada.username;
        document.getElementById('remember-me').checked = true;
    }
}); 