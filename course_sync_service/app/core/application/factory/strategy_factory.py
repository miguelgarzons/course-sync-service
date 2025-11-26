from course_sync_service.app.core.application.strategies.create_course_strategy import CreateCoursetStrategy
from course_sync_service.app.core.application.strategies.delete_course_strategy import DeleteCourseStrategy
from course_sync_service.app.core.application.strategies.enrol_manual_unenrol_strategy import UnenrolStudentStrategy
from course_sync_service.app.core.application.strategies.enrol_student_strategy import EnrolStudentStrategy
from course_sync_service.app.core.application.strategies.get_course_strategy import GetCourseStrategy
from course_sync_service.app.core.application.strategies.update_course_strategy import UpdateCourseStrategy
from rest_framework.exceptions import APIException


class StrategyFactory:

    strategies = {
        "core_course_create_courses": CreateCoursetStrategy(),
        "core_course_delete_courses": DeleteCourseStrategy(),
        "core_course_get_courses": GetCourseStrategy(),
        "core_course_update_courses": UpdateCourseStrategy(),
        "enrol_manual_enrol_users": EnrolStudentStrategy(),
        "enrol_manual_unenrol_users": UnenrolStudentStrategy(),
    }

    @classmethod
    def get_strategy(cls, action):
        try:
            return cls.strategies[action]
        except KeyError:
            raise APIException(f"La acción '{action}' no está soportada")
