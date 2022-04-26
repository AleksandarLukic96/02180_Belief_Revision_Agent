from Belief_base import belief_base
from utils import divide_sentence

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
test10 = ['(P|R)->S']

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

print('All test passed. Resulting belief base:\n')
x.print()
x.add('-S&-M',100)