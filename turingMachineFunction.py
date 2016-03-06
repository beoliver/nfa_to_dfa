
import sys

def run_turing_machine(path, inputString, verbose=False):

    transitions = {}
    with open(path, 'rU') as f:
        start = f.readline().strip()
        accept = f.readline().strip()
        reject = f.readline().strip()
        for line in f:
            line = line.strip().split(" ")
            assert len(line) == 5
            transitions[(line[0],line[1])] = ((line[2],line[3]),line[4])

    tape = list(inputString)
    tape.append('_') # add an explicit blank to the end of the tape
    tape_head = 0
    state = start
    while True:
        if verbose == True:
            print ' '.join(tape)
        try:
            ((new_state, rewrite), direction) = transitions[(state, tape[tape_head])]
            # break if we have found a terminal state
            if (new_state == accept) or (new_state == reject):
                break
            # if we are at the end of the tape, add an extra blank to the tape (tape_head + 1)
            if tape_head == len(tape):
                tape.append('_')
            # re-write at tape head position
            tape[tape_head] = rewrite
            # update state
            state = new_state
            # We can always move right (we append '_' every loop when required)
            if direction == 'R':
                tape_head += 1
                continue
            # test that we are not moving left when at 0
            if tape_head > 0 :
                tape_head -= 1
        except KeyError:
            break # can not possibly be in accept state

        return new_state == accept

if __name__ == '__main__':

    args = sys.argv
    verbose = False

    if len(args) <= 2:
        print("<filepath> <string> [-v]")

    if len(args) == 3 and args[2] == "-v":
        verbose = True

    print(run_turing_machine(args[1], args[2],verbose))
