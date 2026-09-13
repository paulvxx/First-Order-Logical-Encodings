from utils.utils import read_implications_from_diagonals

"""
A cycle/sequence enumeration routine that enumerates
aperiodic fibonacci length blocks inside power of two cycle expansions
"""
def gen_fibonacci_encoding_model(full_iters : int):
    """
    Generates first-order logic constraints encoding Fibonacci-length runs in power-of-two cycles.

    Builds an originless model anchored along the main diagonal (Y = X) to simulate 
    additive sequences. Because Fibonacci growth is non-multiplicative, the routine 
    embeds consecutive terms into a power-of-two cyclic scaffold by coordinating 
    state variables via iterative rotational alignment, additive fusion, and 
    homomorphic doubling.

    Phases per iteration:
        1. Bi-primitive Pairing: Concatenates primitive states into 2-character 
           rotational seeds.
        2. Rotational Alignment: Iteratively shifts the sequence leftward until 
           boundary markers ('AF'/'BF') align the active Fibonacci blocks.
        3. Additive Fusion: Collapses aligned pairs into auxiliary sum states 
           (G, H, I, J) capturing the sequence recurrence.
        4. Capacity Doubling: Expands auxiliary states into doubled primitive cycles, 
           preventing register overflow for subsequent terms.

    Args:
        full_iters (int): Number of complete Fibonacci summation and doubling 
            rounds to simulate.

    Returns:
        tuple: A 3-element tuple containing:
            - diagonal_sequences (list[list[Any]]): History of state sequences 
              along successive sub-diagonals (Y = X + a).
            - horizontal_implications (dict[Any, set[Any]]): Mapping of state 
              P(z, x) to allowed right-adjacent states P(z, y).
            - vertical_implications (dict[Any, set[Any]]): Mapping of state 
              P(x, z) to allowed down-adjacent states P(y, z).
    """
    horizontal_implications = {1:{5}, 
                               2:{6}, 
                               3:{7}, 
                               4:{8},
                               5:{"A"},
                               6:{"D"},
                               7:{"E"},
                               8:{"F"}
                               }
    vertical_implications = {0:{0}, 
                             1:{0}, 
                             2:{0}, 
                             3:{0}, 
                             4:{0}, 
                             5:{2}, 
                             6:{3}, 
                             7:{4}, 
                             8:{1}
                             }
    diagonal_sequences = [
        [1,2,3,4],
        [5,6,7,8],
        ["A","D","E","F"]
    ]
    current_sequence = ["A","D","E","F"]

    # relevant character mapping tables for cycle doubling
    m1 = {"G":"A", "H":"B", "I":"C", "J":"D"}
    m2 = {"G":"E", "H":"E", "I":"E", "J":"F"}

    # current sequence length
    clen = 4

    for _ in range(full_iters):
        #print(f"Current Sequence : {current_sequence}")
        # Phase 1 , transition from primitive states A-F to adjacent two string representations
        next_sequence = []
        for index in range(clen):
            if index != clen-1: 
                next_sequence.append(current_sequence[index] + current_sequence[index+1])
            else: 
                next_sequence.append(current_sequence[index] + current_sequence[0])

        # read off implications
        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )

        # store the next value in the diagonal sequence list
        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        # Phase 2-3 Loop (rotation alignment)
        jump_to_phase_4 = False

        while not jump_to_phase_4:
            # Assume we are at phase 2 at the beginning of the while loop
            # neither "AF" nor "BF" (implying the cycles are fully rotated) are 
            # in the current cycle sequence so rotation needs to continue
            # For First-Order control flow to hold, it is good to note that 
            # we would specify this using the presence of predicate/state pairs "CF", "DF", and "EF"
            # rather than the absense of pairs "AF" and "BF" 
            # since one-way implications (P --> Q) are generally insufficient to control negation
            # behavior ~P. (i.e. you would need more fine-grained logic (P --> Q) && (~P --> R) && ~(Q && R))
            if not len({"AF","BF"}.intersection(set(current_sequence))):
                # Type 2 to Type 3
                for index in range(clen):
                    if index != clen-1: 
                        next_sequence.append(current_sequence[index] + current_sequence[index+1])
                    else: 
                        next_sequence.append(current_sequence[index] + current_sequence[0])

                read_implications_from_diagonals(
                    horizontal_implications, 
                    vertical_implications,
                    current_sequence,
                    next_sequence
                )

                diagonal_sequences.append(next_sequence)
                current_sequence = next_sequence
                next_sequence = []

                # Type 3 to Type 2
                for index in range(clen):
                    # apply the mapping to string xyzw --> xw
                    # retrieve the first and last characters 
                    # then concatenate them
                    first = current_sequence[index][0]
                    last = current_sequence[index][3]
                    next_sequence.append(str(first + last))

                read_implications_from_diagonals(
                    horizontal_implications, 
                    vertical_implications,
                    current_sequence,
                    next_sequence
                )

                diagonal_sequences.append(next_sequence)
                current_sequence = next_sequence
                next_sequence = []
            # Rotation has finished, here
            else:
                jump_to_phase_4 = True

        # Phase 2 --> Phase 4
        # map rotated cycles to first characters Fibonacci expansions
        for index in range(clen):
            # retrieve first and last characters
            first = current_sequence[index][0]
            last = current_sequence[index][1]
            # map rotational alignments to Phase 4 characters
            if first=='A' or first=='B':
                next_sequence.append("G")
            elif last=='A':
                next_sequence.append("H")                
            elif first=='F':
                next_sequence.append("J")
            else:
                next_sequence.append("I")

        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )

        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        # Phase 4 --> Phase 1
        # obtain the next sequence by applying two mappings and
        # concatenate the results
        # doubling phase
        next_sequence_1 = []
        next_sequence_2 = []
        for i in range(clen):
            next_sequence_1.append(m1[current_sequence[i]])
            next_sequence_2.append(m2[current_sequence[i]])            

        # order doesn't matter
        next_sequence = next_sequence_1 + next_sequence_2

        # double sequence length count
        clen *= 2

        # read off implications
        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )

        # store the next value in the diagonal sequence list
        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        #print(f"New Sequence : {current_sequence}")
        #print("Updated Implication List : ")
        #print(f" Horizontal : {horizontal_implications} ")
        #print(f" Vertical : {vertical_implications} ")
        #print("-----------------------------")

    return (diagonal_sequences, horizontal_implications, vertical_implications)