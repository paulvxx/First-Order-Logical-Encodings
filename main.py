#!/usr/bin/env python3
"""
Command-Line Interface for First-Order Logic (FOL) Sequence Encodings.

This script acts as the primary entry point to generate formal first-order logic 
sentences for dynamically expanding cycle models.
"""

import argparse
import sys

# Standardized imports as requested
from powers_of_two_example import powers_of_two_gen, powers_of_two_lin_index_gen
from fibonacci_example import fibonacci_gen
from utils import utils, fol_string_encoder

def main():
    parser = argparse.ArgumentParser(
        description="Generate First-Order Logic encodings for computational sequences.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Positional command for model selection
    parser.add_argument(
        "model",
        choices=["powers_of_two", "linear_blocks", "fibonacci"],
        help="The target sequence model to generate constraints for."
    )

    # Optional flag for mutual exclusion
    parser.add_argument(
        "-d", "--disjoint",
        action="store_true",
        help="Enforce explicit mutual exclusion clauses (e.g., ~(A && B))."
    )

    # Optional flag to disable pretty printing (defaults to True)
    parser.add_argument(
        "--no-pretty",
        action="store_false",
        dest="pretty",
        help="Disable pretty-printing and output the formula on a single line."
    )

    args = parser.parse_args()

    # 1. Route the command to the appropriate generator
    print(f"--- Generating FOL Encodings for: {args.model} ---")
    
    if args.model == "fibonacci":
        iters = 8
        _, h_impl, v_impl = fibonacci_gen.gen_fibonacci_encoding_model(iters)
    elif args.model == "powers_of_two":
        iters = 6
        _, h_impl, v_impl = powers_of_two_gen.gen_powers_of_two_cycle_model(iters)
    elif args.model == "linear_blocks":
        iters = 6
        _, h_impl, v_impl = powers_of_two_lin_index_gen.gen_powers_of_two_cycle_linear_block_model(iters)
    else:
        print("Invalid model selected.")
        sys.exit(1)

    # 2. Extract and print state count metrics
    state_count = utils.get_state_count_adj_mappings(h_impl, v_impl)
    print(f"Number of State Combinations present: {state_count}")

    # 3. Initialize the existential anchor requirement
    cnf_format = [[(1, 'a', 'a', True)]]

    # 4. Serialize implications into CNF clauses
    cnf_clauses = utils.implication_list_to_cnf_AEA(
        h_impl, 
        v_impl, 
        explicit_disjoint=args.disjoint
    )
    cnf_format.extend(cnf_clauses)

    # 5. Format and print the final formula
    formula_str = fol_string_encoder.to_fol_cnf_formula(
        cnf_format, 
        add_exists_front=True, 
        pretty=args.pretty
    )
    
    print("\n[ Final First-Order Logic Formula ]")
    print(formula_str)


if __name__ == "__main__":
    main()