
def get_history_command(text, prefix):

    history = []

    text = text.replace("\\\n> ", "")
    commands = text.split("\n")

    for command in commands:
        if prefix in command and not command.endswith("$ "):
            history.append(command)
    return history