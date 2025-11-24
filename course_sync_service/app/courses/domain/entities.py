# app/Acta/domain/entities.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from typing import Optional

@dataclass
class Curso:
    id: Optional[int] = None
    fullname: str = ""
    shortname: str = ""
    categoryid: int = None
    startdate: int = None
    enddate: int = None
    visible: int = None

@dataclass
class CursosAEliminar:
    ids: List[int]


@dataclass
class CursosObtener:
    ids: List[int]