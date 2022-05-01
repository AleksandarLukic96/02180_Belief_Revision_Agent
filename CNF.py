"""
Function to convert a logical sentence into conjunctive normal form.

The logic syntax used is the following:
or: |
and: &
implies: ->
biimplication: <->
not: -
Parentheses are assumed to be used everywhere where two different operators appear, except for the not operator
"""
from utils import *
import itertools


def to_CNF(sentence):
    # Function for converting a sentence into conjunctive normal form, returning a list of the clauses in the CNF
    # The CNF is constructed by first eliminating bi-implications, replacing them with implications.
    # Then implications are removed, then negations are moved so as to only appear with symbols.
    # At last and is distributed over or to make the sentence a conjunction of disjunctions. Returns a list with the
    # conjunctions
    CNF = []
    biimp = simplify(eliminate_biimplications(sentence))
    imp = simplify(eliminate_implications(biimp))
    neg = simplify(move_negation(imp))
    clauses = find_clauses(neg)
    for clause in clauses:
        dis = distribute(simplify(clause))
        for s in dis:
            CNF.append(simplify(s))
    return CNF


def eliminate_biimplications(sentence):
    # Function for eliminating biimplications from a logic sentence by replacing a < ->b with (a->b) & (b->a)
    bi_implications = sentence.split('<->')
    i = 0
    while len(bi_implications) > 1:
        # Identify alpha and beta for a given biimplication
        alpha = bi_implications[i]
        beta = bi_implications[i+1]
        # Find inner parentheses
        if beta.count('(') > beta.count(')'):
            # Make sure to only operate on the innermost of nested biimplications
            i += 1
            continue
        first_part = ''
        last_part = ''
        if alpha.rfind('(') > alpha.rfind(')'):
            # If the biimplication is within a parentheses, only the inner part is used for alpha and beta
            index = alpha.rfind('(')+1
            first_part = alpha[:index]
            alpha = alpha[index:]

            index = find_matching('(' + beta)-1
            last_part = beta[index:]
            beta = beta[:index]
        else:
            # If the alpha or beta is a sentence, only take the sentence
            if alpha[-1] == ')':
                index = len(alpha) - find_matching_rev(alpha)
                first_part = alpha[:index]
                alpha = alpha[index:]
            if beta[0] == '(':
                index = find_matching(beta)+1
                last_part = beta[index:]
                beta = beta[:index]
        # Make replacement
        new = first_part + '(((' + alpha + ')' '->' + '(' + beta + '))' + '&' + '((' + beta + ')' + '->' + '(' + alpha + ')))' + last_part
        del bi_implications[i]
        bi_implications[i] = new
        i = 0
    return bi_implications[0]


def eliminate_implications(sentence):
    # Function for eliminating implications from a logic sentence by replacing a->b with -a|b
    implications = sentence.split('->')
    i = 0
    while len(implications) > 1:
        # Identify alpha and beta for a given implication
        alpha = implications[i]
        beta = implications[i + 1]
        if beta.count('(') > beta.count(')'):
            # Make sure to only operate on the innermost of nested implications
            i += 1
            continue
        first_part = ''
        last_part = ''
        if alpha.rfind('(') > alpha.rfind(')'):
            # If the implication is within a parentheses, only the inner part is used for alpha and beta
            index = alpha.rfind('(')+1
            first_part = alpha[:index]
            alpha = alpha[index:]
            index = find_matching('(' + beta) - 1
            last_part = beta[index:]
            beta = beta[:index]
        else:
            # If the alpha or beta is a sentence, only take the sentence
            if alpha[-1] == ')':
                index = len(alpha) - find_matching_rev(alpha)
                first_part = alpha[:index]
                alpha = alpha[index:]
            if beta[0] == '(':
                index = find_matching(beta)+1
                last_part = beta[index:]
                beta = beta[:index]
        # Make replacement
        new = first_part + '(-' + '(' + alpha + ')' + '|' + '(' + beta + '))' + last_part
        del implications[i]
        implications[i] = new
        i = 0
    return implications[0]


