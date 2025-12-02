def get_line(data: list[str]) -> str:
    if not data:
        return ""

    val = data[0]
    data.pop(0)

    return val.replace("|", " ")