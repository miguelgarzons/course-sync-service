

from course_sync_service.app.courses.infrastructure.input.delete_params_serializer import MoodleDeleteParamsSerializer
from course_sync_service.app.courses.infrastructure.input.get_params_serializer import MoodleGetParamsSerializer
from course_sync_service.app.courses.infrastructure.input.serializers import MoodleQueryParamsSerializer
from course_sync_service.app.courses.infrastructure.input.update_params_serializer import MoodleUpdateParamsSerializer
from rest_framework.exceptions import APIException


output_map = {
    "core_course_create_courses": MoodleQueryParamsSerializer,
    "core_course_delete_courses": MoodleDeleteParamsSerializer,
    "core_course_update_courses": MoodleUpdateParamsSerializer,
    "core_course_get_courses": MoodleGetParamsSerializer,
}

def input_serializer_for(action, data=None):
        try:
            SerializerClass = output_map[action]
            return SerializerClass(
                data=data,
                many=isinstance(data, list)
            )
        except KeyError:
            raise APIException(f"La acción '{action}' no está soportada")
