from utils import *


class belief_base:

    def __init__(self):
        self.base = []
        self.CNF = []

    def add(self, sentence, score):
        sentence = sentence.replace(' ', '')
        sentence = simplify(sentence)
        CNF = to_CNF(sentence)
        if DPLL_satisfiable([x[i] for x in self.CNF for i in range(len(x))], CNF):
            self.base.append([sentence, score])
            for i in range(len(CNF)):
                if is_tautology(CNF[i]):
                    CNF.remove(CNF[i])
                CNF[i] = remove_duplicates(CNF[i])
            self.CNF.append(CNF)
        else:
            print('Sentence {} is incompatible with what is in the belief base'.format(sentence))

    def satisfiable(self, sentence):
        return DPLL_satisfiable([x[i] for x in self.CNF for i in range(len(x))], to_CNF(sentence))

    def entails(self, sentence):
        return not self.satisfiable('-'+sentence)

    def print(self):
        if len(self.base) == 0:
            print('Empty belief base')
        else:
            padding = max(len(max([x[0] for x in self.base], key=len)), len('Belief'))
            print('{: <{padding}} | Certainty:'.format('Belief', padding = padding))
            for element in self.base:
                print('{: <{padding}} | {}'.format(element[0], element[1], padding=padding))
            print('\n')
            padding = max(len(max([x[i] for x in self.CNF for i in range(len(x))], key=len)), len('Belief in CNF '))
            print('{:<{padding}} | Certainty:'.format('Belief in CNF ', padding = padding))
            for i in range(len(self.CNF)):
                belief = self.CNF[i]
                for element in belief:
                    print('{:<{padding}} | {}'.format(element, self.base[i][1], padding=padding))


