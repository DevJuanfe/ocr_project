from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.ocr_engine import OCREngine
from app.core.schemas import OCRResponse
from typing import Dict, Any
import tempfile
import os

router = APIRouter()
ocr = OCREngine()

@router.post("/process", response_model=OCRResponse)
async def process_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Endpoint optimizado para consumo desde .NET"""
    try:
        # Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Procesar documento
        result = ocr.process_document(tmp_path)
        
        # Limpieza
        os.unlink(tmp_path)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["fields"]["error"])
        
        return result
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento: {str(e)}")
