import json
import os


MEMORY_FILE = "study_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=2
        )


def add_memory(role, content):

    memory = load_memory()

    memory.append(
        {
            "role": role,
            "content": content
        }
    )

    # Keep the latest 20 messages
    memory = memory[-20:]

    save_memory(memory)


def get_memory_text():

    memory = load_memory()

    if not memory:

        return "No previous conversation."

    text = ""

    for item in memory:

        text += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    return text
