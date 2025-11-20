from course_sync_service.app.core.application.strategies.create_student_strategy import CreateStudentStrategy
from course_sync_service.app.core.application.strategies.delete_student_strategy import DeleteStudentStrategy
from course_sync_service.app.core.application.strategies.get_student_strategy import GetStudentStrategy

from rest_framework.exceptions import APIException

class StrategyFactory:

    strategies = {
        "create": CreateStudentStrategy(),
        "delete": DeleteStudentStrategy(),
        "get": GetStudentStrategy(),
    }

    @classmethod
    def get_strategy(cls, action):
        try:
            return cls.strategies[action]
        except KeyError:
            raise APIException(f"La acción '{action}' no está soportada")
