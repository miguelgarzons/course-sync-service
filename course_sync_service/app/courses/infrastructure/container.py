# course_sync_service/app/courses/infrastructure/container.py
from dependency_injector import containers, providers
from course_sync_service.app.courses.application.use_cases.crear_curso import CrearCurso
from course_sync_service.app.courses.application.use_cases.obtener_cursos import ObtenerCursos
from course_sync_service.app.courses.application.use_cases.actualizar_curso import ActualizarCurso
from course_sync_service.app.courses.application.use_cases.eliminar_curso import EliminarCurso


class CourseContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo Courses."""
    
    config = providers.Configuration()
    
    # Inyección del cliente compartido desde el contenedor padre
    google_classroom_client = providers.Dependency()
    
    create = providers.Factory(
        CrearCurso,
        google_classroom_client=google_classroom_client
    )
    
    list = providers.Factory(
        ObtenerCursos,
        google_classroom_client=google_classroom_client
    )
    
    update = providers.Factory(
        ActualizarCurso,
        google_classroom_client=google_classroom_client
    )
    
    delete = providers.Factory(
        EliminarCurso,
        google_classroom_client=google_classroom_client
    )