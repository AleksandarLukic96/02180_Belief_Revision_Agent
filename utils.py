def to_CNF(sentence):
    CNF = []
    biimp = eliminate_biimplications(sentence)
    biimp = simplify(biimp)
    imp = eliminate_implications(biimp)
    imp = simplify(imp)
    neg = move_negation(imp)
    neg = simplify(neg)
    clauses = find_clauses(neg)
    for clause in clauses:
        dis = distribute(simplify(clause))
        for s in dis:
            for part in s:
                for element in find_clauses(part):
                    CNF.append(element)
    return CNF


def surrounded(sentence):
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
    open = 0
    indices = []

    for i in range(len(sentence)):
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
        next = indices[i]
        if surrounded(sentence[cur:next]):
            clauses.append(sentence[cur+1:next-1])
        else:
            clauses.append(sentence[cur:next])
        cur = next+1
    next = len(sentence)
    clauses.append(sentence[cur:next])
    return clauses


def eliminate_biimplications(sentence):
    bi_implications = sentence.split('<->')
    i = 0
    while len(bi_implications) > 1:
        alpha = bi_implications[i]
        beta = bi_implications[i+1]
        # Find inner parentheses
        if beta.count('(') > beta.count(')'):
            i += 1
            continue
        first_part = ''
        last_part = ''
        if alpha.rfind('(') > alpha.rfind(')'):
            index = alpha.rfind('(')+1
            first_part = alpha[:index]
            alpha = alpha[index:]

            index = find_matching('(' + beta)-1
            last_part = beta[index:]
            beta = beta[:index]
        if surrounded(alpha + beta):
            alpha = alpha[1:]
            beta = beta[:-1]
        new = first_part + '(((' + alpha + ')' '->' + '(' + beta + '))' + '&' + '((' + beta + ')' + '->' + '(' + alpha + ')))' + last_part
        del bi_implications[i]
        bi_implications[i] = new
        i = 0
    return bi_implications[0]


def eliminate_implications(sentence):
    implications = sentence.split('->')
    i = 0
    while len(implications) > 1:
        alpha = implications[i]
        beta = implications[i + 1]
        if beta.count('(') > beta.count(')'):
            i += 1
            continue
        first_part = ''
        last_part = ''
        if alpha.rfind('(') > alpha.rfind(')'):
            index = alpha.rfind('(')+1
            first_part = alpha[:index]
            alpha = alpha[index:]
            index = find_matching('(' + beta) - 1
            last_part = beta[index:]
            beta = beta[:index]
        else:
            if alpha[-1] == ')':
                index = len(alpha) - find_matching_rev(alpha)
                first_part = alpha[:index]
                alpha = alpha[index:]
            if beta[0] == '(':
                index = find_matching(beta)+1
                last_part = beta[index:]
                beta = beta[:index]
        if surrounded(alpha + beta):
            alpha = alpha[1:]
            beta = beta[:-1]
        new = first_part + '(-' + '(' + alpha + ')' + '|' + '(' + beta + '))' + last_part
        del implications[i]
        implications[i] = new
        i = 0
    return implications[0]


def find_matching(sentence):
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
    open = 0
    indices = []

    for i in range(len(sentence)):
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


def move_negation(sentence):
    # Move negations into literals, as step 3 on page 245.
    # Importantly, there must be parentheses at all places where junctions and disjuntions appear together
    action_taken = True
    while action_taken:
        action_taken = False

        for i in range(len(sentence)):
            if sentence[i] == '-':
                # Double negation
                if sentence[i+1] == '-':
                    sentence = sentence[0:i:] + sentence[i+2::]
                    action_taken = True
                    break
                if sentence[i+1] == '(':
                    id = find_matching(sentence[i:])+i
                    bit = sentence[i+2:id]
                    parts = divide_sentence(bit)
                    # Double negation
                    if bit[0] == '-' and len(parts) == 1:
                        sentence = sentence[:i] + bit[1:] + sentence[i+3+len(bit):]
                        action_taken = True
                        break
                    elif bit[0] == '(' and find_matching(bit) == len(bit)-1:
                        sentence = sentence[:i] + '(-' + bit + ')' + sentence[i+3+len(bit):]
                        action_taken = True
                        break
                    if '&' in parts:
                        for j in range(len(parts)):
                            if parts[j] == '&':
                                parts[j] = '|'
                            else:
                                parts[j] = '-(' + parts[j] + ')'
                        sentence = sentence[:i] + '(' + ''.join(parts) + ')' + sentence[i + 3 + len(bit):]
                        action_taken = True
                        break
                    elif '|' in parts:
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
    parts = [part for part in divide_sentence(sentence) if part != '|']
    for i in range(len(parts)):
        if len(parts[i]) > 1:
            if surrounded(parts[i]):
                parts[i] = parts[i][1:-1]
            parts[i] = [part for part in divide_sentence(parts[i]) if part != '&']
    for combination in combinations(*parts):
        clauses = [simplify('|'.join(combination))]
        action_taken = True
        while action_taken:
            action_taken = False
            for i in range(len(clauses)):
                if '&' in clauses[i]:
                    temp = distribute(clauses[i])
                    del clauses[i]
                    for j in temp:
                        if not is_tautology(j[0]):
                            clauses.append(remove_duplicates(j[0]))
                    action_taken = True
                    break
        yield clauses


