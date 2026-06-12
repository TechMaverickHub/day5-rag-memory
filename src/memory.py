from collections import deque

MAX_MESSAGES = 10

chat_history = deque(
    maxlen=MAX_MESSAGES
)


def add_message(
    role: str,
    content: str,
):
    chat_history.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_history() -> str:
    if not chat_history:
        return ""

    return "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in chat_history
        ]
    )


def clear_history():
    chat_history.clear()