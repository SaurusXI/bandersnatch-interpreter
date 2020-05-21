import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Evaluator:
    def __init__(self, client, scorer):
        self.client = client
        self.scorer = scorer

    '''
    Returns (valid_input, best_option = None, best_score = 0)
    '''
    def check_options(self, user_input, left_option = None, right_option = None):
        refs = []
        cand = self.client.encode([user_input])
        i = 1

        if left_option is None and right_option is None:
            return (True, 0, 0)

        if left_option is not None:
            left_vector = self.client.encode([left_option])
            refs.append(left_vector)
            i = 0

        if right_option is not None:
            right_vector = self.client.encode([right_option])
            refs.append(right_vector)

        # print(refs)
        scores = []
        for ref in refs:
            scores.append(cosine_similarity(ref, cand))

        max_score, index = max(scores), scores.index(max(scores))

        if max_score < 0.8:
            return (False, index + i, max_score)

        else:
            return (True, index + i, max_score)