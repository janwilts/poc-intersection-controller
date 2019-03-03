from intersection.components.component_state import ComponentState


class LightState(ComponentState):
    """
    Possible states for a light component.
    """

    GO = 2
    TRANSITIONING = 1
    STOP = 0
    OUT_OF_SERVICE = 4

    # The allowed order in which the traffic light can switch, wir sind keine Deutsche.
    ALLOWED_ORDER = [GO, TRANSITIONING, STOP]

# --------
# |  GO  |
# |      |
# | STOP |
# |      |
# | WAIT |
# --------
