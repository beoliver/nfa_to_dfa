
import itertools


def powerset_generator(s):
    for i in xrange(len(s)+1):
        for j in itertools.combinations(s, i):
            yield frozenset(j)

# nfa to dfa

class NFA(object):
    alphabet = set()
    states = set()
    transitions = dict()
    start = 0
    finish = set()
    def make_dfa(self):
        return nfa_to_dfa(self)

class DFA(NFA):
    def simplify(self):
        simplify_dfa(self)


def nfa_to_dfa(nfa):
    
    dfa = DFA()

    dfa.alphabet = nfa.alphabet

    # add states
    dfa.states = set(powerset_generator(nfa.states))
    
    # find and add start states
    dfa.start = {nfa.start}
    remaining = list(dfa.start)
    while remaining != []:
        next_state = remaining.pop()
        epsilon_transitions =  nfa.transitions.get((next_state, "epsilon"), set())
        for transition in epsilon_transitions:
            if transition not in dfa.start:
                dfa.start.add(transition)
                remaining.append(transition)
    
    # add finish states
    for (state, state_set) in itertools.product(nfa.finish, dfa.states):
        if state in state_set:
            dfa.finish.add(state_set)

    # add transitions    
    mappings = {}
    
    for state_word_pair in itertools.product(nfa.states, nfa.alphabet):
        transition_set = nfa.transitions.get(state_word_pair, set())
        remaining = list(transition_set)
        visited   = set()
        while remaining != []:
            next_state = remaining.pop()
            epsilon_transitions =  nfa.transitions.get((next_state, "epsilon"), set())
            for transition in epsilon_transitions:
                if transition not in visited:
                    visited.add(transition)
                    remaining.append(transition)
        mappings[state_word_pair] = transition_set | visited

    for (state_set, word) in itertools.product(dfa.states, nfa.alphabet):
        # mappings has the transitions from the single state s
        dfa.transitions[(state_set, word)] = set()
        for state in state_set:
            try:
                m = mappings[(state, word)]
                dfa.transitions[(state_set,word)] |= m
            except KeyError:
                continue
    return dfa



def simplify_dfa(dfa):
    keep = {}
    vals = dfa.transitions.values()
    finish = set()
    for ((s,a),t) in dfa.transitions.items():
        if (s in vals) and (s in dfa.finish):
            keep[(s,a)] = t
            finish.add(s)
        elif (s in vals):
            keep[(s,a)] = t
    dfa.transitions = keep
    dfa.finish = finish


    


# nfa = NFA()
# nfa.alphabet = {"a","b"}
# nfa.states = {1,2,3}
# nfa.transitions = {(2,"a") : {2,3}, (2,"b") : {3}, (3,"a") : {1},
#                    (1,"b") : {2}, (1,"epsilon") : {3}}
# nfa.start = 1
# nfa.finish = {1}


# dfa = nfa.make_dfa()
# dfa.simplify()



    
nfa2 = NFA()
nfa2.alphabet = {"a","b"}
nfa2.states = {1,2}
nfa2.transitions = {(1,"a") : {1,2}, (1,"b") : {2}, (2,"b") : {1}}
nfa2.start = 1
nfa2.finish = {1}


dfa3 = nfa2.make_dfa()
dfa3.simplify()
