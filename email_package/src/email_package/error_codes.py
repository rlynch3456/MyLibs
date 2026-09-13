from enum import Enum, unique
@unique
class ErrorCodes(Enum):
    SUCCESS = 0
    MISSING_TO_RECIPIENT = 1
    MISSING_FROM_RECIPIENT = 2
    MISSING_FROM_EMAIL = 3
    MISSING_FROM_EMAIL_ADDRESS = 4
    BAD_EMAIL_ADDRESS = 5
    NO_MESSAGE_FOUND = 6
