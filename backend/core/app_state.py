"""
Shared application state.

This module stores objects that need to be accessed
throughout the application, maintaining distinct FAISS indices
and chunk metadata cache per user.
"""

class AppState:
    def __init__(self):
        self.user_indices = {}  # user_id -> FAISS index
        self.user_chunks = {}   # user_id -> chunk metadata list


app_state = AppState()