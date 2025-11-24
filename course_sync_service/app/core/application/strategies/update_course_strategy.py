from course_sync_service.app.shared.container import container
class UpdateCourseStrategy:
    def execute(self, data):
        return container.course().update().ejecutar(data)
