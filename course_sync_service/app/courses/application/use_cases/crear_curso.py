from course_sync_service.app.core.integrations.google_classroom_client import GoogleClassroomClient
from course_sync_service.app.courses.application.mappers.curso_moodle_mapper import CursoMoodleMapper
from course_sync_service.app.courses.application.mappers.curso_google_mapper import CursoGoogleMapper


class CrearCurso:

    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data):
        print(validated_data)
        cursos = CursoMoodleMapper.from_validated_data(validated_data)

        resultados = []

        for curso in cursos:
            google_format = CursoGoogleMapper.to_google_format(curso)
            result = self.google_classroom_client.create_course(google_format)

            resultados.append({
                'course_id': result.get('id'),
                'name': result.get('name'),
                'enrollment_code': result.get('enrollmentCode'),
                'alternate_link': result.get('alternateLink'),
                'raw_data': result,
            })

        if len(resultados) == 1:
            return resultados[0]
        return resultados
