from intersection.components.state import State


class LightState(State):
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