def simplify(sentence):
    while surrounded(sentence):
        sentence = sentence[1:-1]

    parts = divide_sentence(sentence)
    if '|' in parts:
        for i in range(len(parts)):
            if len(parts[i]) > 1:
                temp = parts[i]
                temp = simplify(temp)
                if '|' in divide_sentence(temp):
                    parts[i] = temp
                if '|' not in divide_sentence(temp):
                    parts[i] = '(' + temp + ')'

    elif '&' in parts:
        for i in range(len(parts)):
            if len(parts[i]) > 1:
                temp = parts[i]
                temp = simplify(temp)
                if '&' in divide_sentence(temp):
                    parts[i] = temp
                if '&' not in divide_sentence(temp):
                    parts[i] = '(' + temp + ')'
    sentence = ''.join(parts)

    action_taken = True
    while action_taken:
        action_taken = False
        for i in range(len(sentence)):
            if sentence[i] == '(':
                id = find_matching(sentence[i:])+i
                if sentence[i+1] == '(':
                    id2 = find_matching(sentence[i+1:])+i+1
                    if id == id2+1:
                        sentence = sentence[:i] + sentence[i+1:id] + sentence[id+1:]
                        action_taken = True
                        break
                t = 0
                if sentence[i+1] == '-':
                    t = 1
                op, id = find_next_operator(sentence[i+1+t:])
                if op == ')':
                    sentence = sentence[:i] + sentence[i+1:i+1+t+id] + sentence[i+t+2+id:]
                    action_taken = True
                    break
    return sentence


def find_next_operator(sentence):
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


def DPLL_satisfiable(clauses, sentence):
    if isinstance(sentence, list):
        for element in sentence:
            clauses.append(element)
    else:
        clauses.append(sentence)
    symbols = find_symbols(clauses)
    return DPLL(clauses, symbols, {})


def DPLL(clauses, symbols, model):
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


def check(clauses, model):
    # -1: one false
    # 0: some undetermined
    # 1: all true
    nTrue = 0
    for clause in clauses:
        literals = clause.split('|')
        nFalse = 0
        for i in range(len(literals)):
            if literals[i][0] == '-' and literals[i][1:] in model:
                if model[literals[i][1:]] == False:
                    nTrue += 1
                    break
                else:
                    nFalse += 1
            elif literals[i] in model:
                if model[literals[i]] == True:
                    nTrue += 1
                    break
                else:
                    nFalse += 1
        if nFalse == len(literals):
            return -1
    if nTrue == len(clauses):
        return 1
    else:
        return 0


def find_symbols(clauses):
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


def is_tautology(sentence):
    # Determines if a disjunctions of literals is a tautology
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


def remove_duplicates(sentence):
    parts = [part for part in divide_sentence(sentence) if part != '|']
    return '|'.join(list(set(parts)))


def find_pure_symbol(clauses, symbols, model):
    for symbol in symbols:
        sign = 0
        pure = True
        for clause in clauses:
            if check([clause], model) == 1:
                continue
            literals = clause.split('|')
            if symbol in literals:
                if sign == -1:
                    pure = False
                    break
                sign = 1
                continue
            elif '-'+symbol in literals:
                if sign == 1:
                    pure = False
                    break
                sign = -1
                continue
        if pure and sign != 0:
            return symbol, True if sign == 1 else False
    return None, 0


def find_unit_clause(clauses, model):
    for clause in clauses:
        if check([clause], model) == 1:
            continue
        literals = clause.split('|')
        idx = list(range(len(literals)))
        for i in range(len(literals)):
            if literals[i][0] == '-':
                if literals[i][1:] in model and model[literals[i][1:]] == True:
                    idx.remove(i)
            else:
                if literals[i][1:] in model and model[literals[i][1:]] == False:
                    idx.remove(i)
        clause = '|'.join([literals[i] for i in idx])
        if '|' not in clause:
            if '-' not in clause:
                return clause, True
            return clause[1:], False
    return None, 0


def combinations(*parts):
    total_combinations = 1
    for i in range(len(parts)):
        total_combinations *= len(parts[i])

    idx = [0]*len(parts)

    while idx[0] < len(parts[0]):
        yield [parts[i][idx[i]] for i in range(len(idx))]
        idx[-1] += 1
        j = len(idx)-1
        while j > 0:
            if idx[j] >= len(parts[j]):
                idx[j] = 0
                idx[j-1] += 1
                j -= 1
            else:
                if j >= 1 and is_tautology('|'.join([parts[i][idx[i]] for i in range(j+1)])):
                    idx[j] += 1
                    continue
                new_j = -1
                for k in range(1, len(parts)-j):
                    if is_tautology('|'.join([parts[i][idx[i]] for i in range(k+j+1)])):
                        idx[j+k] += 1
                        new_j = j+k
                        break
                if new_j == -1:
                    break
                j = new_j