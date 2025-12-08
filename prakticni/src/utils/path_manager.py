from platformdirs import PlatformDirs
from pathlib import Path
import sys

APP_NAME = "SecureFileVault"
APP_AUTHOR = "SUISP"

class PathManager:
    _instance = None
    _dirs = PlatformDirs(appname=APP_NAME, appauthor=APP_AUTHOR)

    # Windows: %LOCALAPPDATA%\SecureFileVault
    # Linux: ~/.local/share/SecureFileVault
    BASE_APP_DIR = Path(_dirs.user_data_dir)

    CONFIG_DIR = BASE_APP_DIR / "config"
    DATA_DIR = BASE_APP_DIR / "data"
    FILES_DIR = DATA_DIR / "vault_storage"
    SECURITY_POLICY_JSON = CONFIG_DIR / "security_policy.json"
    DB_FILE = DATA_DIR / "file_vault_database.db"

    # Windows: %LOCALAPPDATA%\SecureFileVault\Cache\temp_unlocked
    # Linux: ~/.cache/SecureFileVault/temp_unlocked
    CACHE_DIR = Path(_dirs.user_cache_dir)
    TEMP_DIR = CACHE_DIR / "temp_unlocked"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathManager, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = Path(__file__).resolve().parent.parent.parent
        
        return Path(base_path) / relative_path

    @classmethod
    def ensure_dirs(cls):
        for d in (cls.BASE_APP_DIR, cls.CONFIG_DIR, cls.DATA_DIR, cls.FILES_DIR, cls.CACHE_DIR, cls.TEMP_DIR):
                print("Creating directory:", d)
                d.mkdir(parents=True, exist_ok=True)
    
path_manager = PathManager()