
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

    # add start states
    visited   = {nfa.start}
    remaining = list(visited)
    while remaining != []:
        state = remaining.pop()
        try:
            transitions = nfa.transitions[(state,"epsilon")]
            for t in transitions:
                if t not in visited:
                    visited.add(t)
                    remaining.append(t)            
        except KeyError:
            continue
    dfa.start = visited
    assert dfa.start in dfa.states

    # add finish states
    for f_state in nfa.finish:
        for state_set in dfa.states:
            if f_state in state_set:
                dfa.finish.add(state_set)

    # add transitions
    mappings  = {}
    remaining = []
    for state in nfa.states:
        for word in nfa.alphabet:
            # (state, word) -> state
            try:
                transition_set = set(nfa.transitions[(state,word)])
                # print (state, word, transition_set)
                # now we need to check and follow epsilon transitions:
                remaining = list(transition_set)
                visited = set()
                while remaining != []:
                    s = remaining.pop()
                    try:
                        epsilon_transitions =  nfa.transitions[(s, "epsilon")]
                        # print "epsilon transitions"
                        # print (state, word, s, epsilon_transitions)
                        for et in epsilon_transitions:
                            if et not in visited:
                                visited.add(et)
                                # transition_set.add(et)
                                remaining.append(et)
                    except KeyError:
                        continue
                transition_set |= visited
                mappings[(state,word)] = transition_set
            except KeyError:
                # print (state, word, "{}")
                # add a transition to the empty set
                mappings[(state,word)] = set()
                
    # mappings has the transitions from the single states
        for word in nfa.alphabet:
            for state_set in dfa.states:
                dfa.transitions[(state_set,word)] = set()                
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


    


# examples

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


dfa2 = nfa2.make_dfa()
dfa2.simplify()
