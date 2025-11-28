# course_sync_service/app/shared/app_container.py
from dependency_injector import containers, providers
from course_sync_service.app.shared.credentials import SharedContainer
from course_sync_service.app.courses.infrastructure.container import CourseContainer
from course_sync_service.app.student.infrastructure.container import StudentContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Contenedor global de la aplicación."""
    
    config = providers.Configuration()
    shared = providers.Container(SharedContainer)
    course = providers.Container(
        CourseContainer,
        google_classroom_client=shared.google_classroom_client
    )
    student = providers.Container(
        StudentContainer,
        google_workspace_client=shared.google_workspace_client
    )
