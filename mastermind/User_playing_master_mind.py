import sys
# setting path
sys.path.append('../02180_BELIEF_REVISION_AGENT')

"""
Script for Mastermind playing with user feedback using belief base for timing and finding number of guesses needed.
"""
from Belief_base import belief_base
from mastermind.Feedback import *

def play_master_mind():
    nGuesses = []
    print("You are playing master mind with 6 colours and 4 pegs")
    colors = ['r', 'g', 'y', 'b', 'w', 'p']  # Possible colors
    print(f"Make a code of the following colors: {colors}")
    print("Remember your solution and provide feedback to the computers guesses:\n")


    fields = 4
    rules = generate_rules(colors, fields)
    base = belief_base()

    for rule in rules:
        base.add(rule, 100)
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
            nGuess += 1
            print(f"The computers guess number {nGuess}: ")
            print(guess.replace("&", "\n").replace("_", " on "))
            print("")
            feedback = input("Give your response of 4 chararcters (r, g or o): ")
            print("Thinking...")
            if feedback == 'gggg':
                # If the guess is correct, stop game
                nGuesses.append(nGuess)
                guess = guess.replace("&", "\n").replace("_", " on ")
                print(f"The code was: \n{guess} \nAnd took {nGuess} tries.")
                print("Thanks for playing")
                break
            # Transform feedback to logic and add it to the belief base
            logic_feedback = feedback_to_logic(guess, feedback)
            base.add(logic_feedback, 50)