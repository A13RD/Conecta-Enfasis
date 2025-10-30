from pydantic import BaseModel
from typing import List, Dict, Any

class ChatBot(BaseModel):
    idBot: int = 1
    nombre: str = "EduBot"

    # Métodos según UML (Importantes para HU3, HU5, HU6, HU7, HU8)
    def mostrar_cursos(self, cursos_data: List[Dict[str, Any]]) -> str:
        """Formatea y muestra la información de los cursos."""
        if not cursos_data:
            return "❌ No se encontraron cursos que cumplan con los criterios."

        output = "✅ Cursos disponibles:\n"
        for curso in cursos_data:
             output += f"- **{curso['nombre']}** (ID: {curso['idCurso']}) | Cupo: {curso['cupo']} | Estado: {curso['estado'].upper()}\n"
        return output

    def validar_inscripcion(self) -> bool:
        """Inicia el proceso de validación (lógica en Controller)."""
        return True # Inicia el flujo de prerrequisitos y cupos

    def enviar_notificacion(self) -> bool:
        """Inicia el proceso de envío de notificación (lógica en Controller)."""
        return True

    def generar_reporte(self) -> bool:
        """Inicia el proceso de generación de reporte (lógica en Controller)."""
        return True