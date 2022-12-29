from typing import Callable

from src.keyboard.keys import special_keys


def do_for_letter_keys(method: Callable) -> Callable:
    """ A decorator for iterating through all keyboard keys which are letters. """

    def inner(*args):
        self = args[0]
        for button in self.buttons:
            if button['text'] not in special_keys:
                method(self, button)
    return inner


def remove_char(string: str, index: int) -> str:
    """
    Removes character at the given index from a string.

    Args:
        string: String from which to remove character.
        index: The index of the character to be removed.

    Returns:
        String with removed character.
    """

    if len(string) > index:
        # Slice string
        string = string[0: index:] + string[index + 1::]
    else:
        string = ''
    return string


def insert_char(string: str, char: str, index: int) -> str:
    """
    Inserts character at the given index into a string.

    Args:
        string: String into which the character will be inserted.
        char: Character to insert.
        index: The index after which character will be inserted.

    Returns:
        String with inserted character.
    """

    return string[:index] + char + string[index:]
