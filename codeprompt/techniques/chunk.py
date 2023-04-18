"""
this is from autogpt.
"""


from typing import Generator


def split_text(
    text: str, max_length: int = 8192, len_function=len
) -> Generator[str, None, None]:
    """Split text into chunks of a maximum length

    Args:
        text (str): The text to split
        max_length (int, optional): The maximum length of each chunk. Defaults to 8192.

    Yields:
        str: The next chunk of text

    Raises:
        ValueError: If the text is longer than the maximum length
    """
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for paragraph in paragraphs:
        if current_length + len_function(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len_function(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len_function(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)
