from pydantic import BaseModel

from app.schemas.annotation import AnnotationValue


class PredictionItem(BaseModel):
    from_name: str
    to_name: str
    type: str
    value: AnnotationValue