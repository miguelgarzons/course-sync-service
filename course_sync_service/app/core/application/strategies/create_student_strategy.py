from course_sync_service.app.shared.container import container
class CreateStudentStrategy:
    def execute(self, data):
        return container.course().create().ejecutar(data)
