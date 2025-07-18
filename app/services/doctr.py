from typing import Any, Dict

from loguru import logger
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


class DocTRService:
    def __init__(self):
        self.model = ocr_predictor(pretrained=True)

    def predict(self, image_bytes: bytes):
        doc = DocumentFile.from_images(image_bytes)
        result = self.model(doc)
        return {
            "predictions": [
                {
                    "result": self.__process_doctr_result(result),
                    "model_version": "1.0.0"
                }
            ]
        }
    
    def __process_doctr_result(self, result: Any) -> Dict:
        predictions = []
        for page in result.pages:
            logger.info(f"Page dimensions: {page.dimensions}")
            for block in page.blocks:
                for line in block.lines:
                    for word in line.words:
                        x0, y0 = word.geometry[0]
                        x1, y1 = word.geometry[1]
                        predictions.append({
                            "from_name": "transcription",
                            "to_name": "image",
                            "type": "textarea",
                            "value": {
                                "text": [word.value],
                                "x": x0 * 100,
                                "y": y0 * 100,
                                "width": (x1 - x0) * 100,
                                "height": (y1 - y0) * 100,
                                "rotation": 0,
                            },
                        })
        return predictions