import sys


def run_turing_machine(path, input_string, verbose=False):
    transitions = {}
    with open(path, 'rU') as f:
        for line in f:
            line = line.strip().split(" ")
            transitions[(int(line[0]),line[1])] = ((int(line[2]),line[3]),line[4])
    tape = list(input_string) + ['_']  # add an explicit blank to the end of the tape
    tape_head = 0
    state = 0
    while True:
        if verbose: print(' '.join(tape))
        ((state, rewrite), direction) = transitions.get((state, tape[tape_head]), ((-1, '_'), 'L'))
        if state in [-1, -2]:  # -1 -> reject, -2 -> accept
            return state == -2
        if tape_head == len(tape):
            tape.append('_')  # pretend the list is infinite
        tape[tape_head] = rewrite
        if direction == 'R':
            tape_head += 1
        elif tape_head > 0:
            tape_head -= 1


if __name__ == '__main__':

    args = sys.argv
    v = False
    if len(args) < 3:
        print("<file path> <string> [--verbose]")
    if len(args) == 4:
        if args[3] == "-v" or args[3] == "--verbose":
            v = True

    print(run_turing_machine(args[1], args[2], verbose=v))
