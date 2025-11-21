from course_sync_service.app.shared.container import container
class DeleteCourseStrategy:
    def execute(self, data):
        return container.course().delete().ejecutar(data)
