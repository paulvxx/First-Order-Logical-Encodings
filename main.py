"""
Main python program to run scripts
"""

from powers_of_two_example import powers_of_two_gen, powers_of_two_lin_index_gen
from fibonacci_example import fibonacci_gen
from utils import utils, fol_string_encoder

fibonacci = False

if fibonacci:
    #h_iList, v_iList = powers_of_two_gen.gen_powers_of_two_cycle_model(5)
    h_iList, v_iList = fibonacci_gen.gen_fibonacci_encoding_model(10)

    print(f"Number of State Combinations present : {utils.get_state_count_adj_mappings(h_iList, v_iList)}")

    # add starting predicate condition
    cnf_format = [[(1,'a','a',True)]]
    cnf_format.extend(utils.implication_list_to_cnf_AEA(h_iList, v_iList, explicit_disjoint=False))

    formula_str = fol_string_encoder.to_fol_cnf_formula(cnf_format, add_exists_front=True, pretty=True)
    print(formula_str)
else:
    #pack = powers_of_two_gen.gen_powers_of_two_cycle_model(6)
    #print(pack[0])
    #print("")
    pack = powers_of_two_lin_index_gen.gen_powers_of_two_cycle_linear_block_model(6)
    print(pack[0])