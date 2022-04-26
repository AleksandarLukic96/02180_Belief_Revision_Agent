from utils import *
from itertools import combinations

class belief_base:

    def __init__(self):
        self.base = []
        self.CNF = []

    def add(self, sentence, score):
        sentence = sentence.replace(' ', '')
        sentence = simplify(sentence)
        CNF = to_CNF(sentence)
        new_CNF = []
        if DPLL_satisfiable([x[i] for x in self.CNF for i in range(len(x))], CNF):
            self.base.append([sentence, score])
            for i in range(len(CNF)):
                if not is_tautology(CNF[i]):
                    new_CNF.append(remove_duplicates(CNF[i]))
            self.CNF.append(new_CNF)
        else:
            print('Sentence {} is incompatible with what is in the belief base'.format(sentence))

    def satisfiable(self, sentence):
        return satisfiable([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], sentence)

    def entails(self, sentence):
        return not satisfiable([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], '-(' + sentence+')')

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

    def contract(self, sentence):
        if not entails([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], sentence):
            return

        for i in range(1, len(self.base)+1):
            remove = sorted(list(combinations(list(range(len(self.base))), i)), key=lambda x: tuple([int(self.base[x[y]][1]) for y in range(i)]))
            for set in remove:
                new_base = [self.CNF[x][i] for x in range(len(self.base)) if x not in set for i in range(len(self.CNF[x]))]
                if not entails(new_base, sentence):
                    for index in sorted(list(set), reverse=True):
                        print(f'Removes sentence {self.base[index][0]}')
                        del self.base[index]
                        del self.CNF[index]
                    return

    def revision(self, sentence, score):
        self.contract('-('+sentence+')')
        self.add(sentence, score)

