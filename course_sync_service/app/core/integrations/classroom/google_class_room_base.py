import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class GoogleClassroomAPIException(APIException):
    status_code = 400
    default_detail = "Error en la API de Google Classroom"
    default_code = "google_classroom_error"


class GoogleClassroomBase:
    """Base para servicios de Google Classroom"""

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self._service = None
    
    @property
    def service(self):
        """Crea el servicio solo una vez (lazy loading)"""
        if not self._service:
            logger.debug("Construyendo servicio base de Google Classroom")
            self._service = build("classroom", "v1", credentials=self.credentials)
        return self._service

    def handle_error(self, error: HttpError, action: str):
        logger.error(f"✗ Error en {action}: {error.resp.status} - {error.reason}")
        logger.debug(f"Detalles: {error.content}")

        raise GoogleClassroomAPIException(
            detail=f"Error al {action}: {error.reason}",
            code=f"{action}_{error.resp.status}"
        )
