# infrastructure/out/google_classroom_client.py
from typing import Dict, Any, List
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

class GoogleClassroomClient:
    """Cliente para interactuar con Google Classroom API"""
    
    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self._service = None
    
    @property
    def service(self):
        if not self._service:
            self._service = build('classroom', 'v1', credentials=self.credentials)
        return self._service
    
    def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un curso en Google Classroom"""
        try:
            course = self.service.courses().create(body=course_data).execute()
            logger.info(f"Curso creado: {course.get('id')}")
            return course
        except HttpError as error:
            logger.error(f"Error al crear curso: {error}")
            raise Exception(f"Error al crear curso: {error}")
    
    def get_courses(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtiene lista de cursos"""
        try:
            params = filters or {}
            courses = []
            page_token = None
            
            while True:
                if page_token:
                    params['pageToken'] = page_token
                
                response = self.service.courses().list(**params).execute()
                courses.extend(response.get('courses', []))
                
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
            
            return courses
        except HttpError as error:
            logger.error(f"Error al obtener cursos: {error}")
            raise Exception(f"Error al obtener cursos: {error}")
    
    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Obtiene un curso por ID"""
        try:
            return self.service.courses().get(id=course_id).execute()
        except HttpError as error:
            logger.error(f"Error al obtener curso {course_id}: {error}")
            raise Exception(f"Error al obtener curso: {error}")
    
    def update_course(self, course_id: str, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un curso"""
        try:
            course_data['id'] = course_id
            update_mask = ','.join([k for k in course_data.keys() if k != 'id'])
            
            course = self.service.courses().update(
                id=course_id,
                updateMask=update_mask,
                body=course_data
            ).execute()
            
            logger.info(f"Curso actualizado: {course_id}")
            return course
        except HttpError as error:
            logger.error(f"Error al actualizar curso: {error}")
            raise Exception(f"Error al actualizar curso: {error}")
    
    def delete_course(self, course_id: str) -> bool:
        try:
            self.service.courses().delete(id=course_id).execute()
            return True

        except HttpError as error:
            print(f"Error eliminando curso: {error}")
            if error.resp.status == 400 and "Precondition check failed" in str(error):
                try:
                    print("No se puede eliminar. Archivando…")

                    self.service.courses().patch(
                        id=course_id,
                        updateMask="courseState",            # ← OBLIGATORIO
                        body={"courseState": "ARCHIVED"}     # ← Nuevo estado
                    ).execute()

                    return True

                except HttpError as error2:
                    print(f"Error archivando curso: {error2}")
                    return False

            return False
