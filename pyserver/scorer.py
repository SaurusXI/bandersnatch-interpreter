import spacy

class Evaluator:
    def __init__(self, nlp):
        self.nlp = nlp

    '''
    Returns (valid_input, best_option = None, right_score = 0, left_score = 0)
    '''
    def check_options(self, user_input, left_option=None, right_option=None):
        user_doc = self.nlp(user_input)
        user_ent = user_doc.ents[0] if len(user_doc.ents)>0 else None
        
        # score = (sent_similarity, ent_similarity)
        sent_scores = [0, 0]
        ent_scores = [0, 0]
        
        if left_option is None and right_option is None:
            return (True, 0, 0, 0)
        
        if left_option is not None:
            sent_scores[0], ent_scores[0] = self.get_score(self.nlp(left_option), user_doc, user_ent)
        
        if right_option is not None:
            sent_scores[1], ent_scores[1] = self.get_score(self.nlp(right_option), user_doc, user_ent)
        
        left_score = sent_scores[0]
        right_score = sent_scores[1]

        max_score, index = max(sent_scores), sent_scores.index(max(sent_scores))

        if max_score <0.8:
            return (False, index, left_score, right_score)
        else:
            # Check if answers are close
            if max_score - sent_scores[abs(index-1)] <=0.1:
                max_score, index = max(ent_scores), ent_scores.index(max(ent_scores))
                
                if max_score <0.5:
                    return (False, index, left_score, right_score)
                
            return (True, index, left_score, right_score)

    def get_score(self, doc, user_doc, user_ent):
        '''
        This function calculates score for a node
        '''
        score = [0, 0]
        
        score[0] = user_doc.similarity(doc)
        
        if len(doc.ents)>0 and user_ent is not None:
            score[1] = user_ent.similarity(doc.ents[0])
            
        return score[0], score[1]