from drf_yasg import openapi

formulario_posgrado_example = {
    "form": {
        "title": "Formulario Posgrados Especialización",
        "slug": "formulario-posgrados-especializacion",
        "fields": [
            {"name": "proceso", "label": "Proceso", "type": "text", "options": [], "value": "a"},
            {"name": "busqueda_snies", "label": "Búsqueda de SNIES", "type": "number", "options": [], "value": 2123},
            {"name": "nivel", "label": "Nivel", "type": "select", "options": ["Pregrado", "Posgrado"], "value": "Posgrado"},
            {"name": "ciclo", "label": "Ciclo", "type": "select", "options": ["Especialización", "Maestría", "Doctorado"], "value": "Especialización"},
            {"name": "nombre_de_programa", "label": "Nombre de la Especialización", "type": "text", "options": [], "value": "11"},
            {"name": "tipo_registro", "label": "Tipo de Registro", "type": "select", "options": ["Registro Calificado", "Acreditación"], "value": "Registro Calificado"},
            {"name": "modalidad_programa", "label": "Modalidad", "type": "select", "options": ["Presencial", "Virtual", "Mixta"], "value": "Presencial"},
            {"name": "regional_programa", "label": "Regional(es)", "type": "text", "options": [], "value": "a"},
            {"name": "título_especialista", "label": "Título de la Especialización a Otorgar", "type": "text", "options": [], "value": "1212"},
            {"name": "perfil_especialista", "label": "Perfil de la Especialización", "type": "textarea", "options": [], "value": "wkjfdf"},
            {"name": "duracion_programa", "label": "Duración de la Especialización (meses)", "type": "number", "options": [], "value": 12233},
            {"name": "periodicidad_programa", "label": "Periodicidad de Admisión", "type": "select", "options": ["Semestral", "Anual", "Trimestral"], "value": "Semestral"},
            {"name": "admitidos_programa", "label": "Cantidad de Estudiantes 1er Semestre", "type": "number", "options": [], "value": 22},
            {"name": "viabilidad_financiera", "label": "Viabilidad Financiera", "type": "boolean", "options": [], "value": True},
            {"name": "fecha", "label": "Fecha de Creación", "type": "date", "options": [], "value": "2025-10-17"},
            {"name": "escuela_datos", "label": "Escuela", "type": "text", "options": [], "value": "Ingeniería"},
            {"name": "correo_director", "label": "Correo del Director de Escuela", "type": "email", "options": [], "value": "dfjdsf@prueba.com"},
            {"name": "campo_amplio", "label": "Campo Amplio", "type": "select", "options": [
                "Ingeniería, Industria y Construcción", "Ciencias Sociales", "Educación", "Salud", "Artes"], "value": "Ingeniería, Industria y Construcción"},
            {"name": "campo_especifico", "label": "Campo Específico", "type": "select", "options": [
                "Arquitectura y Construcción", "Ingeniería Mecánica", "Tecnologías de la Información"], "value": "Arquitectura y Construcción"},
            {"name": "campo_detallado", "label": "Campo Detallado", "type": "select", "options": [
                "Construcción e Ingeniería Civil", "Diseño Arquitectónico", "Gestión de Proyectos"], "value": "Construcción e Ingeniería Civil"},
            {"name": "área_de_conocimiento", "label": "Área del Conocimiento", "type": "select", "options": [
                "Bellas Artes", "Ciencias Sociales", "Ciencias Naturales", "Ingeniería"], "value": "Bellas Artes"},
            {"name": "nucleo_basico", "label": "Núcleo Básico del Conocimiento", "type": "select", "options": [
                "Diseño", "Arquitectura", "Ingeniería Civil"], "value": "Diseño"},
            {"name": "programas_similares", "label": "Programas Similares", "type": "multiselect", "options": [
                "Administración", "Administración en Salud", "Contaduría", "Finanzas"], "value": ["Administración", "Administración en Salud"]}
        ]
    }
}

# Documentación Swagger (drf_yasg)

crear_acta_doc = {
    "operation_summary": "Crear un programa de posgrado",
    "operation_description": "Registrar un programa de posgrado usando el formulario completo.",
    "tags": ["Biblioteca"],
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        example=formulario_posgrado_example
    ),
    "responses": {
        201: openapi.Response(
            description="Programa creado exitosamente",
        ),
        400: openapi.Response(description="Error de validación")
    }
}

obtener_acta_doc = {
    "operation_summary": "Obtener un programa de posgrado",
    "operation_description": "Devuelve el programa de posgrado completo en la misma estructura JSON que se envía en el formulario.",
    "tags": ["Biblioteca"],
    "responses": {
        200: openapi.Response(
            description="Programa obtenido exitosamente",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                example=formulario_posgrado_example
            )
        ),
        404: openapi.Response(
            description="Programa no encontrado",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                example={"error": "Programa no encontrado"}
            )
        )
    }
}
