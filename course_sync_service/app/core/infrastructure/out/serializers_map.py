from course_sync_service.app.core.infrastructure.out.curso_create_response_serializer import CursoGoogleResponseSerializer
from course_sync_service.app.courses.infrastructure.out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_get_response_serializer import CursoGetResponseSerializer


output_map = {
    "create": CursoGoogleResponseSerializer,
    "delete": CursoDeleteResponseSerializer,
    "get": CursoGetResponseSerializer,
}

def output_serializer_for(action):
    return output_map[action]