def move_negation(sentence):
    # Function for moving negations in a sentence to have them only appear before symbols, using
    # elimination of double negations and De Morgan rules.
    action_taken = True
    while action_taken:
        # Looping through the sentence, making sure to only do one change each loop through, as to not mess up indexing
        action_taken = False
        for i in range(len(sentence)):
            if sentence[i] == '-':
                # If a negation is found, see if it can be simplified
                # Elimination of double negation
                if sentence[i+1] == '-':
                    sentence = sentence[0:i:] + sentence[i+2::]
                    action_taken = True
                    break
                if sentence[i+1] == '(':
                    id = find_matching(sentence[i:])+i
                    bit = sentence[i+2:id] # Find inner part of negated parentheses
                    parts = divide_sentence(bit)
                    # Elimination of double negation
                    if bit[0] == '-' and len(parts) == 1:
                        sentence = sentence[:i] + bit[1:] + sentence[i+3+len(bit):]
                        action_taken = True
                        break
                    elif bit[0] == '(' and find_matching(bit) == len(bit)-1:
                        # If inner part consists of a closed pair of parentheses, move the negation into the outer pair
                        sentence = sentence[:i] + '(-' + bit + ')' + sentence[i+3+len(bit):]
                        action_taken = True
                        break
                    if '&' in parts:
                        # Move the negation into the parentheses using De Morgan law for conjunctions replacing & with |
                        for j in range(len(parts)):
                            if parts[j] == '&':
                                parts[j] = '|'
                            else:
                                parts[j] = '-(' + parts[j] + ')'
                        sentence = sentence[:i] + '(' + ''.join(parts) + ')' + sentence[i + 3 + len(bit):]
                        action_taken = True
                        break
                    elif '|' in parts:
                        # Move the negation into the parentheses using De Morgan law for disjunctions replacing | with &
                        for j in range(len(parts)):
                            if parts[j] == '|':
                                parts[j] = '&'
                            else:
                                parts[j] = '-(' + parts[j] +')'
                        sentence = sentence[:i] + '(' + ''.join(parts) + ')' + sentence[i + 3 + len(bit):]
                        action_taken = True
                        break
    return sentence


def distribute(sentence):
    # Function for distributing | over & in a sentence, to get it into CNF,
    # assuming the only operators present are -, | and &. Returns list of clauses
    x = divide_sentence(simplify(sentence))
    for i in range(len(x)):
        if x[i] == '|' or x[i] == '&':
            continue
        if ('|' in x[i]) or ('&' in x[i]):
            # Recursively distribute subelements of sentence, if they do not only consist of disjunctions
            x[i] = simplify('&'.join(distribute(x[i])))
    while len(x) > 1:
        # Distribute two disjunctions at a time from left to right
        if x[1] == '|':
            # If the elements are a disjunction, distribute
            parts1 = [x for x in divide_sentence(x[0]) if x!='|' and x !='&']
            parts2 = [x for x in divide_sentence(x[2]) if x!='|' and x !='&']
            parts = list(itertools.product(parts1, parts2)) # Find all combinations for subelements of each element
            temp = ['|'.join(x) for x in parts]

            for t in range(len(temp) - 1, -1, -1):
                # Reduce each resulting disjunction and check if it is either a tautology, or ensured to be true by a
                # smaller disjunction, removing unneeded disjunctions
                temp[t] = remove_duplicates_or(simplify(temp[t]))
                if is_tautology(temp[t]):
                    del temp[t]
                else:
                    for s in range(len(temp)):
                        if s == t:
                            continue
                        if set(temp[s].split('|')).issubset(set(temp[t].split('|'))):
                            del temp[t]
                            break
            for j in range(len(temp)):
                temp[j] = '(' + temp[j] + ')'
            x[0] = '&'.join(temp)
        else:
            # If the elements are a conjunction, collect them
            x[0] = '('+x[0]+')'+'&'+'('+x[2]+')'
        del x[1]
        del x[1]
    # Return list of clauses
    if x[0] != '':
        return ['('+simplify(part)+')' for part in divide_sentence(x[0]) if part !='&']
    else:
        return x[0]