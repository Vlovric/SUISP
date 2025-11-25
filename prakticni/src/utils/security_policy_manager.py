from pathlib import Path
import json
class SecurityPolicyManager:
    """ Singleton za dohvacanje parametara propisanih u sigurnosnoj politici"""

    _instance = None
    _policy = None
    _policy_path = Path(__file__).parent.parent.parent / "security_policy.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityPolicyManager, cls).__new__(cls)
            cls._instance.__load_policy()
        return cls._instance
    
    def __load_policy(self):
        if self._policy is not None:
            return #Jel bi se trebala moc mijenjat u runtimeu? Izvan opsega mozda
        
        try:
            with open(self._policy_path, "r") as f:
                self._policy = json.load(f)
        except FileNotFoundError:
            raise Exception(f"Security policy file not found at {self._policy_path}")
        except json.JSONDecodeError:
            raise Exception("Security policy file is not a valid JSON.")
    
    def get_policy_param(self, key: str):
        if self._policy is None:
            self._load_policy()

        value = self._policy.get(key)
        if value is None:
            raise KeyError(f"Policy parameter '{key}' not found.")
        return value
    
security_policy_manager = SecurityPolicyManager()

        
