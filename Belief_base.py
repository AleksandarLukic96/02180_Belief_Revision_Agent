"""
Implementation of belief base.

The logic syntax used is the following:
or: |
and: &
implies: ->
biimplication: <->
not: -
Parentheses are assumed to be used everywhere where two different operators appear, except for the not operator
"""

from utils import simplify, is_tautology, remove_duplicates_or
from CNF import to_CNF
from itertools import combinations
from inference import DPLL_satisfiable, entails, satisfiable


class belief_base:

    def __init__(self):
        self.base = []  # List for storing original sentences put into the belief base in the format [sentence, weight]
        self.CNF = []  # List for storing CNF form of sentences put into the belief base as list of lists

    def add(self, sentence, score):
        # Function to add a sentence to the belief base with the weight given by score. If the sentence cannot be
        # true given the existing beliefs, it is not added
        sentence = sentence.replace(' ', '')  # Remove whitespace
        sentence = simplify(sentence)
        CNF = to_CNF(sentence)
        new_CNF = []
        if DPLL_satisfiable([x[i] for x in self.CNF for i in range(len(x))], CNF):
            # If the sentence is satisfiable in the belief base, add it to the belief base
            self.base.append([sentence, score])
            for i in range(len(CNF)):
                if not is_tautology(CNF[i]):
                    # Check that the CNF clause is not a tautology, and reduce it before adding
                    new_CNF.append(remove_duplicates_or(CNF[i]))
            self.CNF.append(new_CNF)
        else:
            print('Sentence {} is incompatible with what is in the belief base'.format(sentence))

    def satisfiable(self, sentence):
        # Function for checking if a sentence is satisfiable given the current beliefs
        return satisfiable([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], sentence)

    def entails(self, sentence):
        # Function for checking if a sentence entails from the current beliefs
        return not satisfiable([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], '-(' + sentence+')')

    def print(self):
        # Prints the beliefs base as orginal sentences and in CNF, along with the weights of the sentences
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
        # Function for contracting a sentence from the belief base, removing beliefs to ensure the sentence does
        # not follow from the beliefs. Beliefs are removed in a way so that the minimum number of beliefs are removed,
        # with the maximum weight of the removed beliefs being as low as possible, to make the sentence not follow from
        # the remaining beliefs

        if not entails([self.CNF[x][i] for x in range(len(self.base)) for i in range(len(self.CNF[x]))], sentence):
            # If the sentence already does not entail from the beliefs, nothing should be done
            return
        # Loop over number of sentences to remove, starting from 1 to find a possibility with the lowest possible
        # number
        for i in range(1, len(self.base)+1):
            # Possible sentences to remove, sorted ascending according to the weights of the removed sentences
            remove = sorted(list(combinations(list(range(len(self.base))), i)), key=lambda x: tuple([int(self.base[x[y]][1]) for y in range(i)]))
            for set in remove:
                # Contruct a belief base in CNF with the remaining beliefs
                new_base = [self.CNF[x][i] for x in range(len(self.base)) if x not in set for i in range(len(self.CNF[x]))]
                if not entails(new_base, sentence):
                    # If the sentence does not entail, the current possibility for removing sentences is the best
                    # given the method of prioritization
                    for index in sorted(list(set), reverse=True):
                        print(f'Removes sentence {self.base[index][0]}')
                        del self.base[index]
                        del self.CNF[index]
                    return

    def revision(self, sentence, score):
        # Implementation of revision of the belief base with a sentence using Levi identity
        self.contract('-('+sentence+')')
        self.add(sentence, score)

