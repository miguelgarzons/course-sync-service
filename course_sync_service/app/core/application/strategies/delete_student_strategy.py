from course_sync_service.app.shared.container import container
class DeleteStudentStrategy:
    def execute(self, data):
        return container.course().delete().ejecutar(data)
