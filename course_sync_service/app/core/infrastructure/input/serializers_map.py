


from course_sync_service.app.courses.infrastructure.input.delete_params_serializer import MoodleDeleteParamsSerializer
from course_sync_service.app.courses.infrastructure.input.get_params_serializer import MoodleGetParamsSerializer
from course_sync_service.app.courses.infrastructure.input.serializers import MoodleQueryParamsSerializer
from course_sync_service.app.courses.infrastructure.input.update_params_serializer import MoodleUpdateParamsSerializer
from course_sync_service.app.student.infrastructure.input.serializers import MoodleEnrolmentParamsSerializer
from course_sync_service.app.student.infrastructure.input.unenrol_users_serializer import MoodleUnenrolmentParamsSerializer
from course_sync_service.app.student.infrastructure.input.create_user_params_serializer import MoodleCreateUsersSerializer
from rest_framework.exceptions import APIException



GET_SERIALIZERS = {
    "core_course_get_courses": MoodleGetParamsSerializer,
}

POST_SERIALIZERS = {
    "core_user_create_users":MoodleCreateUsersSerializer,
    "core_course_create_courses": MoodleQueryParamsSerializer,
    "core_course_delete_courses": MoodleDeleteParamsSerializer,
    "core_course_update_courses": MoodleUpdateParamsSerializer,
    "enrol_manual_enrol_users": MoodleEnrolmentParamsSerializer,
    "enrol_manual_unenrol_users": MoodleUnenrolmentParamsSerializer,
    
}

def input_serializer_for(action, method, data):
    if method == "GET":
        serializer_class = GET_SERIALIZERS.get(action)
    elif method == "POST":
        serializer_class = POST_SERIALIZERS.get(action)
    else:
        raise APIException(f"Método {method} no soportado")

    if not serializer_class:
        raise APIException(f"La acción '{action}' no está soportada para {method}")

    return serializer_class(data=data, many=isinstance(data, list))
