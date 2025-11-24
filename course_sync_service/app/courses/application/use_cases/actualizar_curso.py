import uuid

from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from course_sync_service.app.courses.application.mappers.curso_moodle_mapper import CursoMoodleMapper
from course_sync_service.app.courses.application.mappers.to_google_update_format import CursoGoogleUpdateMapper

class ActualizarCurso:
    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data):
        cursos_moodle = CursoMoodleMapper.from_validated_data(validated_data)  
        resultados = []
        for curso in cursos_moodle:
            google_format = CursoGoogleUpdateMapper.to_google_update_format(curso)
            result = self.google_classroom_client.update_course(
                curso.id,
                google_format
            )

            resultados.append({
                'course_id': result.get('id'),
                **result,
                'raw_data': result,
            })

        return resultados