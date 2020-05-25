import spacy
import string
import random

class Replier:
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        self.nlp_small = spacy.load("en_core_web_small")
        self.prefixes = ["Nothing happens.", "That doesn't do anything.", "You try to ${VERB} the ${NOUN}, but that doesn\'t do anything.", "${VERB}ing the ${NOUN} doesn't do anything.", "That doesn't seem to do anything.", "${VERB}ing the ${NOUN} doesn't help.", "Nothing happens when you ${VERB} the ${NOUN}."]
        self.default = "That doesn't make sense to me. Try typing 'help' for examples on how to interact with the environment"

    def reply(self, user_input, l_score = 0, r_score = 0, left_option = None, right_option = None):
            
        tokens = self.nlp(user_input)

        root_verb = None
        noun_ = None
        nonsense = False

        for token in tokens:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                root_verb = token
                for child in root_verb.children:
                    if child.pos_ == 'NOUN':
                        noun_ = child
                        break
                break
            # print(token.text, token.pos_, token.dep_)

        if root_verb is None or noun_ is None:
            nonsense = True

        if not nonsense:
            l_verb = None
            l_noun_ = None

            r_verb = None
            r_noun_ = None

            similarity = {"verb": 0, "noun": 0}

            if left_option is not None:
                if l_score >= r_score:

                    l_tokens = self.nlp_small(left_option)

                    for token in l_tokens:
                        if token.pos_ == 'VERB':
                            l_verb = token
                        elif token.pos_ == 'NOUN':
                            l_noun_ = child
                                    
                        print(token.text, token.pos_, token.dep_)

                    if l_verb is not None:
                        similarity['verb'] = noun_.similarity(l_verb)
                    if l_noun_ is not None:
                        similarity['noun'] = root_verb.similarity(l_noun_)
                
                
            if right_option is not None:
                if r_score > l_score:
                    r_tokens = self.nlp_small(right_option)

                    for token in r_tokens:
                        if token.pos_ == 'VERB':
                            r_verb = token
                        elif token.pos_ == 'NOUN':
                            r_noun_ = child

                    if r_verb is not None:
                        similarity['verb'] = noun_.similarity(r_verb)
                    if r_noun_ is not None:
                        similarity['noun'] = root_verb.similarity(r_noun_)

            pos_max = max(similarity, key = similarity.get)

            if similarity[pos_max] > 0.79:
                pos_key = pos_max

            else:
                pos_key = 'dissimilar'

        return self.generate_reply(pos_key, nonsense, root_verb, noun_)        

    def generate_reply(self, most_similar_pos, nonsense, verb, noun):
        if nonsense:
            return self.default

        if most_similar_pos == 'noun':
            templates = [ 'Maybe you can do something else with the ${NOUN}?',
                                'Try interacting with the ${NOUN} in a different way.',
                                'You should try interacting with the ${NOUN} in a different way.',
                                'Try doing something else with the ${NOUN}.']
            index = random.randint(0, len(templates) - 1)
            template = templates[index]

        elif most_similar_pos == 'verb':
            templates = ['You should try to ${VERB} something else.', 'Try ${VERB}ing something else.', 'Perhaps you can ${VERB} something else in your environment.']
            index = random.randint(0, len(templates) - 1)
            template = templates[index]

        elif most_similar_pos == 'dissimilar':
            template = ''

        p_idx = random.randint(0, len(self.prefixes) - 1)
        template = string.Template(self.prefixes[p_idx] + ' ' + template)
        reply = template.safe_substitute(NOUN = noun.text.lower(), VERB = verb.text.lower())

        return reply
        