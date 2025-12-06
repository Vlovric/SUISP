from src.utils.security_policy_manager import security_policy_manager
from src.models.user_model import UserModel
from src.models.datoteka.datoteka_model import DatotekaModel
from datetime import datetime, timedelta

class KeyRotationHelper():

    @staticmethod
    def rotate_keys(progress_callback=None) -> tuple[bool, str | None]:
        
        file_count = DatotekaModel.get_file_count()
        

    
    @staticmethod
    def needs_rotation() -> bool:
        user =  UserModel().get_user()
        last_rotation = user.get("last_key_rotation")

        rotation_interval_days = security_policy_manager.get_policy_param("key_rotation_interval_days")
        if not last_rotation:
            return True
        
        days_since_rotation = (datetime.now() - datetime.fromisoformat(last_rotation)).days
        return days_since_rotation >= rotation_interval_days