"""
This module contains a simple function to return a given message.
"""

def text(message: str) -> str:
    """
    Returns the message passed as an argument.

    Args:
        message (str): The message to be returned.

    Returns:
        str: The same message that was passed as input.
    """
    return message

if name == "__main__":
    print(text("Hello, World!"))  # Example usage
