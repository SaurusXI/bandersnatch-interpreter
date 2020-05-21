import nltk
from nltk.tokenize import word_tokenize
import string
import random

class Replier:
    def __init__(self):
        self.similar_templates = []
        self.similar_templates.append(string.Template('You try to ${VERB} ${ADP} the ${NOUN}, but nothing happens.'))
        self.similar_templates.append(string.Template('You try to ${VERB} ${ADP} the ${NOUN}, but that doesn\'t do anything.'))
        self.similar_templates.append(string.Template(''))

        self.dissimilar_templates = []
        self.dissimilar_templates.append(string.Template('You ${VERB} ${ADP} the ${NOUN}. Now back to the task at hand.'))
        self.dissimilar_templates.append(string.Template('Is that really going to help right now?'))
        self.dissimilar_templates.append(string.Template('You shouldn\'t be wasting time!'))
        self.dissimilar_templates.append(string.Template('Why would you want to do that right now?'))

        self.default_template = 'That doesn\'t make sense to me'


    def reply(self, user_input, best_score):
        tokens = word_tokenize(user_input)
        lexemes = nltk.pos_tag(tokens, tagset = 'universal')

        nouns = []
        verbs = []
        adpositions = []

        for lexeme in lexemes:
            tag = lexeme[1]
            if tag == 'NOUN':
                nouns.append(lexeme[0])
            elif tag == 'VERB':
                verbs.append(lexeme[0])
            elif tag == 'ADP':
                adpositions.append(lexeme[0])

        if best_score > 0.7:
            similar = True
        else:
            similar = False
        print(lexemes)
        return self.generate_reply(nouns, verbs, adpositions, similar)

    def generate_reply(self, nouns, verbs, adps, similar = False):
        if not nouns or not verbs:
            return self.default_template

        noun = nouns[0].lower()

        verb = verbs[0].lower()
        
        if adps:
            adp = adps[0].lower()
        else:
            adp = ''

        if similar:
            index = random.randint(0, len(self.similar_templates) - 1)
            reply = self.similar_templates[index].safe_substitute(NOUN = noun, VERB = verb, ADP = adp)
            return reply

        else:
            index = random.randint(0, len(self.dissimilar_templates) - 1)
            reply = self.dissimilar_templates[index].safe_substitute(NOUN = noun, VERB = verb, ADP = adp)
            return reply