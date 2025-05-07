import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import Dict, Any, List
from pathlib import Path

class OCREngine:
    def __init__(self):
        self.ocr = PaddleOCR(
            lang='es',
            use_angle_cls=True,
            show_log=False
        )
    
    def process_document(self, image_path: str) -> Dict[str, Any]:
        """Procesa cualquier documento y devuelve datos estructurados"""
        try:
            img = self._load_image(image_path)
            result = self.ocr.ocr(img, cls=True)
            text_lines = [line[1][0] for line in result[0]] if result else []
            
            return {
                "type": self._classify_document(text_lines),
                "fields": self._extract_fields(text_lines),
                "raw_text": "\n".join(text_lines),
                "status": "success"
            }
        except Exception as e:
            return {
                "type": "error",
                "fields": {"error": str(e)},
                "raw_text": "",
                "status": "error"
            }
    
    def _load_image(self, image_path: str):
        """Carga imágenes desde path o bytes (compatible con API)"""
        if isinstance(image_path, str) and Path(image_path).exists():
            return cv2.imread(image_path)
        elif isinstance(image_path, bytes):
            return cv2.imdecode(np.frombuffer(image_path, np.uint8), -1)
        else:
            raise ValueError("Formato de imagen no soportado")

    def _classify_document(self, text_lines: List[str]) -> str:
        """Clasificación mejorada basada en tus ejemplos"""
        full_text = " ".join(text_lines).lower()
        
        if any(kw in full_text for kw in ["cédula", "identidad"]):
            return "cedula"
        elif any(kw in full_text for kw in ["poder", "apoderado"]):
            return "poder"
        elif any(kw in full_text for kw in ["factura", "nit", "valor total"]):
            return "factura"
        return "desconocido"

    def _extract_fields(self, text_lines: List[str]) -> Dict[str, str]:
        """Extracción combinada de tus ejemplos y requerimientos"""
        doc_type = self._classify_document(text_lines)
        fields = {}
        
        for line in text_lines:
            lower = line.lower()
            
            # Extracción para cédulas
            if doc_type == "cedula":
                if "nombre" in lower:
                    fields["nombre"] = line.split(":")[-1].strip()
                elif "número" in lower or "identidad" in lower:
                    fields["identificacion"] = line.split(":")[-1].strip()
            
            # Extracción para facturas
            elif doc_type == "factura":
                if "nit" in lower:
                    fields["nit"] = line.split(":")[-1].strip()
                elif "total" in lower:
                    fields["total"] = line.split("$")[-1].strip()
            
            # Extracción para poderes
            elif doc_type == "poder":
                if "apoderado" in lower:
                    fields["apoderado"] = line.split(":")[-1].strip()
                elif "beneficiario" in lower:
                    fields["beneficiario"] = line.split(":")[-1].strip()
        
        return fields or {"info": "No se detectaron campos"}
