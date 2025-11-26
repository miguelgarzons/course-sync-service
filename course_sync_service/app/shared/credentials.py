# course_sync_service/app/shared/container.py
from dependency_injector import containers, providers
from google.oauth2.credentials import Credentials
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
import os


class SharedContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias compartidas entre módulos."""
    
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