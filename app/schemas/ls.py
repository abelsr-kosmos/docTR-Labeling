from pydantic import BaseModel

class LabelStudioData(BaseModel):
    ocr: str

class LabelStudioTask(BaseModel):
    id: int
    data: LabelStudioData
    
    class Config:
        extra = "forbid"

class LabelStudioRequest(BaseModel):
    tasks: list[LabelStudioTask]