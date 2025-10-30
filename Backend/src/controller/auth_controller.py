# Backend/src/controller/auth_controller.py

from typing import Dict, Any
from pydantic import BaseModel # 🚨 NUEVA IMPORTACIÓN
from src.controller.db_manager import db_manager

# DTO para el cuerpo de la solicitud POST
class LoginRequest(BaseModel):
    username: str
    password: str

class AuthController:
    """Controlador de Autenticación (Aplicable a HU10)."""

    def login(self, username: str, password: str, rol: str) -> Dict[str, Any] | None:
        """
        HU10: Iniciar sesión con contraseña.
        """
        print(f"DEBUG AUTH: Buscando usuario {username} con rol {rol} en DB.") 

        # Usamos :placeholders para la consulta SQL
        query = "SELECT id, nombre, rol, programa_id FROM usuarios WHERE id = :username AND contraseña = :password AND rol = :rol"
        params = {"username": username, "password": password, "rol": rol}
        
        user_data = db_manager.fetch_one(query, params)

        if user_data:
            return {"token": f"simulated_jwt_for_{username}", "user": user_data}
        
        return None