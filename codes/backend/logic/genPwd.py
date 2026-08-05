import string
import secrets

from ... import config


def generatePwd():
    """Read the generator options from `config` at call time (not import
    time) so changes made in the Settings dialog take effect immediately."""
    char = string.ascii_lowercase

    if config.USE_UPPER_CHAR:
        char += string.ascii_uppercase
    if config.USE_DIGITS:
        char += string.digits
    if config.USE_SYMBOLS:
        char += string.punctuation

    length = max(config.GENERATED_LENGTH, 0)
    return "".join(secrets.choice(char) for _ in range(length))
