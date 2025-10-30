from typing import List, Dict, Any
from src.controller.db_manager import db_manager
from src.model.lineaenfasis import LineaEnfasis
from src.model.programa import Programa

class EstudianteController:
    """Controlador para operaciones del Estudiante (HU1, HU2)."""

    def solicitarLineasEnfasis(self, programa_id: int) -> List[Dict[str, Any]]:
        """
        HU1: Como estudiante, quiero consultar las líneas de énfasis disponibles.
        Flujo: EstudianteController -> Database -> LineaEnfasis (crearDesdeDatos)
        """
        # 1. obtenerLineas(programa) de la DB
        lineas_data = db_manager.fetch_all(
            "SELECT * FROM LineaEnfasis WHERE idPrograma = %s", 
            (programa_id,)
        )


        lineas = [LineaEnfasis(**data) for data in lineas_data]


        return [l.model_dump() for l in lineas]


    def filtrarLineasPorSemestre(self, programa_id: int, semestre: int) -> List[Dict[str, Any]]:
        """
        HU2: Como estudiante, quiero filtrar las líneas de énfasis por semestre.
        Flujo: EstudianteController -> Database -> LineaEnfasis.filtrar_semestre()
        """
        lineas_data = db_manager.fetch_all(
            "SELECT * FROM LineaEnfasis WHERE idPrograma = %s", 
            (programa_id,)
        )

        cursos_filtrados_info = []
        for data in lineas_data:
            linea = LineaEnfasis(**data)
            cursos_ids = linea.filtrar_semestre(semestre)

            for curso_id in cursos_ids:
                curso_info = db_manager.fetch_one(
                    "SELECT * FROM cursos WHERE idCurso = %s AND estado = 'aprobado'",
                    (curso_id,)
                )
                if curso_info:
                    cursos_filtrados_info.append(curso_info)

        return cursos_filtrados_info