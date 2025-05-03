<?php
// Verificar si se recibieron datos
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // Obtener los datos del formulario
    $nombre = $_GET['nombre'] ?? '';
    $username = $_GET['username'] ?? '';
    $email = $_GET['email'] ?? '';
    $password = $_GET['password'] ?? '';
    $fechaNacimiento = $_GET['fechaNacimiento'] ?? '';
    $direccion = $_GET['direccion'] ?? '';

    // Mostrar los datos recibidos
    echo "<h2>Datos recibidos:</h2>";
    echo "<p><strong>Nombre:</strong> " . htmlspecialchars($nombre) . "</p>";
    echo "<p><strong>Usuario:</strong> " . htmlspecialchars($username) . "</p>";
    echo "<p><strong>Email:</strong> " . htmlspecialchars($email) . "</p>";
    echo "<p><strong>Fecha de nacimiento:</strong> " . htmlspecialchars($fechaNacimiento) . "</p>";
    echo "<p><strong>Dirección:</strong> " . htmlspecialchars($direccion) . "</p>";
    
    // Mostrar la contraseña protegida
    echo "<p><strong>Contraseña:</strong> [Protegida]</p>";
    
    echo "<br><a href='registro.html'>Volver al formulario</a>";
} else {
    echo "No se recibieron datos del formulario.";
}
?> 