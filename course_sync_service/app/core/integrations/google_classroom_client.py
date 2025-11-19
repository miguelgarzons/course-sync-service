from typing import Dict, Any, List
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)


class GoogleClassroomAPIException(APIException):
    """Excepción personalizada para errores de Google Classroom"""
    status_code = 400
    default_detail = 'Error en la API de Google Classroom'
    default_code = 'google_classroom_error'


class GoogleClassroomClient:
    """Cliente para interactuar con Google Classroom API"""
    
    def __init__(self, credentials: Credentials):
        logger.info("Inicializando cliente de Google Classroom")
        self.credentials = credentials
        self._service = None
    
    @property
    def service(self):
        if not self._service:
            logger.debug("Construyendo servicio de Google Classroom")
            self._service = build('classroom', 'v1', credentials=self.credentials)
        return self._service
    
    def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un curso en Google Classroom"""
        logger.info(f"Intentando crear curso: {course_data.get('name', 'Sin nombre')}")
        try:
            course = self.service.courses().create(body=course_data).execute()
            logger.info(f"✓ Curso creado exitosamente - ID: {course.get('id')}")
            return course
        except HttpError as error:
            logger.error(f"✗ Error al crear curso: {error.resp.status} - {error.reason}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudo crear el curso: {error.reason}",
                code=f"create_course_{error.resp.status}"
            )
    
    def get_courses(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtiene lista de cursos"""
        logger.info(f"Obteniendo lista de cursos con filtros: {filters}")
        try:
            params = filters or {}
            courses = []
            page_token = None
            page_count = 0
            
            while True:
                page_count += 1
                if page_token:
                    params['pageToken'] = page_token
                
                logger.debug(f"Solicitando página {page_count} de cursos")
                response = self.service.courses().list(**params).execute()
                page_courses = response.get('courses', [])
                courses.extend(page_courses)
                logger.debug(f"Obtenidos {len(page_courses)} cursos en página {page_count}")
                
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
            
            logger.info(f"✓ Total de cursos obtenidos: {len(courses)}")
            return courses
        except HttpError as error:
            logger.error(f"✗ Error al obtener cursos: {error.resp.status} - {error.reason}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudieron obtener los cursos: {error.reason}",
                code=f"get_courses_{error.resp.status}"
            )
    
    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Obtiene un curso por ID"""
        logger.info(f"Obteniendo curso con ID: {course_id}")
        try:
            course = self.service.courses().get(id=course_id).execute()
            logger.info(f"✓ Curso obtenido: {course.get('name', 'Sin nombre')}")
            return course
        except HttpError as error:
            logger.error(f"✗ Error al obtener curso {course_id}: {error.resp.status} - {error.reason}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudo obtener el curso: {error.reason}",
                code=f"get_course_{error.resp.status}"
            )
        
    def get_all_courses(self) -> List[Dict[str, Any]]:
        """Obtiene todos los cursos de Google Classroom"""
        logger.info("Obteniendo todos los cursos disponibles")
        try:
            courses = []
            page_token = None
            page_count = 0

            while True:
                page_count += 1
                logger.debug(f"Procesando página {page_count}")
                response = self.service.courses().list(pageToken=page_token).execute()

                if "courses" in response:
                    page_courses = response["courses"]
                    courses.extend(page_courses)
                    logger.debug(f"Agregados {len(page_courses)} cursos de página {page_count}")

                page_token = response.get("nextPageToken")
                if not page_token:
                    break

            logger.info(f"✓ Total de cursos obtenidos: {len(courses)}")
            return courses

        except HttpError as error:
            logger.error(f"✗ Error al obtener todos los cursos: {error.resp.status} - {error.reason}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudieron obtener todos los cursos: {error.reason}",
                code=f"get_all_courses_{error.resp.status}"
            )
    
    def update_course(self, course_id: str, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un curso"""
        logger.info(f"Actualizando curso: {course_id}")
        logger.debug(f"Datos a actualizar: {course_data.keys()}")
        try:
            course_data['id'] = course_id
            update_mask = ','.join([k for k in course_data.keys() if k != 'id'])
            logger.debug(f"Update mask: {update_mask}")
            
            course = self.service.courses().update(
                id=course_id,
                updateMask=update_mask,
                body=course_data
            ).execute()
            
            logger.info(f"✓ Curso actualizado exitosamente: {course_id}")
            return course
        except HttpError as error:
            logger.error(f"✗ Error al actualizar curso {course_id}: {error.resp.status} - {error.reason}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudo actualizar el curso: {error.reason}",
                code=f"update_course_{error.resp.status}"
            )
    
    def delete_course(self, course_id: str) -> bool:
        """Elimina o archiva un curso"""
        logger.info(f"Intentando eliminar curso: {course_id}")
        try:
            self.service.courses().delete(id=course_id).execute()
            logger.info(f"✓ Curso eliminado exitosamente: {course_id}")
            return True

        except HttpError as error:
            logger.warning(f"⚠ Error al eliminar curso {course_id}: {error.resp.status} - {error.reason}")
            
            if error.resp.status == 400 and "Precondition check failed" in str(error):
                try:
                    logger.info(f"Intentando archivar curso en lugar de eliminar: {course_id}")
                    
                    self.service.courses().patch(
                        id=course_id,
                        updateMask="courseState",
                        body={"courseState": "ARCHIVED"}
                    ).execute()
                    
                    logger.info(f"✓ Curso archivado exitosamente: {course_id}")
                    return True

                except HttpError as error2:
                    logger.error(f"✗ Error al archivar curso {course_id}: {error2.resp.status} - {error2.reason}")
                    logger.debug(f"Detalles del error: {error2.content}")
                    raise GoogleClassroomAPIException(
                        detail=f"No se pudo eliminar ni archivar el curso: {error2.reason}",
                        code=f"archive_course_{error2.resp.status}"
                    )
            
            logger.error(f"✗ Error no recuperable al eliminar curso {course_id}")
            logger.debug(f"Detalles del error: {error.content}")
            raise GoogleClassroomAPIException(
                detail=f"No se pudo eliminar el curso: {error.reason}",
                code=f"delete_course_{error.resp.status}"
            )