from pydantic import BaseModel

class Coordinador(BaseModel):
    id: int
    nombre: str
    contraseña: str

    def aprobar_curso(self, curso_id: int) -> bool:
        """Inicia la aprobación de un curso (lógica en Controller)."""
        return True

    def modificar_curso(self) -> bool:
        """Pass para Sprint 1."""
        pass

    def generar_reporte(self) -> bool:
        """Pass para Sprint 1."""
        pass

    def crear_curso(self) -> bool:
        """Inicia la creación de un curso (lógica en Controller)."""
        return True