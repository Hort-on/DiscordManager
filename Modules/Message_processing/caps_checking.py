def is_caps(text):
    total_chars = len(text)
    if total_chars == 0:
        return False

    uppercase_chars = sum(1 for char in text if char.isupper())
    uppercase_ratio = uppercase_chars / total_chars

    return uppercase_ratio >= 0.6
