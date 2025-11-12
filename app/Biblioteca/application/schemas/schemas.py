
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Any, Dict
import typing
from datetime import date


# ===== SCHEMAS PARA BD (Documento 1) =====

class FormatoLibro(str, Enum):
    FISICO = "Físico"
    DIGITAL = "Digital"


class Libro(BaseModel):
    """Modelo para listadolibros en BD"""
    item: str = Field(alias="item")
    año_libro: str = Field(alias="año_libro")
    nombre_autor: str = Field(alias="nombre_autor")
    nombre_libro: str = Field(alias="nombre_libro")
    formato_libro: str = Field(alias="formato_libro")
    
    model_config = {"populate_by_name": True}


class Software(BaseModel):
    """Modelo para inventario_software en BD"""
    asignatura_software: str = Field(alias="asignatura_software")
    descr_educativosoft: str = Field(alias="descr_educativosoft")
    nombre_medioseducativossoft: str = Field(alias="nombre_medioseducativossoft")
    
    model_config = {"populate_by_name": True}


class Laboratorio(BaseModel):
    """Modelo para inventario_laboratorio en BD"""
    descr_educativolabora: str = Field(alias="descr_educativolabora")
    asignatura_laboratorio: str = Field(alias="asignatura_laboratorio")
    nombre_medioseducativoslabora: str = Field(alias="nombre_medioseducativoslabora")
    
    model_config = {"populate_by_name": True}


class ProyeccionFinanciera(BaseModel):
    """
    Modelo dinámico para proyección_financiera en BD.
    Acepta cualquier número de períodos (periodo_1finan, periodo_2finan, ..., periodo_Nfinan)
    """
    Formato_proyeccionfinan: str = Field(alias="Formato_proyeccionfinan")
    
    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }
    
    def __init__(self, **data):
        super().__init__(**data)
        for key, value in data.items():
            if key.startswith('periodo_') and key.endswith('finan'):
                setattr(self, key, value)


class RecursoBibliografico(BaseModel):
    """
    Modelo dinámico para recursos_bibliograficos en BD.
    Acepta cualquier número de períodos (periodo_1, periodo_2, ..., periodo_N)
    """
    descr_formatobibli: str = Field(alias="descr_formatobibli")
    enlace_bibliografico: str = Field(alias="enlace_bibliografico")
    
    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }
    
    def __init__(self, **data):
        super().__init__(**data)
        for key, value in data.items():
            if key.startswith('periodo_') and not key.endswith('finan'):
                setattr(self, key, value)


# ===== SCHEMAS PARA FRONTEND (Documento 3) =====

class RecursoBibliograficoFrontend(BaseModel):
    """Modelo para recursos_bibliograficos del frontend"""
    item: int
    titulo: str
    autores: str
    año: int = Field(alias="año")
    formato: str
    enlace: str
    
    model_config = {"populate_by_name": True}


class ProyeccionFinancieraFrontend(BaseModel):
    """Modelo para proyeccion_financiera del frontend"""
    año: int = Field(alias="año")
    monto: int
    
    model_config = {"populate_by_name": True}


# ===== SCHEMA PRINCIPAL =====

class FormularioRecursos(BaseModel):
    busqueda_programa: int = Field(alias="Búsqueda programa académico")
    nivel: str = Field(alias="Nivel")
    ciclo: str = Field(alias="Ciclo")
    nombre_programa: str = Field(alias="Nombre del programa del nivel técnico profesional")
    
    # Campos del frontend (Documento 3)
    recursos_bibliograficos_frontend: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        alias="Recursos bibliográficos del programa"
    )
    enlace_inventario: Optional[str] = Field(
        default=None,
        alias="Enlace Inventario de recursos académicos al servicio del programa"
    )
    proyeccion_financiera_frontend: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        alias="Proyección financiera del programa"
    )
    enlace_proyeccion_financiera: Optional[str] = Field(
        default=None,
        alias="Enlace Proyección Financiera"
    )
    
    # Campos de la BD (Documento 1) - opcionales porque pueden venir de frontend
    listadolibros: Optional[List[Dict[str, Any]]] = Field(default=None, alias="listadolibros")
    nombre_de_programa: Optional[str] = Field(default=None, alias="nombre_de_programa")
    inventario_software: Optional[List[Dict[str, Any]]] = Field(default=None, alias="inventario_software")
    inventario_laboratorio: Optional[List[Dict[str, Any]]] = Field(default=None, alias="inventario_laboratorio")
    proyección_financiera: Optional[List[Dict[str, Any]]] = Field(default=None, alias="proyección_financiera")
    recursos_bibliograficos: Optional[List[Dict[str, Any]]] = Field(default=None, alias="recursos_bibliograficos")

    model_config = {"populate_by_name": True, "extra": "allow"}
