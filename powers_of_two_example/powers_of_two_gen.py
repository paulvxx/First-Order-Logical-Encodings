from utils.utils import read_implications_from_diagonals

"""
A cycle/sequence enumeration routine that enumerates
aperiodic increasing powers of two cycles 
"""
def gen_powers_of_two_cycle_model(full_iters : int):
    """
    A cycle/sequence enumeration routine that generates dynamically expanding, 
    aperiodic cycles to encode powers of two for origin-less computation on a 
    2-D grid.
    
    When the total number of required states (or tiles) to represent this 
    exponential growth is initially unknown in general, this routine serves as a discovery tool. 
    By running the deterministic expansion for a sufficient number of iterations, 
    it exhausts all early-developing dynamic cases and tracks emergent global 
    behavior. This seamlessly determines the necessary state count and 
    constructs the final first-order logical formula (adjacency implications) 
    required for the model.
    
    Algorithm Phases:
        - Phase 1: Applies a bijective structural mapping to the current dynamic 
          cycle, transitioning the base states into a set of auxiliary/transitional 
          states
        - Phase 2: Applies branching non-deterministic mappings to the auxiliary 
          states and concatenates the results. This explicitly doubles 
          the sequence length per iteration, capturing the powers-of-two exponential 
          growth

    Args:
        full_iters (int): The number of iterations to perform of the dynamic 
                          cycle expansion.

    Returns:
        tuple: A tuple containing two dictionaries representing the final formula:
            - horizontal_implications (dict): Maps a given state to a set of 
              valid horizontally adjacent states
            - vertical_implications (dict): Maps a given state to a set of 
              valid vertically adjacent states
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