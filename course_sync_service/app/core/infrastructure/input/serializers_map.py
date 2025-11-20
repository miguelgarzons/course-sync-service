

from course_sync_service.app.courses.infrastructure.input.delete_params_serializer import MoodleDeleteParamsSerializer
from course_sync_service.app.courses.infrastructure.input.get_params_serializer import MoodleGetParamsSerializer
from course_sync_service.app.courses.infrastructure.input.serializers import MoodleQueryParamsSerializer


output_map = {
    "core_course_create_courses": MoodleQueryParamsSerializer,
    "core_course_delete_courses": MoodleDeleteParamsSerializer,
    "core_course_update_courses":MoodleGetParamsSerializer,
    "core_course_get_courses":MoodleGetParamsSerializer,
}

def input_serializer_for(action):
    return output_map[action]
