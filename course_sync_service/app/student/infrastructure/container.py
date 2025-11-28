# course_sync_service/app/student/infrastructure/container.py
from dependency_injector import containers, providers
from course_sync_service.app.student.application.use_cases.crear_estudiante import CrearEstudiante
from course_sync_service.app.student.application.use_cases.matricular_estudiante import MatricularEstudiante
from course_sync_service.app.student.application.use_cases.obtener_estudiante import ObtenerEstudiante
from course_sync_service.app.student.application.use_cases.actualizar_estudiante import ActualizarEstudiante
from course_sync_service.app.student.application.use_cases.eliminar_estudiante import EliminarEstudiante


class StudentContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo Student."""
    
    config = providers.Configuration()
    
    google_classroom_client = providers.Dependency()
    google_workspace_client = providers.Dependency()
    
    matricular = providers.Factory(
        MatricularEstudiante,
        google_classroom_client=google_classroom_client
    )

    crear_estudiante = providers.Factory(
        CrearEstudiante,
        google_workspace_client=google_workspace_client
    )
    
