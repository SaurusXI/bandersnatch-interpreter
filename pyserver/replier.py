import spacy
import string
import random


class Replier:
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        self.prefixes = ["Nothing happens.", "That doesn't do anything.", "You try to ${verb} the ${noun}, but that doesn\'t do anything.", "${Verb}ing the ${noun} doesn't seem to change anything.", "That doesn't seem to do anything.", "${Verb}ing the ${noun} doesn't seem to do anything.", "Nothing happens when you try to ${verb} the ${noun}."]
        self.default = "That doesn't make sense to me. Try typing 'help' for examples on how to interact with the environment"

    def reply(self, user_input, l_score = 0, r_score = 0, left_option = None, right_option = None):
            
        tokens = self.nlp(user_input)
        nonsense = False

        root_verb = self.nlp('')
        noun_ = tokens.ents[0] if len(tokens.ents) > 0 else self.nlp('')

        for token in tokens:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                root_verb = token
            if token.is_oov == True:
                nonsense = True
        
        if not nonsense:
            similarity = {"noun": 0}

            if left_option is not None:
                if l_score >= r_score:
                    l_tokens = self.nlp(left_option)
                    l_noun_ = l_tokens.ents[0] if len(l_tokens.ents) > 0 else None
                                    
                    if l_noun_ is not None and noun_.text != '':
                        similarity['noun'] = noun_.similarity(l_noun_)
                
            if right_option is not None:
                if r_score > l_score:
                    r_tokens = self.nlp(right_option)
                    r_noun_ = r_tokens.ents[0] if len(r_tokens.ents) > 0 else None

                    if r_noun_ is not None and noun_.text != '':
                        similarity['noun'] = noun_.similarity(r_noun_)

            # pos_max = max(similarity, key = similarity.get)

            if similarity["noun"] > 0.79:
                pos_key = "noun"

        return self.generate_reply(pos_key, nonsense, root_verb.text, noun_.text)        

    def generate_reply(self, most_similar_pos, nonsense, verb, noun):
        if nonsense:
            return self.default
        
        if most_similar_pos == 'noun':
            templates = [ 'Maybe you can do something else with the ${noun}?',
                                'Try interacting with the ${noun} in a different way.',
                                'You should try interacting with the ${noun} in a different way.',
                                'Try doing something else with the ${noun}.']
            index = random.randint(0, len(templates) - 1)
            template = templates[index]

        elif most_similar_pos == 'dissimilar':
            template = ''

        if noun == '' or verb == '':
            p_idx = 0
        else:
            p_idx = random.randint(0, len(self.prefixes) - 1)

        template = string.Template(self.prefixes[p_idx] + ' ' + template)
        reply = template.safe_substitute(noun = noun.lower(), verb = verb.lower(), Noun = noun.capitalize(), Verb = verb.capitalize())

        return reply
        
'''
        elif most_similar_pos == 'verb':
            templates = ['You should try to ${VERB} something else.', 'Try ${VERB}ing something else.', 'Perhaps you can ${VERB} something else in your environment.']
            index = random.randint(0, len(templates) - 1)
            template = templates[index]
'''