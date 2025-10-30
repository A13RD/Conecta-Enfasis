from pydantic import BaseModel

class Docente(BaseModel):
    id: int
    nombre: str
    contraseña: str

    def registrar_notas(self):
        pass

    def crear_cronogramas(self):
        pass

    def subir_material(self):
        pass