from typing import Any, Dict, List

from pydantic import BaseModel


class MLResponse(BaseModel):
    predictions: List[Dict[str, Any]]