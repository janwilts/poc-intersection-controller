from enum import Enum


class LightState(Enum):
    # Green
    GO = 1
    # Orange
    STOP = 2
    # Red
    WAIT = 0

# --------
# |  GO  |
# |      |
# | STOP |
# |      |
# | WAIT |
# --------
