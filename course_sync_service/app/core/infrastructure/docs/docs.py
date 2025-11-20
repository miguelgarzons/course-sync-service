from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter

from ..out.curso_get_response_serializer import CursoGetResponseSerializer
from ..out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from ..out.curso_create_response_serializer import CursoGoogleResponseSerializer
from drf_spectacular.types import OpenApiTypes

def crear_estudiantes_schema():
    return extend_schema(
        operation_id="matricular_estudiantes",
        summary="Matricula estudiantes classroom",
        description="Matricula estudiantes usando el formato de query params de Moodle Web Services.",
        tags=["Estudiantes"],
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
            200: OpenApiResponse(response=CursoGoogleResponseSerializer, description="Programa obtenido exitosamente"),
            404: OpenApiResponse(response=CursoGetResponseSerializer, description="Programa no encontrado"),
        }
    )

def obtener_estudiantes_schema():
    return extend_schema(
        operation_id="obtener_estudiante",
        summary="Obtener un estudiante de classroom",
        description="Devuelve estudiantes usando el formato de query params de Moodle Web Services.",
        tags=["Estudiantes"],
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
            200: OpenApiResponse(response=CursoGetResponseSerializer, description="Programa obtenido exitosamente"),
            404: OpenApiResponse(response=CursoGetResponseSerializer, description="Programa no encontrado"),
        }
    )

def eliminar_estudiantes_schema():
    return extend_schema(
        operation_id="eliminar_estudiante",
        summary="Eliminar un estudiante classroom",
        description="elimina un estudiante usando el formato de query params de Moodle Web Services.",
        tags=["Estudiantes"],
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
            200: OpenApiResponse(response=CursoDeleteResponseSerializer, description="Programa obtenido exitosamente"),
            404: OpenApiResponse(response=CursoGetResponseSerializer, description="Programa no encontrado"),
        }
    )


def actualizar_estudiantes_schema():
    return extend_schema(
        operation_id="Actualizar_estudiante",
        summary="Actualiza un estudiante en classroom",
        description=(
            "Actualiza un estudiante usando el formato de query params del Moodle Web Service "
            "`core_course_update_courses`. Los parámetros deben enviarse siguiendo la convención:\n"
            "`courses[0][campo] = valor`."
        ),
        tags=["Estudiantes"],
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
                response=CursoGetResponseSerializer,
                description="Curso actualizado exitosamente"
            ),
            404: OpenApiResponse(
                response=CursoGetResponseSerializer,
                description="Curso no encontrado"
            ),
        }
    )

