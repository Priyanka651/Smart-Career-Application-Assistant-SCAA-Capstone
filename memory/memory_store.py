# memory/memory_store.py
"""
Simple JSON-backed memory store for long-term memory (not secure; for demo only).
Stores user preferences, jd_signatures, and past answers.
"""
import json
import os
from typing import Any

DEFAULT_PATH = "memory/memory_store.json"

class MemoryStore:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({"users":{}, "jd_signatures":{}, "answers":{}}, f)

    def _load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, key, default=None):
        data = self._load()
        return data.get(key, default)

    def read_user(self, user_id):
        data = self._load()
        return data["users"].get(user_id, {})

    def write_user(self, user_id, payload):
        data = self._load()
        data["users"][user_id] = payload
        self._save(data)

    def add_jd_signature(self, sig, payload):
        data = self._load()
        data["jd_signatures"][sig] = payload
        self._save(data)

    def add_answer(self, user_id, job_id, answer):
        data = self._load()
        u = data["answers"].setdefault(user_id, {})
        u[job_id] = answer
        self._save(data)

# Example usage
if __name__ == "__main__":
    mem = MemoryStore("memory/demo.json")
    mem.write_user("u1", {"prefs": ["frontend"]})
    print(mem.read_user("u1"))
