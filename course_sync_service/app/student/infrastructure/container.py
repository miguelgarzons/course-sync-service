# course_sync_service/app/courses/infrastructure/container.py
from dependency_injector import containers, providers
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from google.oauth2.credentials import Credentials
import os

from course_sync_service.app.courses.application.use_cases.crear_curso import CrearCurso
from course_sync_service.app.courses.application.use_cases.obtener_cursos import ObtenerCursos
from course_sync_service.app.courses.application.use_cases.actualizar_curso import ActualizarCurso
from course_sync_service.app.courses.application.use_cases.eliminar_curso import EliminarCurso


class CourseContainer(containers.DeclarativeContainer):
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