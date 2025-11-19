# course_sync_service/app/shared/container.py
from dependency_injector import containers, providers
from course_sync_service.app.courses.infrastructure.container import CourseContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Contenedor global de la aplicación."""
    config = providers.Configuration()
    course = providers.Container(CourseContainer)