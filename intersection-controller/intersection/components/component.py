class Component:
    type = None

    def __init__(self, id=1):
        self.id = id
        self.group = None

        self.state = None

    @property
    def topic(self):
        base_topic = f'{self.group.topic}/{self.type.value}'

        if self.id:
            return f'{base_topic}/{self.id}'

        return base_topic
