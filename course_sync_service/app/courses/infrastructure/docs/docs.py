from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter

from ..serializers import (
    ActaRetrieveResponseSerializer,
    ErrorResponseSerializer,
)
from drf_spectacular.types import OpenApiTypes

def crear_cursos_schema():
    return extend_schema(
        operation_id="crear_curso",
        summary="Crear un curso classroom",
        description="Crear cursos usando el formato de query params de Moodle Web Services.",
        tags=["Cursos"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Función del web service (ej: core_course_create_courses)",
                required=True
            ),
            OpenApiParameter(
                name="moodlewsrestformat",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Formato de respuesta (json, xml)",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][fullname]",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Nombre completo del curso",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][shortname]",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Nombre corto del curso",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][categoryid]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="ID de la categoría",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][startdate]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Fecha de inicio (timestamp Unix)",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][enddate]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Fecha de fin (timestamp Unix)",
                required=True
            ),
            OpenApiParameter(
                name="courses[0][visible]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Visibilidad del curso (0=oculto, 1=visible)",
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Curso creado exitosamente",
                response={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "data": {"type": "object"},
                        "courses_count": {"type": "integer"}
                    }
                }
            ),
            400: OpenApiResponse(description="Error de validación"),
        }
    )

def obtener_cursos_schema():
    return extend_schema(
        operation_id="obtener_curso",
        summary="Obtener un curso classroom",
        description="Devuelve cursos usando el formato de query params de Moodle Web Services.",
        tags=["Cursos"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Función del web service (ej: core_course_create_courses)",
                required=True
            ),
                      OpenApiParameter(
                name="options[ids][0]",
                type=OpenApiTypes.INT,  # o STR según necesites
                location=OpenApiParameter.QUERY,
                description="Primer ID dentro de options[ids]",
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(response=ActaRetrieveResponseSerializer, description="Programa obtenido exitosamente"),
            404: OpenApiResponse(response=ErrorResponseSerializer, description="Programa no encontrado"),
        }
    )

def eliminar_cursos_schema():
    return extend_schema(
        operation_id="eliminar_curso",
        summary="Eliminar un curso classroom",
        description="elimina un curso usando el formato de query params de Moodle Web Services.",
        tags=["Cursos"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Función del web service (ej: core_course_create_courses)",
                required=True
            ),
                      OpenApiParameter(
                name="options[ids][0]",
                type=OpenApiTypes.INT,  # o STR según necesites
                location=OpenApiParameter.QUERY,
                description="Primer ID dentro de options[ids]",
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(response=ActaRetrieveResponseSerializer, description="Programa obtenido exitosamente"),
            404: OpenApiResponse(response=ErrorResponseSerializer, description="Programa no encontrado"),
        }
    )


def actualizar_cursos_schema():
    return extend_schema(
        operation_id="Actualizar_curso",
        summary="Actualiza un curso en classroom",
        description=(
            "Actualiza un curso usando el formato de query params del Moodle Web Service "
            "`core_course_update_courses`. Los parámetros deben enviarse siguiendo la convención:\n"
            "`courses[0][campo] = valor`."
        ),
        tags=["Cursos"],
        parameters=[

            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True
            ),

            # Función del WS
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Función del WebService (ej: core_course_update_courses)",
                required=True
            ),

            # --- Parámetros de courses[0] ---

            OpenApiParameter(
                name="courses[0][id]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="ID del curso a actualizar",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][fullname]",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Nuevo nombre completo del curso",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][shortname]",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Nuevo shortname del curso",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][categoryid]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Nueva categoría del curso",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][startdate]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Nueva fecha de inicio (timestamp Unix)",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][enddate]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Nueva fecha de finalización (timestamp Unix)",
                required=True
            ),

            OpenApiParameter(
                name="courses[0][visible]",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Visibilidad del curso (0 = oculto, 1 = visible)",
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ActaRetrieveResponseSerializer,
                description="Curso actualizado exitosamente"
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Curso no encontrado"
            ),
        }
    )

