from dependency_injector import containers, providers
from google.oauth2 import service_account
from google.auth import default as google_auth_default
from course_sync_service.app.core.integrations.classroom.google_classroom_courses import GoogleClassroomClient
from course_sync_service.app.core.integrations.google_workspace.google_workspace_users import GoogleWorkspaceUsers
import os


class SharedContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/admin.directory.user",
        "https://www.googleapis.com/auth/admin.directory.user.readonly",
        "https://www.googleapis.com/auth/classroom.courses",
        "https://www.googleapis.com/auth/classroom.rosters",
    ]

    # Detecta si estamos en LOCAL (archivo JSON) o CLOUD RUN (credenciales por defecto)
    def _load_credentials():
        json_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

        if json_path:  
            # ⭐ MODO LOCAL
            return service_account.Credentials.from_service_account_file(
                json_path,
                scopes=SharedContainer.GOOGLE_SCOPES,
            )
        
        # ⭐ MODO CLOUD RUN
        creds, _ = google_auth_default(scopes=SharedContainer.GOOGLE_SCOPES)
        return creds

    google_credentials = providers.Singleton(_load_credentials)

    # Impersonation
    impersonated_credentials = providers.Singleton(
        lambda creds: creds.with_subject(os.getenv("GOOGLE_IMPERSONATE_ADMIN")),
        creds=google_credentials
    )

    google_classroom_client = providers.Singleton(
        GoogleClassroomClient,
        credentials=impersonated_credentials
    )

    google_workspace_client = providers.Singleton(
        GoogleWorkspaceUsers,
        credentials=impersonated_credentials
    )
