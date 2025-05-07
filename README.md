OCR_PROJECT/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada
│   ├── api/
│   │   └── endpoints.py     # API para .NET
│   ├── interface/
│   │   └── gradio_ui.py     # Interfaz visual
│   └── core/
│       ├── ocr_engine.py    # Combina pipeline + ejemplos
│       └── schemas.py       # Modelos Pydantic
├── tests/
├── venv
├── .venv
└── requirements.txt

// cuando no se ejecute con el comando virtualizado, ejecutar como modulo:
python -m uvicorn app.main:app --reload
