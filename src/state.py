import jovialengine

import constants


class State(jovialengine.Saveable):
    __slots__ = (
        'score',
        'high_scores',
    )

    def __init__(self):
        self.score = 0
        self.high_scores = []

    def save(self):
        return {
            'score': self.score,
            'high_scores': self.high_scores,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.score = save_data['score']
        new_obj.high_scores = save_data['high_scores']
        return new_obj

    def get_score(self):
        return f"{int(self.score):010}"

    def get_high_score(self):
        high_score = 0 if not self.high_scores else self.high_scores[0]
        return f"{high_score:010}"

    def get_high_scores(self):
        return [f"{high_score:010}" for high_score in self.high_scores[:10]]

    def enter_score(self):
        int_score = int(self.score)
        self.score = 0
        if int_score == 0:
            return
        if int_score > (self.high_scores[0] if self.high_scores else 0):
            new_high_score = jovialengine.load.sound(constants.NEW_HIGH_SCORE)
            new_high_score.play()
        self.high_scores.append(int_score)
        self.high_scores = list(set(self.high_scores))
        self.high_scores.sort(reverse=True)
