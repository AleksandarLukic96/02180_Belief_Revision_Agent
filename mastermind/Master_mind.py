from Belief_base import belief_base
import itertools
import random
from Feedback import generate_feedback, feedback_to_logic



solution = ['r', 'r', 'g']

colors=['r', 'g', 'y']
fields = len(solution)

rules = []
for i in range(1, fields+1):
    rules.append('|'.join(list(map('_'.join, list(itertools.product(*[colors, [str(i)]]))))))
    rule = ''
    for j in range(len(colors)):
        temp = list(map('_'.join, list(itertools.product(*[colors[:j] + colors[j+1:], [str(i)]]))))
        temp = ['-' + x for x in temp]
        rule += '&(' + '|'.join(temp) + ')'
    rules.append(rule[1:])

suc = 0
N = 100
nGuesses = []
for i in range(N):
    base = belief_base()

    for rule in rules:
        base.add(rule, 100)
    print(f'{i/N*100:.0f} % complete.')
    pos = [[colors[i] + '_' + str(j) for i in range(len(colors))] for j in range(1, fields + 1)]
    guesses = list(itertools.product(*pos))
    nGuess = 0
    random.shuffle(guesses)
    while len(guesses) > 0:
        guess = guesses[0]
        del guesses[0]
        guess = '&'.join(guess)

        if base.satisfiable(guess):
            feedback = generate_feedback(guess, solution)
            nGuess += 1
            print(nGuess)
            if feedback == 'g' * len(solution):
                suc += 1
                nGuesses.append(nGuess)
                break
            logic_feedback = feedback_to_logic(guess, feedback)
            base.add(logic_feedback, 50)
    assert(feedback == 'g'*len(solution))
print('Success rate:')
print(suc/N)
print('Average number of guesses: {}'.format(sum(nGuesses)/suc))
print('Maximum number of guesses: {}'.format(max(nGuesses)))


