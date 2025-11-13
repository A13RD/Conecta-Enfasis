
from typing import List
from datetime import date
from pydantic import BaseModel

class Inscripcion(BaseModel):
    id: int
    estudianteId: int
    cursoId: int
    fechaInscripcion: date
    estado: str = "inscrito" 
    notaFinal: float | None = None


    def valoridad_prerrequisitos(self, estudiante_id: int, curso_prerreq: List[int]) -> bool:
        """Valida que el estudiante cumpla los prerrequisitos del curso."""
        print(f"Validando prerrequisitos para estudiante {estudiante_id}...")
        return not curso_prerreq 

    def registrar(self) -> bool:
        """Guarda la inscripción en el sistema (lógica en Controller)."""
        return True