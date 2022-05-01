import sys
# setting path
sys.path.append('../02180_BELIEF_REVISION_AGENT')

"""
Test with flower variation of mastermind game from exercise session week 10
"""

from Belief_base import belief_base
import itertools

rules = ['t_1|s_1|d_1', 't_2|s_2|d_2', '(-t_1|-s_1)&(-s_1|-d_1)&(-d_1|-t_1)', '(-t_2|-s_2)&(-s_2|-d_2)&(-d_2|-t_2)']
premises = ['(t_1&-d_2)|(d_2&-t_1)', '-t_1&-t_2', '(d_1&-d_2)|(d_2&-d_1)']

base = belief_base()

for rule in rules:
    base.add(rule, 100)
for premise in premises:
    base.add(premise, 50)
base.print()
colors = ['t', 'd', 's']
fields = 2

pos=[[colors[i]+'_'+str(j) for i in range(len(colors))] for j in range(1,fields+1)]
guesses = list(itertools.product(*pos))
new_guesses = []

for guess in guesses:
    # Check all possible guesses
    if base.satisfiable('&'.join(guess)):
        new_guesses.append(guess)
print(new_guesses)  # Only the correct guess should be possible


