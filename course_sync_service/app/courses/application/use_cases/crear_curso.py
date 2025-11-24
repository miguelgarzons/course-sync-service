from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from course_sync_service.app.courses.application.mappers.curso_moodle_mapper import CursoMoodleMapper
from course_sync_service.app.courses.application.mappers.curso_google_mapper import CursoGoogleMapper
from course_sync_service.app.courses.application.mappers.mapper_sinu import CursoSinuMapper


class CrearCurso:

    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data):
        cursos = CursoMoodleMapper.from_validated_data(validated_data)
        resultados_google = []
        for curso in cursos:
            google_format = CursoGoogleMapper.to_google_format(curso)
            result = self.google_classroom_client.create_course(google_format)
            resultados_google.append({
                'course_id': result.get('id'),
                'name': result.get('name'),
                'enrollment_code': result.get('enrollmentCode'),
                'alternate_link': result.get('alternateLink'),
                'raw_data': result,
            })
        resultados_sinu = CursoSinuMapper.from_validated_data(resultados_google)
        if len(resultados_sinu) == 1:
            return resultados_sinu[0]
        return resultados_sinu
