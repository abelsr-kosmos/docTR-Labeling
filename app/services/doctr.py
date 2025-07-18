import random
import string
from typing import Any, Dict

import torch
from loguru import logger
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


class DocTRService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        self.model = ocr_predictor(pretrained=True).to(self.device)

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
            for block in page.blocks:
                for line in block.lines:
                    for word in line.words:
                        x0, y0 = word.geometry[0]
                        x1, y1 = word.geometry[1]
                        id = self.__generate_id()
                        bbox = {
                            "from_name": "bbox",
                            "id": id,
                            "to_name": "image",
                            "type": "rectangle",
                            "value": {
                                "text": [word.value],
                                "x": x0 * 100,
                                "y": y0 * 100,
                                "width": (x1 - x0) * 100,
                                "height": (y1 - y0) * 100,
                                "rotation": 0,
                            },
                        }
                        label = {
                            "from_name": "label",
                            "id": id,
                            "to_name": "image",
                            "type": "labels",
                            "value": {
                                "text": [word.value],
                                "x": x0 * 100,
                                "y": y0 * 100,
                                "width": (x1 - x0) * 100,
                                "height": (y1 - y0) * 100,
                                "rotation": 0,
                                "labels": [
                                    "Text"
                                ]
                            },
                        }
                        transcription = {
                            "from_name": "transcription",
                            "to_name": "image",
                            "id": id,
                            "type": "textarea",
                            "value": {
                                "text": [word.value],
                                "x": x0 * 100,
                                "y": y0 * 100,
                                "width": (x1 - x0) * 100,
                                "height": (y1 - y0) * 100,
                                "rotation": 0,
                            },
                        }
                        predictions.append(bbox)
                        predictions.append(label)
                        predictions.append(transcription)
                        
        return predictions
    
    def __generate_id(self):
        "Generate a random id of 10 characters with letters and numbers"
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))