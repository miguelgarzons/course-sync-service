from enum import Enum
from app.Biblioteca.application.schemas.schemas import FormularioRecursos
import typing
from datetime import date



class FormularioRecursosMapper:
    
    @staticmethod
    def to_etiquetas(data: dict) -> dict:
        """
        Convierte del formato frontend (Documento 3) al formato BD (Documento 1).
        
        Transforma:
        - recursos_bibliograficos (frontend) → listadolibros (BD)
        - proyeccion_financiera (frontend) → proyección_financiera (BD)
        
        Args:
            data: JSON del frontend con estructura form.fields[]
            
        Returns:
            dict: Estructura {metadata: {...}, variables: {...}}
        """
        form_data = data.get("form", data)
        
        # Extraer campos del array fields[] a un diccionario
        fields_dict = {}
        if "fields" in form_data:
            for field in form_data.get("fields", []):
                label = field.get("label")
                value = field.get("value")
                if label and value is not None:
                    fields_dict[label] = value
        else:
            fields_dict = data
        
        # Validar con Pydantic
        formulario = FormularioRecursos.model_validate(fields_dict)
        
        # Construir variables para BD
        variables_dict = {
            "busqueda_programa": formulario.busqueda_programa,
            "nivel": formulario.nivel,
            "ciclo": formulario.ciclo,
            "nombre_programa": formulario.nombre_programa,
        }
        
        # Transformar recursos_bibliograficos (frontend) → listadolibros (BD)
        if formulario.recursos_bibliograficos_frontend:
            variables_dict["listadolibros"] = [
                {
                    "item": str(item.get("item", "")),
                    "año_libro": str(item.get("año", "")),
                    "nombre_autor": item.get("autores", ""),
                    "nombre_libro": item.get("titulo", ""),
                    "formato_libro": item.get("formato", "")
                }
                for item in formulario.recursos_bibliograficos_frontend
            ]
        
        # Agregar nombre_de_programa (para BD)
        variables_dict["nombre_de_programa"] = formulario.nombre_programa
        
        # Transformar proyeccion_financiera (frontend) → proyección_financiera (BD)
        if formulario.proyeccion_financiera_frontend:
            # Agrupar por formato/categoría si existe esa lógica
            # Por ahora, creamos una entrada genérica
            variables_dict["proyección_financiera"] = []
            
            # Crear estructura con períodos dinámicos
            periodos_dict = {}
            for idx, item in enumerate(formulario.proyeccion_financiera_frontend, 1):
                periodos_dict[f"periodo_{idx}finan"] = f"${item.get('monto', 0):,}"
            
            periodos_dict["Formato_proyeccionfinan"] = "Total inversión"
            variables_dict["proyección_financiera"].append(periodos_dict)
        
        # Agregar campos opcionales si existen
        if formulario.enlace_inventario:
            variables_dict["enlace_inventario"] = formulario.enlace_inventario
        
        if formulario.enlace_proyeccion_financiera:
            variables_dict["enlace_proyeccion_financiera"] = formulario.enlace_proyeccion_financiera
        
        # Mantener campos de BD si vienen directamente
        if formulario.inventario_software:
            variables_dict["inventario_software"] = formulario.inventario_software
        
        if formulario.inventario_laboratorio:
            variables_dict["inventario_laboratorio"] = formulario.inventario_laboratorio
        
        if formulario.recursos_bibliograficos:
            variables_dict["recursos_bibliograficos"] = formulario.recursos_bibliograficos
        
        return {
            "metadata": {
                "title": form_data.get("title", "Formulario Programa Académico"),
                "slug": form_data.get("slug", "formulario-programa-academico")
            },
            "variables": variables_dict
        }
    
    @staticmethod
    def from_etiquetas(etiquetas: dict) -> dict:
        """
        Convierte del formato BD (Documento 1) al formato frontend (Documento 3).
        
        Transforma:
        - listadolibros (BD) → recursos_bibliograficos (frontend)
        - proyección_financiera (BD) → proyeccion_financiera (frontend)
        
        Args:
            etiquetas: Estructura {metadata: {...}, variables: {...}}
            
        Returns:
            dict: JSON para el frontend con estructura form.fields[]
        """
        variables = etiquetas.get("variables", {})
        metadata = etiquetas.get("metadata", {})
        
        fields = []
        
        # Campos básicos
        campos_basicos = [
            ("busqueda_programa", "Búsqueda programa académico", "number"),
            ("nivel", "Nivel", "select"),
            ("ciclo", "Ciclo", "select"),
            ("nombre_programa", "Nombre del programa del nivel técnico profesional", "text"),
        ]
        
        for name, label, field_type in campos_basicos:
            if name in variables:
                field_dict = {
                    "name": name,
                    "label": label,
                    "type": field_type,
                    "value": variables[name]
                }
                
                # Agregar options para selects
                if field_type == "select":
                    if name == "nivel":
                        field_dict["options"] = ["Pregrado", "Posgrado"]
                    elif name == "ciclo":
                        field_dict["options"] = ["Técnico Profesional", "Tecnológico", "Profesional Universitario"]
                
                fields.append(field_dict)
        
        # Transformar listadolibros (BD) → recursos_bibliograficos (frontend)
        if "listadolibros" in variables:
            recursos = [
                {
                    "item": int(libro.get("item", 0)),
                    "titulo": libro.get("nombre_libro", ""),
                    "autores": libro.get("nombre_autor", ""),
                    "año": int(libro.get("año_libro", 0)),
                    "formato": libro.get("formato_libro", ""),
                    "enlace": variables.get("enlace_inventario", "")
                }
                for libro in variables["listadolibros"]
            ]
            
            fields.append({
                "name": "recursos_bibliograficos",
                "label": "Recursos bibliográficos del programa",
                "type": "repeat_group",
                "value": recursos
            })
        
        # Agregar enlace_inventario
        if "enlace_inventario" in variables:
            fields.append({
                "name": "enlace_inventario",
                "label": "Enlace Inventario de recursos académicos al servicio del programa",
                "type": "url",
                "value": variables["enlace_inventario"]
            })
        
        # Transformar proyección_financiera (BD) → proyeccion_financiera (frontend)
        if "proyección_financiera" in variables:
            # Encontrar el registro de "Total inversión" o el primero disponible
            total_inversion = None
            for item in variables["proyección_financiera"]:
                if item.get("Formato_proyeccionfinan") == "Total inversión":
                    total_inversion = item
                    break
            
            if not total_inversion and variables["proyección_financiera"]:
                total_inversion = variables["proyección_financiera"][0]
            
            if total_inversion:
                # Extraer períodos dinámicamente
                proyecciones = []
                periodo_num = 1
                base_year = 2025
                
                while f"periodo_{periodo_num}finan" in total_inversion:
                    monto_str = total_inversion[f"periodo_{periodo_num}finan"]
                    # Limpiar formato: "$3.000.000" → 3000000
                    monto = int(monto_str.replace("$", "").replace(".", "").replace(",", ""))
                    
                    proyecciones.append({
                        "año": base_year + periodo_num - 1,
                        "monto": monto
                    })
                    periodo_num += 1
                
                fields.append({
                    "name": "proyeccion_financiera",
                    "label": "Proyección financiera del programa",
                    "type": "repeat_group",
                    "value": proyecciones
                })
        
        # Agregar enlace_proyeccion_financiera
        if "enlace_proyeccion_financiera" in variables:
            fields.append({
                "name": "enlace_proyeccion_financiera",
                "label": "Enlace Proyección Financiera",
                "type": "url",
                "value": variables["enlace_proyeccion_financiera"]
            })
        
        return {
            "form": {
                "title": metadata.get("title", "Formulario Programa Académico"),
                "slug": metadata.get("slug", "formulario-programa-academico"),
                "fields": fields
            }
        }

