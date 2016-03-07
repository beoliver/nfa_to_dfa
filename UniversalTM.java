import java.util.Arrays;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

class UniversalTM {
    // MAIN FUNCTION
    public static void main(String[] args) throws FileNotFoundException {
        if ( args.length < 3 ) {
            System.out.print("\nCorrect usage:\n\njava ");
            System.out.println("UniversalTM <TM_file> <input_string> <step_max>\n");
            System.out.println("<TM_file>      : file containing TM encoding");
            System.out.println("<input_string> : input to tape");
            System.out.println("<step_max>     : max number of steps\n");
            System.out.println("NOTE: Use underscore '_' as blank when");
            System.out.println("encoding a TM.\n");
            return;
        }

        // NEW TM FROM FILE <TM_file>
        TuringMachine M2 = createTMFromFile(args[0]);

        // INITIAL TAPE CONTENT <input_string>
        M2.initializeTape(args[1].getBytes());

        // RUN TM for at most <step_max> steps
        M2.run(Integer.parseInt(args[2]));
        if ( M2.getState() == -2 ) {
            // ACCEPT
            System.out.println("ACCEPT.");
        } else if ( M2.getState() == -1 ) {
            // REJECT
            System.out.println("REJECT.");
        } else {
            // DID NOT FINISH (DNF)
            System.out.printf("Did Not Finish in %d steps.\n", Integer.parseInt(args[2]));
        }
    }

    private static TuringMachine createTMFromFile(String fileName) throws FileNotFoundException {
        TuringMachine tm = null;
        
        Scanner sc = new Scanner(new File(fileName));
        if ( sc.hasNextInt() ) {
            // Create TM
            tm = new TuringMachine(sc.nextInt());
            // Modify states
            while ( sc.hasNext() ) {
                String line = sc.nextLine();
                String[] data = line.split(" ");
                if ( data.length == 5 ) {
                    int state = Integer.parseInt(data[0]);
                    byte input = (byte) data[1].charAt(0);
                    int newState = Integer.parseInt(data[2]);
                    byte output = (byte) data[3].charAt(0);
                    char dir = data[4].charAt(0);

                    if ( input == (byte) '_' ) {
                        input = (byte) 0;
                    }
                    if ( output == (byte) '_' ) {
                        output = (byte) 0;
                    }

                    tm.modifyState(state, input, newState, output, (dir == 'R'));
                }
            }
        }
        // Return null or created TM
        return tm;
    }
}

class TuringMachine {
    // Tape
    private byte[] tape;
    // Read/write head
    private int rwHeadPos;
    // States
    private State[] states;
    private int numberOfStates;
    private int currentState;

    // CONSTRUCTORS
    public TuringMachine(int numberOfStates) {
        // State array
        this.numberOfStates = numberOfStates;
        this.states = new State[numberOfStates];
        for ( int i = 0; i < numberOfStates; i++ ) {
            this.states[i] = new State(numberOfStates);
        }
        this.currentState = 0;
    }

    // FUNCTIONS
    public void modifyState(int stateNumber, byte inputSymbol, int targetState, byte outputSymbol, boolean direction) {
        // Set transition
        if ( stateNumber < states.length ) {
            states[stateNumber].transitions[inputSymbol].setTransition(targetState, outputSymbol, direction);
        }
    }

    public void initializeTape(byte[] initial) {
        if ( initial.length == 0 ) {
            tape = new byte[32];
        } else {
            tape = Arrays.copyOf(initial, initial.length*2);
        }
    }

    public int stepComputation() {
        // Read transition function
        Transition thisTransition = states[currentState].transitions[tape[rwHeadPos]];
        // Write to tape
        tape[rwHeadPos] = thisTransition.output;
        // Update state
        currentState = thisTransition.state;
        // Move R/W-head
        moveHead(thisTransition.direction);

        // Return current state
        return currentState;
    }

    public int run(int stepLimit) {
        for ( int i = 0; i < stepLimit; i++ ) {
            stepComputation();
            if ( currentState < 0 ) {
                return currentState;
            }
        }
        return currentState;
    }

    public byte[] getTape() {
        return tape;
    }

    public int getState() {
        return currentState;
    }

    private void moveHead(boolean direction) {
        if ( direction ) {
            rwHeadPos++;
            if ( rwHeadPos == tape.length ) {
                tape = Arrays.copyOf(tape, tape.length * 2);
            }
        } else {
            if ( rwHeadPos > 0 ) {
                rwHeadPos--;
            }
        }
    }
}

class State {
    // ===================================
    // STATE CLASS
    //
    // State class contains an array indicating
    // for every input character the character to be written,
    // the R/W-head's move, and the state to go to.
    // By default, every transition is to the REJECT state (-1).
    // ===================================

    // Transition function
    Transition[] transitions;

    // CONSTRUCTORS
    public State(int numberOfStates) {
        this.transitions = new Transition[256];
        for ( int i = 0; i < 256; i++ ) {
            this.transitions[i] = new Transition();
        }
    }
}

class Transition {
    // ===================================
    // TRANSITION CLASS
    // ===================================

    int state; // -1: REJECT state, -2: ACCEPT state
    byte output;
    boolean direction; // false: LEFT, true: RIGHT

    // CONSTRUCTORS
    public Transition() {
        this(-1, (byte) 0, false);
    }

    public Transition(int state, byte output, boolean direction) {
        this.state = state;
        this.output = output;
        this.direction = direction;
    }

    // FUNCTIONS
    public void setTransition(int state, byte output, boolean direction) {
        this.state = state;
        this.output = output;
        this.direction = direction;
    }
}
