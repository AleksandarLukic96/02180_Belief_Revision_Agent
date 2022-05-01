import sys
# setting path
sys.path.append('../02180_BELIEF_REVISION_AGENT')

from Belief_base import belief_base
from utils import divide_sentence
from inference import entails, satisfiable


def success(belief_base, sentence):
    print(f'Does the sentence {sentence} already entail from the belief base?')
    print(belief_base.entails(sentence))
    print('Revise with sentence')
    belief_base.revision(sentence, 50)
    print(f'Does the sentence {sentence} now entail from the belief base?')
    entails = (belief_base.entails(sentence))
    print(entails)
    if entails:
        print('Success is satisfied.')
    else:
        print('Success is  NOT satisfied.')


def inclusion(b_b, sentence):
    print('Is the sentence satisfiable in the belief base?')
    print(b_b.satisfiable(sentence))
    belief_base_add = b_b.copy()
    print('Perform revision and expansion seperately')
    b_b.revision(sentence, 100)
    belief_base_add.add(sentence, 100)
    print('Is revised belief base a subset of the expanded belief base?')
    if set([C[i] for C in b_b.CNF for i in range(len(C))]).issubset(set([C[i] for C in belief_base_add.CNF for i in range(len(C))])):
        print('True. Inclusion is satisfied')
    else:
        print('False. Inclusion is NOT satisfied')

def vacuity(b_b, sentence):
    print(f'Is the negated sentence -({sentence}) entailed from the belief base?')
    print(b_b.entails('-(' + sentence + ')'))
    belief_base_add = b_b.copy()
    print('Perform revision and expansion seperately')
    b_b.revision(sentence, 100)
    belief_base_add.add(sentence, 100)
    print('Are the resulting belief bases equal?')
    if b_b.CNF == belief_base_add.CNF:
        print('True. Vacuity is satisfied')
    else:
        print('False. Vacuity is NOT satisfied')


def consistency(b_b, sentence):
    print(f'Is sentence {sentence} consistent?')
    print(satisfiable([], sentence))
    print(f'Performs revision with sentence {sentence}.')
    b_b.revision(sentence, 100)
    print('Is the revised belief base consistent?')
    check = b_b.satisfiable(b_b.CNF[0][0])
    if check:
        print('True. Consistency is satisfied.')
    else:
        print('False. Consistency is NOT satisfied.')

def extensionality(b_b, sentence):
    print('Is sentence a tautology?')
    print(entails([], sentence))
    sentence = sentence.split('<->')
    b_b2 = b_b.copy()
    print('Performs revisions seperately.')
    b_b.revision(sentence[0], 100)
    b_b2.revision(sentence[1], 100)
    print('Are the resulting belief bases equal?')
    if b_b.CNF == b_b2.CNF:
        print('True. Extensionality is satisfied')
    else:
        print('False. Extensionality is NOT satisfied')


# Test cases found by inserting logical formulas in WolframAlpha using BooleanConvert[..., 'CNF']
test1 = ['B<->(P_1|Q)', '-B|P_1|Q', 'B|-P_1', '-Q|B']
test2 = ['-(S&(T|Q))->M', 'S|M', 'T|Q|M']
test3 = ['(P|(R&(S|T)))', 'P|R', 'P|S|T']
test4 = ['(P|(R&-(S_1|T)))', 'P|R', 'P|-S_1', 'P|-T']
test5 = ['(P|(R&((S&(U|A))|T)))', 'P|R', 'P|S|T', 'P|U|A|T']
test6 = ['a->(s->(d<->m))', '-a|-s|-d|m', '-a|-s|-m|d']
test7 = ['(a->(s|(t->h)))&((s->w)|q)', '-a|s|-t|h', '-s|w|q']
test8 = ['(a->((s|(t->h_1))&(s->w)))|q', '-a|s|-t|h_1|q', '-a|-s|w|q']
test9 = ['(a<->s_1)->(t_1->(a<->(s_1<->m)))', 'a|m|s_1|-t_1', 'm|-a|-s_1|-t_1']

test = [test1, test2, test3, test4, test5, test6, test7, test8, test9]

x = belief_base()

for i in range(len(test)):
    x.add(test[i][0], i+1)
    for j in range(len(test[i])-1):
        try:
            assert set([part for part in divide_sentence(test[i][j+1]) if part != '|']) in [set(n for n in divide_sentence(m[i]) if n != '|') for m in x.CNF for i in range(len(m))], f'Failed on test {i+1}. Expected CNF form not found in belief base. Added belief: {test[i][0]}. Expected CNF part: {test[i][j+1]}'
        except AssertionError:
            x.print()
            assert set([part for part in divide_sentence(test[i][j+1]) if part != '|']) in [set(n for n in divide_sentence(m[i]) if n != '|') for m in x.CNF for i in range(len(m))], f'Failed on test {i+1}. Expected CNF form not found in belief base. Added belief: {test[i][0]}. Expected CNF part: {test[i][j+1]}'
print('Success:\n')
success(x, 'p&q')
print('\n Inclusion:\n')
inclusion(x, '-p&q')
print('\n Vacuity:\n')
vacuity(x, '-(w|s)')
print('\n Consistency:\n')
consistency(x, '(P&Q)|(P->Q)')
print('\n Extensionality:\n')
extensionality(x, '(a->b)<->(-a|b)')

