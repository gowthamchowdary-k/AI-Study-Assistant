"""
Shared application state.

This module stores objects that need to be accessed
throughout the application, such as the FAISS index
and chunk metadata.
"""


class AppState:
    def __init__(self):
        self.index = None
        self.chunks = None


app_state = AppState()