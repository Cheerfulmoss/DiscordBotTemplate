def title_format(words):
    title_top = "---" + words + "-" * (86 - len(words))
    title_bottom = "-" * 89 + "\n"
    return title_top, title_bottom
