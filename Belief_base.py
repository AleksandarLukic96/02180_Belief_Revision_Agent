from utils import *


class belief_base:

    def __init__(self):
        self.base = []
        self.CNF = []

    def add(self, sentence, score):
        sentence = sentence.replace(' ', '')
        sentence = simplify(sentence)
        CNF = to_CNF(sentence)
        if DPLL_satisfiable([x[0] for x in self.CNF], CNF):
            self.base.append([sentence, score])
            for element in CNF:
                if not is_tautology(element):
                    self.CNF.append([remove_duplicates(element), score])
        else:
            print('Sentence {} is incompatible with what is in the belief base'.format(sentence))

    def satisfiable(self, sentence):
        return DPLL_satisfiable([x[0] for x in self.CNF], to_CNF(sentence))

    def print(self):
        if len(self.base) == 0:
            print('Empty belief base')
        else:
            padding = max(len(max([x[0] for x in self.base], key=len)), len('Belief'))
            print('{: <{padding}} | Certainty:'.format('Belief', padding = padding))
            for element in self.base:
                print('{: <{padding}} | {}'.format(element[0], element[1], padding=padding))
            print('\n')
            padding = max(len(max([x[0] for x in self.CNF], key=len)), len('Belief in CNF '))
            print('{:<{padding}} | Certainty:'.format('Belief in CNF ', padding = padding))
            for element in self.CNF:
                print('{:<{padding}} | {}'.format(element[0], element[1], padding=padding))
