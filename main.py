from Belief_base import *
from utils import  *

if __name__ == "__main__":

    print("Program start")
    print("Type \'exit\' to exit")
    print("Type \'CREATE {NAME}\' to create a belief base with name {NAME}")
    print("Type \'PRINT {NAME}\' to print belief base with name {NAME}")
    print("Type \'EXPAND {NAME} {SENTENCE}\' to expand a belief base with name {NAME} with a sentence {SENTENCE}")
    print("Type \'CONTRACT {NAME} {SENTENCE}\' to contract a belief base with name {NAME} with a sentence {SENTENCE}")
    print("Type \'REVISION {NAME} {SENTENCE}\' to revise a belief base with name {NAME} with a sentence {SENTENCE}")

    print("")
    print("Type \'ENTAILS {NAME} {SENTENCE}\' to check wether the belief base with name {NAME} entails the sentence {SENTENCE}")
    print("Type \'SATISFIES {NAME} {SENTENCE}\' to check wether the belief base with name {NAME} satisfies the sentence {SENTENCE}")

    print("\nType \'MASTER MIND {COLORS} {PATTERN LENGTH}\' to play master mind with {COLORS} different colors and pattern length of {PATTERN LENGTH}")


    priority_weight = 1
    while True:
        user_input = input("Your input: ")

        input_words=user_input.split()

        if len(input_words) == 0:
            print(input_words)

        elif user_input.lower() == "exit":
            print("Thanks for playing")
            break

        elif input_words[0].upper() == "CREATE":
            globals()[user_input.split()[1]] = belief_base()

        elif input_words[0].upper() == "EXPAND":
            name = input_words[1]
            sentence = input_words[2]
            globals()[name].add(sentence,priority_weight)

        elif input_words[0].upper() == "CONTRACT":
            name = input_words[1]
            sentence = input_words[2]
            globals()[name].contract(sentence)

        elif input_words[0].upper() == "REVISION":
            name = input_words[1]
            sentence = input_words[2]
            globals()[name].revision(sentence)

        elif input_words[0].upper() == "ENTAILS":
            name = input_words[1]
            sentence = input_words[2]
            not_helper = "DOES NOT entail"
            if globals()[name].entails(sentence):
                not_helper = "entails"
            print(f"The belief base: {name} {not_helper} the sentence: {sentence}")

        elif input_words[0].upper() == "SATISFIES":
            name = input_words[1]
            sentence = input_words[2]
            not_helper = "DOES NOT satisfy"
            if globals()[name].satisfiable(sentence):
                not_helper = "satisfy"
            print(f"The belief base: {name} {not_helper} the sentence: {sentence}")

        elif input_words[0].upper() == "PRINT":
            name = input_words[1]
            globals()[name].print()

        elif user_input.upper() == "MASTER MIND":
            print("Not yet implemented")
            #TODO Implement

        else:
            print(f"No match for: \"{user_input}\"")