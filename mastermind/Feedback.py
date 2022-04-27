"""
Functions for generating rules and feedback for the game Mastermind to use with a belief base.
"""
import random
import itertools
from utils import *


def generate_feedback(guess, solution):
    # Generates the feedback for a given guess with a given solution, used when playing automatically.
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
    # Used for translating the feedback for a given guess into the logical statements,
    # that can be added to the belief base.
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


def generate_rules(colors, fields):
    # generate_rules(colors, fields): Function to generate rules in the form of logical sentences to be added
    # to the belief base given list of colors and number of fields in the game.
    rules = []
    for i in range(1, fields+1):
        rules.append('|'.join(list(map('_'.join, list(itertools.product(*[colors, [str(i)]]))))))
        rule = ''
        if len(colors) == 2:
            rule += '-'+colors[0]+'_'+str(i)+'|-'+colors[1]+'_'+str(i)
            rules.append(rule)
        else:
            for j in range(len(colors)):
                temp = list(map('_'.join, list(itertools.product(*[colors[:j] + colors[j+1:], [str(i)]]))))
                temp = ['-' + x for x in temp]
                rule += '&(' + '|'.join(temp) + ')'
            rules.append(rule[1:])
    return rules
