from typing import List

from pydantic import BaseModel

class AnnotationValue(BaseModel):
    x: float
    y: float
    width: float
    height: float
    rotation: int = 0
    text: List[str] = None
    labels: List[str] = None