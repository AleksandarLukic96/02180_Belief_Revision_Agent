from Belief_base import *
from mastermind.User_playing_master_mind import play_master_mind

def error(user_input):
    print(f"No match for: \"{user_input}\"")

if __name__ == "__main__":
    print("Program start")
    print("Type \'exit\' to exit")
    print("Type \'CREATE {NAME}\' to create a belief base with name {NAME}")
    print("Type \'PRINT {NAME}\' to print belief base with name {NAME}")
    print("Type \'EXPAND {NAME} {SENTENCE} {WEIGHT}\' to expand a belief base with name {NAME} with a sentence {SENTENCE} of weight {WEIGHT}")
    print("Type \'CONTRACT {NAME} {SENTENCE}\' to contract a belief base with name {NAME} with a sentence {SENTENCE}")
    print("Type \'REVISION {NAME} {SENTENCE} {WEIGHT}\' to revise a belief base with name {NAME} with a sentence {SENTENCE} of weight {WEIGHT}")

    print("")
    print(
        "Type \'ENTAILS {NAME} {SENTENCE}\' to check wether the belief base with name {NAME} entails the sentence {SENTENCE}")
    print(
        "Type \'SATISFIES {NAME} {SENTENCE}\' to check wether the belief base with name {NAME} satisfies the sentence {SENTENCE}")

    print(
        "\nType \'MASTER MIND\' to play master mind with 6 different colors and pattern length of 4")

    while True:
        user_input = input("Your input: ")

        input_words = user_input.split()
        words = len(input_words)
        if user_input.lower() == "exit":
            print("Thanks for playing")
            break

        elif input_words[0].upper() == "CREATE" and words == 2:
            if not input_words[1].isdigit():
                globals()[input_words[1]] = belief_base()
            else:
                error(user_input)

        elif input_words[0].upper() == "EXPAND" and words == 4:
            name = input_words[1]
            sentence = input_words[2]
            priority_weight = input_words[3]
            if (globals().__contains__(name) and priority_weight.isdigit()):
                globals()[name].add(sentence, priority_weight)
            else:
                error(user_input)

        elif input_words[0].upper() == "CONTRACT" and words == 3:
            name = input_words[1]
            sentence = input_words[2]
            if (globals().__contains__(name)):
                globals()[name].contract(sentence)
            else:
                error(user_input)

        elif input_words[0].upper() == "REVISION" and words == 4:
            name = input_words[1]
            sentence = input_words[2]
            priority_weight = input_words[3]
            if (globals().__contains__(name) and priority_weight.isdigit()):
                globals()[name].revision(sentence, priority_weight)
            else:
                error(user_input)

        elif input_words[0].upper() == "ENTAILS" and words == 3:
            name = input_words[1]
            sentence = input_words[2]
            if (globals().__contains__(name)):
                not_helper = "DOES NOT entail"
                if globals()[name].entails(sentence):
                    not_helper = "entails"
                print(f"The belief base: {name} {not_helper} the sentence: {sentence}")
            else:
                error(user_input)

        elif input_words[0].upper() == "SATISFIES" and words == 3:
            name = input_words[1]
            sentence = input_words[2]
            if (globals().__contains__(name)):
                not_helper = "DOES NOT satisfy"
                if globals()[name].satisfiable(sentence):
                    not_helper = "satisfy"
                print(f"The belief base: {name} {not_helper} the sentence: {sentence}")
            else:
                error(user_input)

        elif input_words[0].upper() == "PRINT" and words == 2:
            name = input_words[1]
            if (globals().__contains__(name)):
                globals()[name].print()
            else:
                error(user_input)

        elif user_input.upper() == "MASTER MIND":
            play_master_mind()

        else:
            error(user_input)

