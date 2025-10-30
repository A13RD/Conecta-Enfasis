from pydantic import BaseModel

class Notificacion(BaseModel):
    id: int
    estudianteId: int
    mensaje: str
    leido: bool = False

    def enviar(self) -> bool:
        """Envía la notificación al estudiante (lógica en Controller)."""
        return True

    def marcar_como_leida(self):
        """Marca la notificación como leída."""
        self.leido = True