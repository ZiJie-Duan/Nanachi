
def get_history_command(text, prefix):

    history = []

    text = text.replace("\\\n> ", "")
    commands = text.split("\n")

    for command in commands:
        if prefix in command and not command.endswith("$ "):
            history.append(command)
    return history


def get_n_history(text, prefix, n): 
    text = text.replace("\\\n> ", "")
    parts = text.split(prefix)
    parts = [x for x in parts if not (x.endswith("$ \n") \
                                or x.endswith("$ \n\n") \
                                or x.endswith("$ \n\n\n"))]
    parts = parts[len(parts)-n:len(parts)]
    return prefix + prefix.join(parts)