from dependency_injector import containers, providers
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from google.oauth2.credentials import Credentials
import os

from course_sync_service.app.student.application.use_cases.matricular_estudiante import MatricularEstudiante
from course_sync_service.app.student.application.use_cases.obtener_estudiante import ObtenerEstudiante
from course_sync_service.app.student.application.use_cases.actualizar_estudiante import ActualizarEstudiante
from course_sync_service.app.student.application.use_cases.eliminar_estudiante import EliminarEstudiante


class StudentContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo Courses."""
    

    config = providers.Configuration()
    google_credentials = providers.Singleton(
        Credentials,
        token=os.getenv('GOOGLE_ACCESS_TOKEN'),
        refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/classroom.courses']
    )
    
    google_classroom_client = providers.Singleton(
        GoogleClassroomClient,
        credentials=google_credentials
    )
    
    create = providers.Factory(
        MatricularEstudiante,
        google_classroom_client=google_classroom_client
    )
    
    list = providers.Factory(
        ObtenerEstudiante,
        google_classroom_client=google_classroom_client
    )
    
    update = providers.Factory(
        EliminarEstudiante,
        google_classroom_client=google_classroom_client
    )
    
    delete = providers.Factory(
        EliminarEstudiante,
        google_classroom_client=google_classroom_client
    )