from utils.utils import read_implications_from_diagonals

"""
A cycle/sequence enumeration routine that enumerates
aperiodic increasing powers of two cycles with linearly increasing
blocks
"""

def gen_powers_of_two_cycle_linear_block_model(full_iters : int):
    """
    This program iterates through dynamically expanding cycles
    of powers of two using simple mapping rules to phase out 
    cycle period anchors, with the additional properties of 
    also enforcing a linearly increasing block at the beggining (or relative
    beginning) of the cycle by detecting certain adjacency pairs to determine
    the end of the current linear block, and expanding it by one (which is 
    detectable using specialized state markers)

    In particular, the construction involves 
    ensuring the length of the linear block (L state) inside a power of two cycle of 
    period 2^n, n > 1, is n-1.
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
                next_sequence_1[i] = "L"
            else:
                next_sequence_1[i] = "A"
            next_sequence_2[i] = "C"
        # handle the last cycle elements separately (reduces in-loop branching)
        next_sequence_1[clen-1] = "B"
        next_sequence_2[clen-1] = "D"

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

    # Return the final list of implications
    return (horizontal_implications, vertical_implications)