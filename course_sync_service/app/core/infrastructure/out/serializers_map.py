from rest_framework.exceptions import APIException

from course_sync_service.app.core.infrastructure.out.curso_create_response_serializer import CursoGoogleResponseSerializer
from course_sync_service.app.courses.infrastructure.out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_get_response_serializer import CursoGetResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_update_response_serializer import CursoUpdateResponseSerializer

output_map = {
    "core_course_create_courses": CursoGoogleResponseSerializer,
    "core_course_delete_courses": CursoDeleteResponseSerializer,
    "core_course_get_courses": CursoGetResponseSerializer,
    "core_course_update_courses": CursoUpdateResponseSerializer,
    "enrol_manual_enrol_users": CursoUpdateResponseSerializer,
    "enrol_manual_unenrol_users": CursoUpdateResponseSerializer,
}

OUTPUT_IS_LIST = {
    "core_course_create_courses": True,
    "core_course_delete_courses": False,
    "core_course_get_courses": True,
    "core_course_update_courses": False,
    "enrol_manual_enrol_users": False,
    "enrol_manual_unenrol_users": False,
}

def output_serializer_for(action, result):
    try:
        SerializerCls = output_map[action]
    except KeyError:
        raise APIException(f"La acción '{action}' no tiene serializer configurado")

    is_list = OUTPUT_IS_LIST.get(action, False)

    # Normalización: si debe ser lista pero no lo es, envolverlo
    if is_list and not isinstance(result, list):
        result = [result]

    # Normalización: si NO debe ser lista pero viene lista, tomar solo uno
    if not is_list and isinstance(result, list):
        result = result[0] if result else None

    serializer = SerializerCls(result, many=is_list)
    return serializer.data
