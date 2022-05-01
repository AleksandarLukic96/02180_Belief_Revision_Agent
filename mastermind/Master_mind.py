import sys  
# setting path
sys.path.append('../02180_BELIEF_REVISION_AGENT')

"""
Script for automatic Mastermind playing using belief base for timing and finding number of guesses needed.
"""
from Belief_base import belief_base
import itertools
import random
from Feedback import *
import time


t1 = time.time_ns()
colors = ['r', 'g', 'y', 'b', 'w', 'p'] # Possible colors

fields = 4

rules = generate_rules(colors, fields)

N = 25  # Number of games to play
nGuesses = []
for i in range(N):
    solution = []
    for _ in range(4):
        solution.append(colors[random.randint(0,5)])
    base = belief_base()
    for rule in rules:
        base.add(rule, 100)

    print(f'{i / N * 100:.0f} % complete.')
    # Generate all possible guesses
    pos = [[colors[i] + '_' + str(j) for i in range(len(colors))] for j in range(1, fields + 1)]
    guesses = list(itertools.product(*pos))

    nGuess = 0
    random.shuffle(guesses)  # Ensure random guessing
    while len(guesses) > 0:
        # While a guess is possible
        guess = guesses[0]
        del guesses[0]
        guess = '&'.join(guess)
        if base.satisfiable(guess):
            # If the guess is possible given the known information, make the guess
            feedback = generate_feedback(guess, solution)
            nGuess += 1
            print(nGuess)
            if feedback == 'g' * len(solution):
                # If the guess is correct, stop game
                nGuesses.append(nGuess)
                break
            # Transform feedback to logic and add it to the belief base
            logic_feedback = feedback_to_logic(guess, feedback)
            base.add(logic_feedback, 50)
    assert (feedback == 'g' * len(solution)) # Assert correct solution is found
print('Average number of guesses: {}'.format(sum(nGuesses) / N))
print('Maximum number of guesses: {}'.format(max(nGuesses)))
print('Average time per game [s]:')
print((time.time_ns()-t1)/(N*1e9))