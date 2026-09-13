from utils.utils import read_implications_from_diagonals

"""
A cycle/sequence enumeration routine that enumerates
aperiodic increasing powers of two cycles 
"""
def gen_powers_of_two_cycle_model(full_iters : int):
    """
    Generates first-order logic adjacency constraints for dynamically expanding power-of-two cycles.

    Constructs an originless computational model over a 2D grid anchored to 
    the main diagonal (Y = X). The routine iteratively expands periodic diagonal 
    slices using homomorphic state substitutions and irreversible phase-out 
    transitions to discover the minimal closed signature and derive all required 
    horizontal and vertical first-order implication clauses.

    Phases per iteration:
        1. Expansion: Applies a deterministic mapping to elevate current base 
           cycle states to auxiliary transitional states.
        2. Doubling: Applies branching non-deterministic substitutions to double 
           the cycle period ($2^n \to 2^{n+1}$) and records new boundary implications.

    Args:
        full_iters (int): Number of doubling iterations to simulate.

    Returns:
        tuple: A 3-element tuple containing:
            - diagonal_sequences (list[list[Any]]): History of state sequences 
              along successive sub-diagonals (Y = X + a).
            - horizontal_implications (dict[Any, set[Any]]): Mapping of state 
              P(z, x) to allowed right-adjacent states P(z, y).
            - vertical_implications (dict[Any, set[Any]]): Mapping of state 
              P(x, z) to allowed down-adjacent states P(y, z).
    """
    horizontal_implications = {1:{3}, 
                               2:{4}, 
                               3:{5,7}, 
                               4:{6,8}
                               }
    vertical_implications = {0:{0}, 
                             1:{0}, 
                             2:{0}, 
                             3:{2}, 
                             4:{1}, 
                             5:{4}, 
                             6:{3}, 
                             7:{4}, 
                             8:{3}
                             }
    diagonal_sequences = [
        [1,2],
        [3,4],
        [5,6,7,8]
    ]
    current_sequence = [5,6,7,8]

    # first mapping
    m1 = {5:9, 6:10, 7:11, 8:12}
    # second two mappings
    m2 = {9:5, 10:5, 11:5, 12:6}
    m3 = {9:7, 10:7, 11:7, 12:8}

    # current sequence length
    clen = 4

    for _ in range(full_iters):
        #print(f"Current Sequence : {current_sequence}")
        next_sequence = []
        for i in range(clen):
            next_sequence.append(m1[current_sequence[i]])

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

        # obtain the next sequence by applying two mappings 
        # and concatenating the result
        next_sequence_1 = []
        next_sequence_2 = []
        for i in range(clen):
            next_sequence_1.append(m2[current_sequence[i]])
            next_sequence_2.append(m3[current_sequence[i]])

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