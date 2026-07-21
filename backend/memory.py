conversation_history = []
last_context = ""


def add_user_message(message):
    conversation_history.append({
        "role": "user",
        "content": message
    })


def add_ai_message(message):
    conversation_history.append({
        "role": "assistant",
        "content": message
    })


def get_history():
    return conversation_history


def save_context(context):
    global last_context
    last_context = context


def get_context():
    return last_context


def clear_memory():
    global conversation_history, last_context
    conversation_history = []
    last_context = ""