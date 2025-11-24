from course_sync_service.app.core.infrastructure.out.curso_create_response_serializer import CursoGoogleResponseSerializer
from course_sync_service.app.courses.infrastructure.out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_get_response_serializer import CursoGetResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_update_response_serializer import CursoUpdateResponseSerializer


output_map = {
    "core_course_create_courses": CursoGoogleResponseSerializer,
    "core_course_delete_courses": CursoDeleteResponseSerializer,
    "core_course_get_courses": CursoGetResponseSerializer,
    "core_course_update_courses": CursoUpdateResponseSerializer,
}

def output_serializer_for(action):
    return output_map[action]
