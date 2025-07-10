def load_binary(filepath):
    with open(filepath, "rb") as file_object:
        content = file_object.read()
        return content