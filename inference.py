"""
Functions for logic inference.

The logic syntax used is the following:
or: |
and: &
implies: ->
biimplication: <->
not: -
Parentheses are assumed to be used everywhere where two different operators appear, except for the not operator
"""
from CNF import to_CNF


def DPLL_satisfiable(clauses, sentence):
    # Function for using the DPLL algorithm to determine if a sentence in CNF is satisfiable given a belief base,
    # represented as a list of clauses in CNF.
    if isinstance(sentence, list):
        for element in sentence:
            clauses.append(element)
    else:
        clauses.append(sentence)
    symbols = find_symbols(clauses)
    return DPLL(clauses, symbols, {})


def DPLL(clauses, symbols, model):
    # Function for finding if a model exist where the list of clauses in CNF, containing the symbols, is true.
    temp = check(clauses, model)
    if temp == 1:
        return True
    if temp == -1:
        return False
    P, value = find_pure_symbol(clauses, symbols, model)
    if P is not None:
        new_model = model.copy()
        new_model[P] = value
        new_symbols = symbols.copy()
        new_symbols.remove(P)
        return DPLL(clauses, new_symbols, new_model)
    P, value = find_unit_clause(clauses, model)
    if P is not None:
        new_model = model.copy()
        new_model[P] = value
        new_symbols = symbols.copy()
        new_symbols.remove(P)
        return DPLL(clauses, new_symbols, new_model)
    P = symbols[0]
    new_modelT = model.copy()
    new_modelT[P] = True
    new_modelF = model.copy()
    new_modelF[P] = False
    new_symbols = symbols.copy()
    new_symbols.remove(P)
    return DPLL(clauses, new_symbols, new_modelT) or DPLL(clauses, new_symbols, new_modelF)


def entails(base, sentence):
    # Function for determining if a logic sentence entails from a belief base consisting of a list of clauses in CNF.
    return not satisfiable(base, '-(' + sentence+')')


def satisfiable(base, sentence):
    # Function for determining if a sentence is satisfiable given a belief base consisting of a list of clauses in CNF.
    return DPLL_satisfiable(base, to_CNF(sentence))


def check(clauses, model):
    # check(clauses, model): Function for checking whether a list of clauses in CNF is true, false or undertermined
    # under the truth assignments in the dict model.
    # -1: one false
    # 0: some undetermined
    # 1: all true
    nTrue = 0 # Counts number of true clauses
    for clause in clauses:
        literals = clause.split('|')
        nFalse = 0 # Counts number of false literals in clause
        for i in range(len(literals)):
            if literals[i][0] == '-' and literals[i][1:] in model:
                if model[literals[i][1:]] == False:
                    # If a negated symbol is false in model, the clause is true
                    nTrue += 1
                    break
                else:
                    # Else the literal is false
                    nFalse += 1
            elif literals[i] in model:
                if model[literals[i]] == True:
                    # A true, non-negated symbol makes the clause true
                    nTrue += 1
                    break
                else:
                    # Else the literal is false
                    nFalse += 1
        if nFalse == len(literals):
            # If all literals are false, the clause is false
            return -1
    if nTrue == len(clauses):
        # If all clauses are true
        return 1
    else:
        return 0


def find_symbols(clauses):
    # Function for finding a list of symbols occuring in the list of clauses in CNF
    symbols = []
    for clause in clauses:
        literals = clause.split('|')
        for literal in literals:
            if literal[0] == '-':
                symbols.append(literal[1:])
            else:
                symbols.append(literal)
        symbols = list(set(symbols))
    return symbols


def find_pure_symbol(clauses, symbols, model):
    # Function for finding a pure symbol and it's truth assignment in the list of clauses in CNF in the model
    for symbol in symbols:
        sign = 0 # Sign seen for symbol
        pure = True
        for clause in clauses:
            if check([clause], model) == 1:
                # If the clause is already true in the model, it does not matter
                continue
            literals = clause.split('|')
            if symbol in literals:
                if sign == -1:
                    # If a non-negated symbol has been seen as negated before, it is not pure
                    pure = False
                    break
                sign = 1  # Else, sign is seen as positive
                continue
            elif '-'+symbol in literals:
                if sign == 1:
                    # If a negated symbol has been seen as non-negated before, it is not pure
                    pure = False
                    break
                sign = -1  # Else, sign is seen as negative
                continue
        if pure and sign != 0:
            # If a pure symbol is found, return it with the truth assignment to it
            return symbol, True if sign == 1 else False
    return None, 0


def find_unit_clause(clauses, model):
    # Function for finding a unit clause in the list of clauses in CNF in the model
    for clause in clauses:
        if check([clause], model) == 1:
            # If the clause is already true in the model, it does not matter
            continue
        literals = clause.split('|')
        idx = list(range(len(literals)))
        for i in range(len(literals)):
            if literals[i][0] == '-':
                if literals[i][1:] in model and model[literals[i][1:]] == True:
                    idx.remove(i)
                    # If negated symbol is true, it cannot make the clause true
            else:
                if literals[i][1:] in model and model[literals[i][1:]] == False:
                    # If non-negated symbol is false, it cannot make the clause true
                    idx.remove(i)
        clause = '|'.join([literals[i] for i in idx])
        if '|' not in clause:
            # If the clause consists only of one literal, return it with the truth assignment
            # to the only symbol appearing
            if '-' not in clause:
                return clause, True
            return clause[1:], False
    return None, 0
