from utils.path_manager import path_manager
from pathlib import Path
import json

class SecurityPolicyManager:
    """ Singleton za dohvacanje parametara propisanih u sigurnosnoj politici"""

    _instance = None
    _policy = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityPolicyManager, cls).__new__(cls)
        return cls._instance
    
    def __load_policy(self):
        if not path_manager.SECURITY_POLICY_JSON.exists():
            default_policy_path = Path(__file__).parent.parent.parent / "security_policy.json"
            try:
                data = json.loads(default_policy_path.read_text(encoding="utf-8"))
                path_manager.SECURITY_POLICY_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
            except FileNotFoundError:
                raise Exception("Default security policy file not found.")
            except json.JSONDecodeError:
                raise Exception("Default security policy file is not a valid JSON.")
        
        self._policy = json.loads(path_manager.SECURITY_POLICY_JSON.read_text(encoding="utf-8"))
    
    def get_policy_param(self, key: str):
        if self._policy is None:
            self._load_policy()

        value = self._policy.get(key)
        if value is None:
            raise KeyError(f"Policy parameter '{key}' not found.")
        return value
    
security_policy_manager = SecurityPolicyManager()

        
