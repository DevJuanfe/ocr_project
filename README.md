Documentación del Proyecto API OCR

 Descripción General
Este proyecto implementa un sistema OCR (Reconocimiento Óptico de Caracteres) con **PaddleOCR**, capaz de:

Procesar imágenes de documentos (cédulas, tirillas, poderes).
Detectar automáticamente el tipo de documento.
Extraer información estructurada (como nombres, cédulas, fechas).
Ofrecer resultados mediante una **API para .NET** o una **interfaz visual Gradio**.

Estructura del Proyecto

```
OCR_PROJECT/
├── app/
│   ├── __init__.py                 # Inicializador del paquete
│   ├── main.py                     # Punto de entrada con FastAPI y rutas
│   ├── api/
│   │   └── endpoints.py            # Endpoints de la API REST para consumo externo (como .NET)
│   ├── interface/
│   │   └── gradio_ui.py            # Interfaz gráfica usando Gradio para pruebas visuales del OCR
│   └── core/
│       ├── ocr_engine.py           # Motor central OCR: preprocesamiento, clasificación, extracción
│       └── schemas.py              # Modelos de datos con Pydantic (entrada/salida de la API)
├── tests/                          # Carpeta opcional para tests con Pytest
├── .venv/                          # Entorno virtual (excluido en control de versiones)
└── requirements.txt                # Dependencias del proyecto
```

Comandos para Ejecutar el Proyecto

1. Instalar dependencias

Python 3.8–3.11 y luego ejecuta:

```bash
python -m venv .venv
.venv\Scripts\activate          # En Windows
# source .venv/bin/activate    # En Linux/Mac

pip install -r requirements.txt
```

---

2. Ejecutar la API con FastAPI + Uvicorn

```bash
# Desde la raíz del proyecto
set PYTHONPATH=.
uvicorn app.main:app --reload
```

La API quedará disponible en:

```
http://127.0.0.1:8000
http://127.0.0.1:8000/docs  ← Documentación Swagger UI
```

---

3. Ejecutar la interfaz Gradio

```bash
python app/interface/gradio_ui.py
```

Esto abre una interfaz visual en el navegador donde puedes subir imágenes y ver resultados.

---

4. Ejecutar pruebas (si existen)

```bash
set PYTHONPATH=.
pytest app/tests -v
```

---

Info adicional
Los modelos OCR se descargan automáticamente al usar PaddleOCR por primera vez.
Se recomienda usar imágenes claras y bien alineadas para mejores resultados, aunque el sistema incluye preprocesamiento y validaciones.
Servicio a producción, usar `gunicorn` o `uvicorn` con `--host 0.0.0.0`.
