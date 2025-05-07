from pydantic import BaseModel
from typing import Dict, Any

class OCRResponse(BaseModel):
    type: str
    fields: Dict[str, Any]
    raw_text: str
    status: str
