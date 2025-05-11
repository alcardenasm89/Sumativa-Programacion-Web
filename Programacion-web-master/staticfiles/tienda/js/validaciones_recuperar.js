const form = document.getElementById('recuperarPasswordForm');
const emailInput = document.getElementById('email');
const emailError = document.getElementById('email-error');

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

// Event Listeners para validación
emailInput.addEventListener('invalid', function(e) {
    e.preventDefault();
    e.stopPropagation();
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

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!emailInput.validity.valid) {
        emailError.textContent = 'Por favor, ingrese un correo electrónico válido';
        emailError.style.display = 'block';
        return;
    }

    if (!validarEmail(emailInput.value)) {
        emailError.textContent = 'Por favor, cumple todos los requisitos del correo electrónico';
        emailError.style.display = 'block';
        return;
    }

    // Aquí iría la lógica de recuperación de contraseña
    // Por ahora, solo mostraremos un mensaje de éxito

    const datosHTML = `
    <div class="datos-mostrados">
        <h2>¡Correo enviado!</h2>
        <p>Se ha enviado un enlace de recuperación a tu correo electrónico.</p>
        <p>Por favor, revisa tu bandeja de entrada.</p>
        <button onclick="window.location.href='login.html'" class="submit-btn">Volver al login</button>
    </div>
`;
document.querySelector('.form-box').innerHTML = datosHTML;
});
