import requests
from tqdm import tqdm
from loguru import logger
from label_studio_sdk import Client


class DocTRLabeler:
    def __init__(self, doctr_service_url: str, label_studio_url: str, api_key: str, project_id: int):
        self.label_studio_url = label_studio_url
        self.api_key = api_key
        self.doctr_service_url = doctr_service_url
        self.ls_client = Client(url=label_studio_url, api_key=api_key)
        self.ls_client.check_connection()
        self.project_id = project_id

    def run(self):
        # Get all tasks from the project
        tasks = self.ls_client.get_project(self.project_id).get_tasks()
        
        # Filter tasks that already have annotations
        tasks = [task for task in tasks if len(task.get("predictions", [])) == 0]
        
        progress_bar = tqdm(tasks, total=len(tasks), desc="Labeling tasks")
        for task in progress_bar:
            # Check if the task has already been labeled
            # Get the image
            image_path = task.get("data").get("ocr", None)
            if not image_path:
                progress_bar.write(f"Task {task.get('id')} has no image path")
                continue
            image = self._get_image(image_path)
            # Get the predictions
            predictions = self._predict(image)
            # Create the annotation
            self.ls_client.get_project(self.project_id).create_prediction(
                task.get("id"),
                result=predictions,
                model_version="1.0.0"
            )

    def _get_image(self, url: str) -> bytes:
        if not url:
            raise ValueError("URL is required")
        response = requests.get(
            f"{self.label_studio_url}{url}",
            headers={"Authorization": f"Token {self.api_key}"}
        )
        return response.content
    
    def _predict(self, image: bytes) -> dict:
        import io
        files = {'file': ('image.jpg', io.BytesIO(image), 'image/jpeg')}
        response = requests.post(
            f"{self.doctr_service_url}/predict",
            files=files,
            headers={"accept": "application/json"}
        )
        return response.json()["predictions"][0]["result"]
    
    
if __name__ == "__main__":
    labeler = DocTRLabeler(
        doctr_service_url="http://localhost:8000",
        label_studio_url="https://ls.ksms.mx/",
        api_key="fd23fd63c0d45a6fd264ad34d6aaf7e225e09e64",
        project_id=65
    )
    labeler.run()