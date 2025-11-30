from platformdirs import PlatformDirs
from pathlib import Path

APP_NAME = "SecureFileVault"
APP_AUTHOR = "SUISP"

def _is_dev() -> bool:
    return True # Ne da mi se set uppat env varijable tak da sam maknemo

def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent

_dirs = PlatformDirs(appname=APP_NAME, appauthor=APP_AUTHOR)

if _is_dev():
    BASE_APP_DIR = _project_root()

    CONFIG_DIR = BASE_APP_DIR
    DATA_DIR = BASE_APP_DIR / "data"
    FILES_DIR = DATA_DIR / "vault_storage"
    SECURITY_POLICY_JSON = CONFIG_DIR / "security_policy.json"
    DB_FILE = DATA_DIR / "baza.db"
else:
    # Windows: %LOCALAPPDATA%\SecureFileVault
    # Linux: ~/.local/share/SecureFileVault
    BASE_APP_DIR = Path(_dirs.user_data_dir)

    CONFIG_DIR = BASE_APP_DIR / "config"
    DATA_DIR = BASE_APP_DIR / "data"
    FILES_DIR = DATA_DIR / "vault_storage"
    SECURITY_POLICY_JSON = CONFIG_DIR / "security_policy.json"
    DB_FILE = DATA_DIR / "file_vault_database.db"



def ensure_dirs():
    if not _is_dev():
        for d in (BASE_APP_DIR, CONFIG_DIR, DATA_DIR, FILES_DIR):
            d.mkdir(parents=True, exist_ok=True)