import json
import os
from typing import Any


class SessionMemory:
    """
    Simple JSON-based session + memory store.
    Stores user sessions, outlines, generated blogs, and snapshots.
    """

    def __init__(self, save_path='session_memory.json'):
        self.save_path = save_path
        self.store = {}

        # Load previous memory if file exists
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    self.store = json.load(f)
            except Exception:
                # If corrupted, start clean
                self.store = {}

    def set(self, session_id: str, data: Any):
        """Set a session to a specific data value."""
        self.store[session_id] = data
        self._persist()

    def append(self, session_id: str, data: Any):
        """
        Append data to an existing session.
        If session doesn't exist, create a new list.
        If session exists but isn't a list, convert it.
        """
        if session_id not in self.store:
            self.store[session_id] = []

        if isinstance(self.store[session_id], list):
            self.store[session_id].append(data)
        else:
            # Convert non-list session to list
            self.store[session_id] = [self.store[session_id], data]

        self._persist()

    def get(self, session_id: str):
        """Retrieve stored memory for a session."""
        return self.store.get(session_id)

    def _persist(self):
        """Save the store back to disk."""
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(self.store, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Error saving session memory:", e)
