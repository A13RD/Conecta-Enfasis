const API_URL = "http://localhost:8000"; 
let selectedRole = "estudiante";

function selectRole(role) {
    selectedRole = role;
    document.querySelectorAll(".role-option").forEach(opt => opt.classList.remove("active"));
    event.target.closest(".role-option").classList.add("active");
}

function togglePassword() {
    const input = document.getElementById("password");
    const icon = document.querySelector(".password-toggle");
    const showing = input.type === "text";
    input.type = showing ? "password" : "text";
    icon.textContent = showing ? "👁️" : "🙈";
}

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const rememberMe = document.getElementById("rememberMe").checked;

    showAlert("Verificando credenciales...", "success");

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password, role: selectedRole}),
        });

        if (!response.ok) throw new Error("Credenciales inválidas");

        const data = await response.json();

        
        if (data.access_token && data.user) {
            sessionStorage.setItem("token", data.access_token);
            sessionStorage.setItem("currentUser", JSON.stringify(data.user));
            showAlert("¡Inicio de sesión exitoso! Redirigiendo...", "success");
            redirectByRole(data.user.rol);
        } else {
            throw new Error("Formato de respuesta inesperado");
        }

    } catch (err) {
        console.warn("Error de autenticación o backend inactivo:", err);
        authenticateDemo(username, password); 
    }
}

function authenticateDemo(username, password) {
    const demoUsers = {
        estudiante: {
            username: "EST001",
            password: "estudiante123",
            data: {
                id: 1,
                nombre: "Ana López García",
                codigo: "EST001",
                programa: "Ingeniería de Sistemas",
                rol: "estudiante",
                email: "ana.lopez@udem.edu.co"
            }
        },
        coordinador: {
            username: "COORD001",
            password: "coordinador123",
            data: {
                id: 2,
                nombre: "Dr. Carlos Ramírez",
                codigo: "COORD001",
                programa: "Coordinación Académica",
                rol: "coordinador",
                email: "carlos.ramirez@udem.edu.co"
            }
        },
        docente: {
            username: "DOC001",
            password: "docente123",
            data: {
                id: 3,
                nombre: "Dra. María González",
                codigo: "DOC001",
                departamento: "Ciencias Básicas",
                rol: "docente",
                email: "maria.gonzalez@udem.edu.co"
            }
        }
    };

    const user = demoUsers[selectedRole];

    if (user && (username === user.username || username === "demo") &&
        (password === user.password || password === "demo")) {
        loginSuccess(user.data);
    } else {
        showAlert("Usuario o contraseña incorrectos. Usa 'demo' / 'demo' o credenciales válidas.", "error");
    }
}

function loginSuccess(userData) {
    sessionStorage.setItem("currentUser", JSON.stringify(userData));
    showAlert("¡Inicio de sesión exitoso! Redirigiendo...", "success");
    redirectByRole(userData.rol);
}

function redirectByRole(rol) {
    setTimeout(() => {
        switch (rol) {
            case "estudiante":
                window.location.href = "index.html";
                break;
            case "coordinador":
                window.location.href = "coordinador.html";
                break;
            case "docente":
                window.location.href = "docente.html";
                break;
            default:
                window.location.href = "index.html";
        }
    }, 1000);
}

function quickLogin(role) {
    selectedRole = role;
    selectRoleUI(role);
    document.getElementById("username").value = "demo";
    document.getElementById("password").value = "demo";
    document.getElementById("loginForm").dispatchEvent(new Event("submit"));
}

function selectRoleUI(role) {
    document.querySelectorAll(".role-option").forEach(opt => opt.classList.remove("active"));
    const options = document.querySelectorAll(".role-option");
    if (role === "estudiante") options[0].classList.add("active");
    if (role === "coordinador") options[1].classList.add("active");
    if (role === "docente") options[2].classList.add("active");
}

function showAlert(message, type) {
    const alertDiv = document.getElementById("alertMessage");
    alertDiv.textContent = message;
    alertDiv.className = `alert ${type}`;
    alertDiv.style.display = "block";

    if (type === "success") {
        setTimeout(() => {
            alertDiv.style.display = "none";
        }, 3000);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const currentUser = sessionStorage.getItem("currentUser");
    if (currentUser) {
        const userData = JSON.parse(currentUser);
        showAlert("Ya tienes una sesión activa. Redirigiendo...", "success");
        redirectByRole(userData.rol);
    }
});

window.handleLogin = handleLogin;
window.togglePassword = togglePassword;
window.selectRole = selectRole;
window.quickLogin = quickLogin;
