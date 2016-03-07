#!/usr/bin/env python
import sys


def run_turing_machine(path, inputString, verbose=False):
    transitions = {}
    with open(path, 'rU') as f:
        start = f.readline().strip()
        accept = f.readline().strip()
        reject = f.readline().strip()
        assert accept != reject
        for line in f:
            line = line.strip().split(" ")
            assert len(line) == 5
            transitions[(line[0],line[1])] = ((line[2],line[3]),line[4])
    tape = list(inputString) + ['_'] # add an explicit blank to the end of the tape
    tape_head = 0
    state = start
    while True:
        if verbose:
            tape_pre  = ' '.join(tape[:tape_head])
            tape_at   = " [" + tape[tape_head] + "] "
            tape_post = ' '.join(tape[tape_head+1:])
            if tape_head > 0:
                tape_pre = " " + tape_pre
            print(tape_pre + tape_at + tape_post)            
        ((state, rewrite), direction) = transitions.get((state, tape[tape_head]), ((reject,'_'),'L'))
        if state in [accept, reject]:
            return state == accept
        if tape_head == len(tape)-1:
            tape.append('_') # pretend the list is infinite
        tape[tape_head] = rewrite
        if direction == 'R':
            tape_head += 1
        elif tape_head > 0:
            tape_head -= 1




if __name__ == '__main__':

    args = sys.argv
    v = False

    if len(args) < 3:
        print("<filepath> <string> [--verbose]")
        sys.exit()

    if len(args) == 4:
        if args[3] == "-v" or args[3] == "--verbose":
            v = True

    print(run_turing_machine(args[1], args[2], verbose=v))


# an example file

# q0
# accept
# reject
# q0 0 q1 _ R
# q1 _ accept _ R
# q1 x q1 x R
# q1 0 q2 x R
# q2 _ q4 _ L
# q2 x q2 x R
# q2 0 q3 0 R
# q3 x q3 x R
# q3 0 q2 x R
# q4 _ q1 _ R
# q4 x q4 x L
# q4 0 q4 0 L

# an example input

# ./turingMachine.py ~/Path/To/File.txt 0000 --verbose

