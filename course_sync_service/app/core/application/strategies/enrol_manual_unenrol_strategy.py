from course_sync_service.app.shared.container import container
class UnenrolStudentStrategy:
    def execute(self, data):
        return container.student.matricular.ejecutar(data)
