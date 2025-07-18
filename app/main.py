from loguru import logger
from fastapi import FastAPI, File, UploadFile

from app.services.doctr import DocTRService

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.doctr_service = DocTRService()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/predict")
async def ocr(file: UploadFile = File(...)):
    img_bytes = await file.read()
    predictions = app.state.doctr_service.predict(img_bytes)
    return predictions