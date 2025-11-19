import logging
from typing import Dict, Any, List
from googleapiclient.errors import HttpError

from course_sync_service.app.core.integrations.classroom.google_class_room_base import (
    GoogleClassroomBase
)

logger = logging.getLogger(__name__)


class GoogleClassroomClient(GoogleClassroomBase):

    def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Intentando crear curso: {course_data.get('name', 'Sin nombre')}")
        try:
            return self.service.courses().create(body=course_data).execute()
        except HttpError as error:
            self.handle_error(error, "crear curso")

    def get_courses(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        logger.info(f"Obteniendo cursos con filtros: {filters}")

        try:
            params = filters or {}
            courses = []
            page_token = None

            while True:
                if page_token:
                    params["pageToken"] = page_token

                response = self.service.courses().list(**params).execute()
                courses.extend(response.get("courses", []))
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            return courses

        except HttpError as error:
            self.handle_error(error, "obtener cursos")

    def get_course(self, course_id: str) -> Dict[str, Any]:
        logger.info(f"Obteniendo curso {course_id}")

        try:
            return self.service.courses().get(id=course_id).execute()
        except HttpError as error:
            self.handle_error(error, "obtener curso")

    def get_all_courses(self) -> List[Dict[str, Any]]:
        logger.info("Obteniendo todos los cursos")

        try:
            courses = []
            page_token = None

            while True:
                response = self.service.courses().list(pageToken=page_token).execute()
                courses.extend(response.get("courses", []))
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            return courses

        except HttpError as error:
            self.handle_error(error, "obtener todos los cursos")

    def update_course(self, course_id: str, course_data: Dict[str, Any]):
        logger.info(f"Actualizando curso {course_id}")

        try:
            update_mask = ",".join(course_data.keys())
            return self.service.courses().update(
                id=course_id,
                updateMask=update_mask,
                body=course_data
            ).execute()
        except HttpError as error:
            self.handle_error(error, "actualizar curso")

    def delete_course(self, course_id: str) -> bool:
        logger.info(f"Eliminando curso {course_id}")

        try:
            self.service.courses().delete(id=course_id).execute()
            return True

        except HttpError as error:
            # Caso especial: no se puede eliminar → archivar
            if error.resp.status == 400 and "Precondition check failed" in str(error):
                try:
                    self.service.courses().patch(
                        id=course_id,
                        updateMask="courseState",
                        body={"courseState": "ARCHIVED"}
                    ).execute()
                    return True
                except HttpError as error2:
                    self.handle_error(error2, "archivar curso")

            self.handle_error(error, "eliminar curso")
