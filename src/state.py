import jovialengine


class State(jovialengine.Saveable):
    __slots__ = (
        'score',
        'high_score',
    )

    def __init__(self):
        self.score = 0
        self.high_score = 0

    def save(self):
        return {
            'score': self.score,
            'high_score': self.high_score,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.score = save_data['score']
        new_obj.high_score = save_data['high_score']
        return new_obj
