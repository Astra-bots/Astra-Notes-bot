import json
import os

FILE_NAME = "notes.json"


def load_notes():

    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notes(data):

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def add_note(user_id, text):

    data = load_notes()

    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(text)

    save_notes(data)


def get_notes(user_id):

    data = load_notes()

    return data.get(str(user_id), [])


def delete_note(user_id, index):

    data = load_notes()

    user_id = str(user_id)

    if user_id in data:

        if 0 <= index < len(data[user_id]):

            data[user_id].pop(index)

            save_notes(data)

            return True

    return False


def delete_all_notes(user_id):

    data = load_notes()

    user_id = str(user_id)

    if user_id in data:

        data[user_id] = []

        save_notes(data)


def edit_note(user_id, index, new_text):

    data = load_notes()

    user_id = str(user_id)

    if user_id in data:

        if 0 <= index < len(data[user_id]):

            data[user_id][index] = new_text

            save_notes(data)

            return True

    return False


def search_notes(user_id, keyword):

    notes = get_notes(user_id)

    result = []

    for i, note in enumerate(notes):

        if keyword.lower() in note.lower():

            result.append((i, note))

    return result
