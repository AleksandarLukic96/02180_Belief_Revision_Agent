import random
import itertools
from utils import simplify, divide_sentence, move_negation, is_false, distribute
from Belief_base import belief_base

def generate_feedback(guess, solution):
    solution = solution.copy()
    guess = guess.split('&')
    guess = [x[0] for x in guess]

    feedback = ''
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            feedback += 'g'
            solution[i] = '...'
            guess[i] = ',,,'
    for i in range(len(guess)):
        if guess[i] in solution:
            feedback += 'o'
        elif solution[i] != '...':
            feedback += 'r'
    return ''.join(random.sample(feedback, k=len(feedback)))


def feedback_to_logic(guess, feedback):
    guess = guess.split('&')
    Gs = list(itertools.permutations(list(range(1, len(guess)+1)), r=feedback.count('g')))
    outer = []
    for G in Gs:
        not_G = [x for x in range(1, len(guess)+1) if x not in G]
        phi_g = '&'.join([guess[x-1] for x in G]) + '&' + '&'.join(['-'+guess[x-1] for x in not_G])
        if phi_g[0] == '&':
            phi_g = phi_g[1:]
        if phi_g[-1] == '&':
            phi_g = phi_g[:-1]
        Os = list(itertools.permutations(not_G, r=feedback.count('o')))
        inner = []
        for O in Os:
            R = [x for x in range(1, len(guess)+1) if x not in G and x not in O]
            temp = ['('+'|'.join([guess[x-1][0]+'_'+str(y) for y in not_G if y != x]) + ')' for x in O]
            while '()' in temp:
                temp.remove('()')
            phi_o = '&'.join(temp)
            if phi_o != '' and phi_o[0] == '&':
                phi_o = phi_o[1:]
            if phi_o != '' and phi_o[-1] == '&':
                phi_o = phi_o[:-1]
            phi_r = '&'.join(['-' + guess[x-1][0] + '_' + str(y) for x in R for y in not_G if y!=x])
            s1 = ''
            if phi_o != '':
                s1 += '('+phi_o + ')'
            s1 += '&'
            if phi_r != '':
                s1 += '(' + phi_r+')'
            if s1 != '' and s1[0] == '&':
                s1 = s1[1:]
            if s1 != '' and s1[-1] == '&':
                s1 = s1[:-1]
            if s1 != '':
                s1 = '(' + s1 + ')'
                inner.append(s1)
        s2 = ''
        if phi_g != '':
            s2 += '('+phi_g + ')'
        s2 += '&'
        if len(inner) > 0:
            s2 += '(' + '|'.join(inner)+')'
        if s2 != '' and s2[0] == '&':
            s2 = s2[1:]
        if s2 != '' and s2[-1] == '&':
            s2 = s2[:-1]
        if s2 != '':
            s2 = '(' + s2 + ')'
            outer.append(s2)
    return '|'.join(outer)

def simplify_feedback(feedback):
    parts = divide_sentence(feedback)
    new_parts = []
    for part in parts:
        if part == '|':
            continue
        clauses = [x for x in divide_sentence(simplify(part)) if x != '&']
        literals = clauses[:-1]
        phis = divide_sentence(simplify(clauses[-1]))
        new_phis = []
        for phi in phis:
            if phi == '|':
                continue
            new_phi = []
            x = divide_sentence(phi)
            for w in x:
                new_w = []
                if w == '&':
                    continue
                if '|' in w:
                    for atom in divide_sentence(w):
                        if atom == '|':
                            continue
                        elif atom in literals:
                            break
                        elif move_negation('-'+atom) in literals:
                            continue
                        else:
                            new_w.append(atom)
                    if new_w != '':
                        new_phi.append('('+'|'.join(new_w)+')')
                elif w in literals:
                    continue
                elif move_negation('-' + w) in literals:
                    new_phi = []
                    break
                else:
                    new_phi.append(w)
            if new_phi != '':
                temp = simplify('&'.join(new_phi))
                if not is_false(temp):
                    new_phis.append('('+remove_duplicates_and(temp)+')')
        if new_phis != '':
            new_parts.append('(('+'&'.join(literals)+')&('+'|'.join(new_phis)+'))')
    return '|'.join(new_parts)


def remove_duplicates_and(sentence):
    parts = ['('+part+')' for part in divide_sentence(sentence) if part != '&']
    return '&'.join(list(set(parts)))

if __name__ == '__main__':
    feedback = '((r_1&-s_2&-y_3&-y_4)&((((s_3|s_4)&(y_2|y_4))&(-y_2&-y_3))|(((s_3|s_4)&(y_2|y_3))&(-y_2&-y_4))|(((y_2|y_4)&(s_3|s_4))&(-y_2&-y_3))|(((y_2|y_4)&(y_2|y_3))&(-s_3&-s_4))|(((y_2|y_3)&(s_3|s_4))&(-y_2&-y_4))|(((y_2|y_3)&(y_2|y_4))&(-s_3&-s_4))))|((s_2&-r_1&-y_3&-y_4)&((((r_3|r_4)&(y_1|y_4))&(-y_1&-y_3))|(((r_3|r_4)&(y_1|y_3))&(-y_1&-y_4))|(((y_1|y_4)&(r_3|r_4))&(-y_1&-y_3))|(((y_1|y_4)&(y_1|y_3))&(-r_3&-r_4))|(((y_1|y_3)&(r_3|r_4))&(-y_1&-y_4))|(((y_1|y_3)&(y_1|y_4))&(-r_3&-r_4))))|((y_3&-r_1&-s_2&-y_4)&((((r_2|r_4)&(s_1|s_4))&(-y_1&-y_2))|(((r_2|r_4)&(y_1|y_2))&(-s_1&-s_4))|(((s_1|s_4)&(r_2|r_4))&(-y_1&-y_2))|(((s_1|s_4)&(y_1|y_2))&(-r_2&-r_4))|(((y_1|y_2)&(r_2|r_4))&(-s_1&-s_4))|(((y_1|y_2)&(s_1|s_4))&(-r_2&-r_4))))|((y_4&-r_1&-s_2&-y_3)&((((r_2|r_3)&(s_1|s_3))&(-y_1&-y_2))|(((r_2|r_3)&(y_1|y_2))&(-s_1&-s_3))|(((s_1|s_3)&(r_2|r_3))&(-y_1&-y_2))|(((s_1|s_3)&(y_1|y_2))&(-r_2&-r_3))|(((y_1|y_2)&(r_2|r_3))&(-s_1&-s_3))|(((y_1|y_2)&(s_1|s_3))&(-r_2&-r_3))))'
    new_feedback=simplify(simplify_feedback(feedback))
    print(list(distribute('(-s_4&y_2&-s_3)|(-s_4&(y_2|y_3)&(y_2|y_4)&-s_3)')))
    x=belief_base()
    x.add(new_feedback,100)
