def mask_string(s: str, num_unmasked_chars: int = 4) -> str:
    """
    Masks a string by replacing all characters except for the last `num_unmasked_chars` with asterisks.

    Args:
    s (str): The string to mask.
    num_unmasked_chars (int, optional): Number of characters at the end of the string to remain unmasked. Defaults to 4.

    Returns:
    str: The masked string, or a full mask (if its length is less than `num_unmasked_chars`).
    """
    if num_unmasked_chars == 0:
        return "*" * len(s)
    elif len(s) < num_unmasked_chars:
        return "*" * len(s)
    else:
        return "*" * (len(s) - num_unmasked_chars) + s[-num_unmasked_chars:]
