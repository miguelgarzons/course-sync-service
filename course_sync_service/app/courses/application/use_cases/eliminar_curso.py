from typing import Dict, Any

from course_sync_service.app.courses.application.mappers.moodle_delete_mapper import MoodleDeleteMapper
from course_sync_service.app.core.integrations.google_classroom_client import GoogleClassroomClient


class EliminarCurso:

    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data) -> Dict[str, Any]:
        entidad = MoodleDeleteMapper.from_validated_data(validated_data)

        resultados = []

        for course_id in entidad.ids:
            success = self.google_classroom_client.delete_course(course_id)

            resultados.append({
                'course_id': course_id,
                'status': 'deleted' if success else 'error',
                'message': 'Curso archivado exitosamente' if success else 'Error al archivar curso'
            })


        return resultados[0] if len(resultados) == 1 else resultados
