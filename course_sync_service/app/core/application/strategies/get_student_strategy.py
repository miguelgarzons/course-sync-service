from course_sync_service.app.shared.container import container
class GetStudentStrategy:
    def execute(self, data):
        return container.course().list().ejecutar(data)
