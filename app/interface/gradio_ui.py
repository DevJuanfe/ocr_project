from fastapi import FastAPI
from app.core.ocr_engine import OCREngine
import gradio as gr
import tempfile
import os

def mount_gradio_app(fastapi_app: FastAPI):
    ocr = OCREngine()

    def process(file):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            
            result = ocr.process_document(tmp_path)
            os.unlink(tmp_path)
            
            return [
                result["type"],
                "\n".join(f"{k}: {v}" for k, v in result["fields"].items()),
                result["raw_text"]
            ]
        except Exception as e:
            return ["Error", str(e), ""]

    with gr.Blocks() as demo:
        gr.Markdown("## Procesador de Documentos")
        with gr.Row():
            inputs = gr.File(label="Sube tu documento")
            outputs = [
                gr.Textbox(label="Tipo de Documento"),
                gr.Textbox(label="Campos Extraídos"),
                gr.Textbox(label="Texto Completo", lines=10)
            ]
        btn = gr.Button("Procesar")
        btn.click(process, inputs=inputs, outputs=outputs)

    return gr.mount_gradio_app(fastapi_app, demo, path="/gradio")
