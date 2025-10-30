from typing import Dict, Any, List
from datetime import date
from src.controller.db_manager import db_manager
from src.model.chatbot import ChatBot
from src.model.curso import Curso
from src.model.inscripcion import Inscripcion
from src.model.reporte import Reporte
from src.model.estudiante import Estudiante
#from Backend.src.model.notificacion import Notificacion # Para HU6 (asumida)

class ChatBotController:
    """Controlador para la lógica de EduBot (HU3, HU5, HU7, HU8)."""

    def __init__(self):
        self.chatbot = ChatBot()

    def procesar_mensaje_hu3(self, estudiante_id: int, curso_nombre: str) -> str:
        """
        HU3: Mostrar cupos y validar prerrequisitos.
        Flujo: ChatBot -> InscripcionController (simulado) -> Curso.validar_cupo() -> Inscripcion.valoridad_prerrequisitos()
        """

        curso_data = db_manager.fetch_one(
            "SELECT * FROM cursos WHERE nombre = %s", 
            (curso_nombre,)
        )
        estudiante_data = db_manager.fetch_one(
            "SELECT * FROM usuarios WHERE id = %s AND rol = 'estudiante'", 
            (estudiante_id,)
        )

        if not curso_data or not estudiante_data:
            return "❌ Curso o estudiante no encontrado."

        curso = Curso(**curso_data)
        inscripcion_logic = Inscripcion(id=0, estudianteId=estudiante_id, cursoId=curso.idCurso, fechaInscripcion=date.today())


        if not curso.validar_cupo():
            return f"❌ El curso '{curso.nombre}' (ID: {curso.idCurso}) no tiene cupos disponibles."


        if not inscripcion_logic.valoridad_prerrequisitos(estudiante_id, curso.prerrequisitos):
            return f"❌ Cumple cupo ({curso.cupo} disponibles) pero NO cumple con los prerrequisitos del curso '{curso.nombre}'."


        return f"✅ Cumple con cupo ({curso.cupo} disponibles) y prerrequisitos. Puedes inscribirte en '{curso.nombre}' (ID: {curso.idCurso})."


    def inscribir_estudiante_hu5(self, estudiante_id: int, curso_id: int) -> str:
        """
        HU5: Inscribirse en un curso directamente desde EduBot.
        Asume que la validación (HU3) ya ocurrió o la integra.
        """

        curso_data = db_manager.fetch_one(
            "SELECT * FROM cursos WHERE idCurso = %s AND estado = 'aprobado'", 
            (curso_id,)
        )

        if not curso_data:
            return "❌ El curso no existe o no ha sido aprobado por el coordinador."

        curso = Curso(**curso_data)
        inscripcion_logic = Inscripcion(id=0, estudianteId=estudiante_id, cursoId=curso_id, fechaInscripcion=date.today())

        if not curso.validar_cupo():
            return "❌ Inscripción fallida: No hay cupos disponibles."
        if not inscripcion_logic.valoridad_prerrequisitos(estudiante_id, curso.prerrequisitos):
             return "❌ Inscripción fallida: No cumple con los prerrequisitos."

  
        if db_manager.execute_and_commit("INSERT INTO inscripcion (estudiante_id, curso_id) VALUES (%s, %s)", (estudiante_id, curso_id)):
        
            comprobante_data = self.generar_comprobante_hu8(estudiante_id, f"Inscripción al curso {curso.nombre}")
            return f"🎉 **Inscripción exitosa** en el curso '{curso.nombre}'. {comprobante_data}"

        return "❌ Error al registrar la inscripción (ya podrías estar inscrito)."


    def generar_progreso_hu7(self, estudiante_id: int) -> str:
        """
        HU7: Solicitar un reporte consolidado de mi progreso.
        Flujo: ChatBot -> Reporte.generar() -> Database
        """

        cursos_inscritos = db_manager.fetch_all("SELECT * FROM inscripciones WHERE estudiante_id = %s", (estudiante_id,))

        progreso_data = []
        for curso in cursos_inscritos:
            progreso_data.append({
                "curso_id": curso["idCurso"],
                "nombre": curso["nombre"],
                "creditos": curso["creditos"],
                "estado_academico": "Activo" if curso["estado"] == "aprobado" else "Finalizado (Nota: 4.5)" # Simulación
            })


        reporte_logic = Reporte(id=db_manager.get_new_id("reporte"), estudianteId=estudiante_id, tipo="Progreso")
        reporte_logic.generar(progreso_data)


        reporte_exportado = reporte_logic.exportar(formato="PDF")

        output = self.chatbot.mostrar_cursos(progreso_data) # Reutilizamos formato de chat
        return f"📄 **Reporte de Progreso Consolidado** generado y listo para exportar:\n{output}\nContenido de Comprobante: {reporte_exportado.decode('utf-8')}"


    def generar_comprobante_hu8(self, estudiante_id: int, detalle: str) -> str:
        """
        HU8: Generar comprobantes. (Subfunción usada en HU5/HU7)
        """

        comprobante_logic = Reporte(id=db_manager.get_new_id("comprobante"), estudianteId=estudiante_id, tipo="Comprobante")
        comprobante_logic.generar([{"detalle": detalle, "fecha": str(date.today())}])

        comprobante_exportado = comprobante_logic.exportar(formato="PDF_Comprobante")
        return f"**Comprobante generado**: {comprobante_exportado.decode('utf-8')}"


    def notificar_cambio_hu6(self, curso_id: int, mensaje: str):
        """
        HU6: Recibir notificaciones automáticas de cambios.
        Esto es una función interna, disparada por otros eventos (e.g., Docente actualiza cronograma).
        """

        estudiantes_inscritos_ids = [k for k, v in db_manager.db["inscripciones"].items() if curso_id in v]

  
        for est_id in estudiantes_inscritos_ids:
            print(f"**NOTIFICACIÓN ENVIADA a Estudiante {est_id}:** {mensaje}")

        return len(estudiantes_inscritos_ids)