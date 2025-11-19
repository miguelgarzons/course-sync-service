from typing import Any, Dict
import uuid

from course_sync_service.app.courses.application.mappers.moodle_get_mapper import MoodleGetMapper
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient

class ObtenerCursos:
    def __init__(self, google_classroom_client: GoogleClassroomClient):
        self.google_classroom_client = google_classroom_client

    def ejecutar(self, validated_data) -> Dict[str, Any]:
        entidad = MoodleGetMapper.from_validated_data(validated_data)   
        if not entidad.ids:
            success = self.google_classroom_client.get_all_courses()
        else:
            course_id = entidad.ids[0]
            success = self.google_classroom_client.get_course(course_id)

        return success
