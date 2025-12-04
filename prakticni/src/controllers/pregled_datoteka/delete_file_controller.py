
import os
from src.utils import security_policy_manager
from src.utils.file_selection_response import FileSelectionResponse
from src.controllers.base_controller import BaseController
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.file_manager import FileManager

class DeleteFileController(BaseController):
    def __init__(self):
        super().__init__()

    def delete_file(self, file_id):
        try:
            database_path = DatotekaModel.fetch_by_id(file_id)["path"]
            absolute_path = os.path.abspath(database_path)
            if os.path.exists(absolute_path):
                FileManager.secure_delete(absolute_path)

            result = DatotekaModel.delete_file_by_id(file_id)

            if result == 0:
                return {"status": "success", "message": "File deleted successfully."}
            else:
                return {"status": "error", "message": "File not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}