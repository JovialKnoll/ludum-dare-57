import jovialengine


class State(jovialengine.Saveable):
    __slots__ = (
    )

    def __init__(self):
        pass

    def save(self):
        return {
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        return new_obj
