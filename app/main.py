from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.interface.gradio_ui import mount_gradio_app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OCR Service API", version="1.0")

# Configuración CORS (para .NET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar componentes
app.include_router(api_router, prefix="/api")
mount_gradio_app(app)
