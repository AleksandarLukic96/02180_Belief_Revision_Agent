"""
Utility functions for the belief base.

The logic syntax used is the following:
or: |
and: &
implies: ->
biimplication: <->
not: -
Parentheses are assumed to be used everywhere where two different operators appear, except for the not operator
"""


def surrounded(sentence):
    # Function for determining whether a logic sentence is surrounded by parentheses
    if sentence[0] != '(':
        return False
    open = 0
    for i in range(len(sentence)):
        character = sentence[i]
        if character == '(':
            open += 1
        elif character == ')':
            open -= 1
        if open == 0 and i < len(sentence)-1:
            return False
    return True


def find_clauses(sentence):
    # Function for splitting a logic sentence up in a list of the clauses in it
    open = 0
    indices = []

    for i in range(len(sentence)):
        # Find index of &'s outside parentheses
        character = sentence[i]
        if character == '(':
            open += 1
        elif character == ')':
            open -= 1
        elif character == '&' and open == 0:
            indices.append(i)


    clauses = []
    cur = 0
    for i in range(len(indices)):
        # Divide the sentence at the found &'s
        next = indices[i]
        if surrounded(sentence[cur:next]):
            clauses.append(sentence[cur+1:next-1])
        else:
            clauses.append(sentence[cur:next])
        cur = next+1
    next = len(sentence)
    clauses.append(sentence[cur:next])
    return clauses


def find_matching(sentence):
    # Helper function for finding the mathing end parentheses for the first start parentheses found
    open = 0
    for i in range(len(sentence)):
        character = sentence[i]
        if character == '(':
            open += 1
        elif character == ')':
            open -= 1
            if open == 0:
                return i


def find_matching_rev(sentence):
    # Helper function for finding the matching start parentheses founc for the first end parentheses found when
    # looking from the right
    open = 0
    for i in range(1, len(sentence)+1):
        character = sentence[-i]
        if character == ')':
            open += 1
        elif character == '(':
            open -= 1
            if open == 0:
                if i < len(sentence) and sentence[-i-1] == '-':
                    return i+1
                return i


def divide_sentence(sentence):
    # Function for splitting a logic sentence up in a list of the subelements. Similar to find_clause but can also
    # split into disjunctions, if the sentence is built from them.
    open = 0
    indices = []

    for i in range(len(sentence)):
        # Find index of &'s and |'s outside parentheses
        character = sentence[i]
        if character == '(':
            open += 1
        elif character == ')':
            open -= 1
        elif (character == '&' or character == '|') and open == 0:
            indices.append(i)


    clauses = []
    cur = 0
    for i in range(len(indices)):
        # Divide the sentence at the found operators
        next = indices[i]
        if surrounded(sentence[cur:next]):
            clauses.append(sentence[cur+1:next-1])
        else:
            clauses.append(sentence[cur:next])
        clauses.append(sentence[next])
        cur = next+1
    next = len(sentence)

    clauses.append(sentence[cur:next])
    return clauses


def simplify(sentence):
    # Function for simplifying a logic sentence by removing redundant parentheses, but preserving
    # those splitting different operators.
    while surrounded(sentence):
        # Remove outer parentheses
        sentence = sentence[1:-1]

    parts = divide_sentence(sentence)
    if '|' in parts:
        # If sentence is a disjunction, remove parentheses around other disjunctions
        for i in range(len(parts)):
            if len(parts[i]) > 1:
                # If not looking at an operator
                temp = parts[i]
                temp = simplify(temp)  # Recursively simplify part
                if '|' in divide_sentence(temp):
                    parts[i] = temp
                if '|' not in divide_sentence(temp):
                    # If part is a conjunction, add parentheses to fit syntax
                    parts[i] = '(' + temp + ')'

    elif '&' in parts:
        # If sentence is a conjunction, remove parentheses around other conjunctions
        for i in range(len(parts)):
            if len(parts[i]) > 1:
                # If not looking at an operator
                temp = parts[i]
                temp = simplify(temp)  # Recursively simplify part
                if '&' in divide_sentence(temp):
                    parts[i] = temp
                if '&' not in divide_sentence(temp):
                    # If part is a disjunction, add parentheses to fit syntax
                    parts[i] = '(' + temp + ')'
    sentence = ''.join(parts)

    action_taken = True
    while action_taken:
        # Loop through sentence, looking for redundant parentheses, making sure to only remove one pair
        # at each loop through to not mess up index
        action_taken = False
        for i in range(len(sentence)):
            if sentence[i] == '(':
                id = find_matching(sentence[i:])+i
                if sentence[i+1] == '(':
                    id2 = find_matching(sentence[i+1:])+i+1
                    if id == id2+1:
                        # If two parentheses are surrounding same part, remove one pair
                        sentence = sentence[:i] + sentence[i+1:id] + sentence[id+1:]
                        action_taken = True
                        break
                t = 0
                if sentence[i+1] == '-':
                    t = 1
                op, id = find_next_operator(sentence[i+1+t:])  # Find next non-symbol in sentence
                if op == ')':
                    # If a pair of parentheses is surrounding a single literal, remove them
                    sentence = sentence[:i] + sentence[i+1:i+1+t+id] + sentence[i+t+2+id:]
                    action_taken = True
                    break
    return sentence


def find_next_operator(sentence):
    # Function for finding the next operator or parentheses appearing in a sentence, and the index
    for i in range(len(sentence)):
        characther = sentence[i]
        if characther in ['(', ')', '|', '&']:
            return characther, i
        if characther == '<':
            return '<->', i
        if characther == '-' and sentence[i+1] == '>':
            return '->', i
        elif characther == '-':
            return characther, i
    return '', -1


def is_tautology(sentence):
    # Function for determining if a sentence consisting of disjunctions is a tautology
    parts = divide_sentence(sentence)
    for part in parts:
        if part[0] == '-':
            if part[1:] in parts:
                return True
    return False


def is_false(sentence):
    # Determines if a conjunction is always false
    parts = divide_sentence(sentence)
    for part in parts:
        if part[0] == '-':
            if part[1:] in parts:
                return True
    return False


def remove_duplicates_or(sentence):
    # Removes duplicate symbols in a sentence consisting of disjunctions
    parts = [part for part in divide_sentence(sentence) if part != '|']
    return '|'.join(list(set(parts)))


def remove_duplicates_and(sentence):
    # Removes duplicate symbols in a sentence consisting of conjunctions
    parts = ['('+part+')' for part in divide_sentence(sentence) if part != '&']
    return '&'.join(list(set(parts)))
