from typing import Any, Dict
import uuid

from course_sync_service.app.courses.application.mappers.mapper_sinu import CursoSinuMapper
from course_sync_service.app.courses.application.mappers.moodle_get_mapper import MoodleGetMapper
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient

from typing import Dict, Any
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from course_sync_service.app.courses.application.mappers.moodle_get_mapper import MoodleGetMapper


class ObtenerCursos:

    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data) -> Dict[str, Any]:

        entidad = MoodleGetMapper.from_validated_data(validated_data)

        # -----------------------------------------------------------------------
        # SIN IDS → obtener todos los cursos
        # -----------------------------------------------------------------------
        if not entidad.ids:
            google_courses = self.google_classroom_client.get_all_courses()

            # Classroom devuelve una lista → la mapeamos directo
            if isinstance(google_courses, list):
                return [CursoSinuMapper.map_course(curso) for curso in google_courses]

            raise ValueError("Formato inesperado desde get_all_courses()")

        # -----------------------------------------------------------------------
        # CON ID → obtener un curso específico
        # -----------------------------------------------------------------------
        course_id = entidad.ids[0]
        google_course = self.google_classroom_client.get_course(course_id)
        print(google_course)
        if isinstance(google_course, dict):
            return CursoSinuMapper.map_course(google_course)

        raise ValueError("Formato inesperado desde get_course()")
