from typing import List, Dict, Any
from pydantic import BaseModel

class Reporte(BaseModel):
    id: int
    estudianteId: int
    tipo: str
    contenido: List[Dict[str, Any]]

    def generar(self, progreso_data: List[Dict[str, Any]]) -> 'Reporte':
        """Genera el contenido del reporte consolidado o comprobante."""
        self.contenido = progreso_data
        return self

    def exportar(self, formato: str = "PDF") -> bytes:
        """Exporta el reporte en formato institucional (simulado)."""
        print(f"Generando comprobante/reporte en formato {formato}...")
        return f"Comprobante/Reporte para estudiante {self.estudianteId}".encode('utf-8')