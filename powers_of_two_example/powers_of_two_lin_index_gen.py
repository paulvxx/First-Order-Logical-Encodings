from utils.utils import read_implications_from_diagonals

"""
A cycle/sequence enumeration routine that enumerates
aperiodic increasing powers of two cycles with linearly increasing
blocks
"""
def gen_powers_of_two_cycle_linear_block_model(full_iters : int):
    """
    Generates first-order constraints for power-of-two cycles containing linearly expanding sub-blocks.

    Extends the 1D diagonal-anchored power-of-two model by embedding a linear run 
    of length n - 1 (state 'L') within each cycle period of length 2^n. The 
    generator tracks bi-adjacency state pairs across two intermediate auxiliary 
    sequences to forward-propagate transition markers and increment the linear run.

    Phases per iteration:
        1. Adjacency Pairing: Computes pairwise boundary states and appends a prime 
           marker ('P') to the first non-linear state.
        2. Marker Propagation: Replicates the auxiliary cycle and shifts 'P' to 
           the terminal linear state to bridge successive horizons.
        3. Doubled Re-encoding: Applies homomorphic homomorphisms that expand the 
           linear block by 1 while doubling the total periodic length.

    Args:
        full_iters (int): Number of expansion and doubling cycles to execute.

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
                               3:{"L","C"}, 
                               4:{"B","D"}
                               }
    vertical_implications = {0:{0}, 
                             1:{0}, 
                             2:{0}, 
                             3:{2}, 
                             4:{1}, 
                             "L":{4}, 
                             "B":{3}, 
                             "C":{4}, 
                             "D":{3}
                             }
    diagonal_sequences = [
        [1,2],
        [3,4],
        ["L","B","C","D"]
    ]
    # current sequence and corresponding length 
    current_sequence = ["L","B","C","D"]
    clen = 4
    # linear index to track the end of the linear block
    linear_index = 1

    # begin the dynamically expanding sequences iteration
    for _ in range(full_iters):

        # Calculate the first auxillary sequence
        next_sequence = []
        for i in range(clen-1):
            next_sequence.append(current_sequence[i] + current_sequence[i+1])
        # wrap around logic
        next_sequence.append(current_sequence[clen-1] + current_sequence[0])
        # append the "P" (' prime marker) at the first non-linear block (non L) state
        next_sequence[linear_index] = next_sequence[linear_index] + "P"

        # read off horizontal and vertical implications
        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )
        # store the next value in the diagonal sequence list,
        # update the current cycle
        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        # Calculate the second auxillary sequence
        # make a copy of the current sequence
        next_sequence = current_sequence.copy()
        # Modify the last linear state (linear_index-1) and append
        # the "P" (' prime marker) at the first non-linear block (non L) state
        next_sequence[linear_index-1] = next_sequence[linear_index-1] + "P"

        # read off horizontal and vertical implications
        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )
        # store the next value in the diagonal sequence list,
        # update the current cycle
        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        # apply string mappings to generate the next doubled-length cycle
        next_sequence_1 = []
        next_sequence_2 = []
        for i in range(clen-1):
            # The latter condition (current_sequence[i][-1]=="P")
            # allows the linear sequence to expand
            if current_sequence[i][0]=="L" or current_sequence[i][-1]=="P":
                next_sequence_1.append("L")
            else:
                next_sequence_1.append("A")
            next_sequence_2.append("C")
        # handle the last cycle elements separately (reduces in-loop branching)
        next_sequence_1.append("B")
        next_sequence_2.append("D")

        # Append the results of the two applied mappings together
        next_sequence = next_sequence_1 + next_sequence_2

        # read off horizontal and vertical implications
        read_implications_from_diagonals(
            horizontal_implications, 
            vertical_implications,
            current_sequence,
            next_sequence
        )
        # store the next value in the diagonal sequence list,
        # update the current cycle
        diagonal_sequences.append(next_sequence)
        current_sequence = next_sequence
        next_sequence = []

        # update the current length and the linear index
        clen *= 2
        linear_index += 1

    # Return the diagonal sequences and the final list of implications
    return (diagonal_sequences, horizontal_implications, vertical_implications)