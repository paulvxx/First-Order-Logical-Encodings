import math

"""
Shorthand utility to add implication to list
"""
def add_implication_to_list(ilist : list, key, value):
    """
    Inserts a target transition state into an adjacency implication map.

    Maintains a set-valued multimap representing non-deterministic (consequent) implications
    $P_i \to \bigvee P_j$. Initializes a new singleton set if the antecedent 
    key is unseen, or appends to the existing consequent set.

    Args:
        ilist (dict[Any, set[Any]]): Dictionary tracking antecedents to sets of 
            reachable consequent states.
        key (Any): Antecedent state identifier.
        value (Any): Consequent transition state to register.
    """
    if key not in ilist:
        ilist[key] = {value}
    else:
        ilist[key].add(value)

def read_implications_from_diagonals(horizontal_implications : dict, vertical_implications : dict, 
            current_line : list, next_line : list):
    """
    Extracts first-order grid adjacency constraints between consecutive diagonal slices.

    Aligns two periodic sub-diagonals by computing their Least Common Multiple (LCM) 
    period and projects their local boundary relationships into 2D grid implications. 
    Maps horizontal implications $P(z,x) \to P(z,y)$ from parallel positions and 
    vertical implications $P(x,z) \to P(y,z)$ from forward-shifted offsets.

    Args:
        horizontal_implications (dict[Any, set[Any]]): Multimap recording right-adjacent 
            transitions between matching indices.
        vertical_implications (dict[Any, set[Any]]): Multimap recording down-adjacent 
            transitions between index-offset pairs.
        current_line (list[Any]): Periodic state sequence along diagonal $Y = X + a$.
        next_line (list[Any]): Periodic state sequence along successor diagonal $Y = X + a + 1$.

    Raises:
        ValueError: If either diagonal sequence is empty.
    """
    c_len = len(current_line)
    n_len = len(next_line)
    # if either list is empty, raise an exception
    if (c_len * n_len) == 0:
        raise ValueError("Error : Cycle lists must be non-empty")

    c_expanded = current_line
    n_expanded = next_line
    cycle_length = c_len
    # if the lengths are not equal, expand the cycles continuously (least common multiple) until the periods match
    if c_len != n_len:
        cycle_length = math.lcm(c_len, n_len)
        # expand the cycles to have matching lcm periods
        c_expanded = current_line * (cycle_length // c_len)
        n_expanded = next_line * (cycle_length // n_len)

    # read off implications
    for i in range(cycle_length):
        add_implication_to_list(horizontal_implications, c_expanded[i], n_expanded[i])
        if i == cycle_length-1:
            add_implication_to_list(vertical_implications, n_expanded[i], c_expanded[0])
        else:
            add_implication_to_list(vertical_implications, n_expanded[i], c_expanded[i+1])


def get_state_count_adj_mappings(h_implication_list, v_implication_list):
    """
    Calculates the closed signature cardinality across horizontal and vertical implication maps.

    Aggregates the union of all antecedent keys and consequent values across both 
    directional dictionaries to determine the total number of distinct mutually 
    disjoint predicates required by the first-order signature.

    Args:
        h_implication_list (dict[Any, set[Any]]): Horizontal transition multimap.
        v_implication_list (dict[Any, set[Any]]): Vertical transition multimap.

    Returns:
        int: Total count of unique active states across all implication boundaries.
    """
    present_states = set()
    present_states = present_states.union(set(h_implication_list.keys()))
    present_states = present_states.union(set(v_implication_list.keys()))

    horizontal_value_set = set()
    for h in h_implication_list.keys(): horizontal_value_set = horizontal_value_set.union(h_implication_list[h])
    present_states = present_states.union(horizontal_value_set)

    vertical_value_set = set()
    for v in v_implication_list.keys(): vertical_value_set = vertical_value_set.union(v_implication_list[v])
    present_states = present_states.union(vertical_value_set)

    # total number of states / mutually-disjoint predicates
    return len(present_states)


def implication_list_to_cnf_AEA(h_implication_list, v_implication_list, explicit_disjoint=True):
    """
    Synthesizes horizontal and vertical implication mappings into CNF clauses under the AEA prefix.

    Transforms directional transition dictionaries into raw 4-tuple literal clauses 
    applying De Morgan's laws ($A \to \bigvee B_i \equiv \neg A \lor \bigvee B_i$). 
    Optionally appends pairwise exclusion clauses ($\neg P_i \lor \neg P_j$) to guarantee 
    mutual exclusivity across distinct predicates.

    Args:
        h_implication_list (dict[Any, set[Any]]): Horizontal transition multimap 
            $P(z,x) \to P(z,y)$.
        v_implication_list (dict[Any, set[Any]]): Vertical transition multimap 
            $P(x,z) \to P(y,z)$.
        explicit_disjoint (bool, optional): If True, generates explicit pairwise 
            clauses asserting no two distinct predicates hold simultaneously. 
            Defaults to True.

    Returns:
        list[list[tuple[Any, str, str, bool]]]: A list of disjunctive clauses, where 
        each literal is represented as `(predicate, arg1, arg2, sign)`.
    """
    clauses = []

    # horizontal implication clauses
    for h in h_implication_list.keys():
        # demorgan's laws applied to the antecedent
        clause = [(h,'z','x',False)]
        for adj in h_implication_list[h]:
            clause.append((adj,'z','y',True))
        clauses.append(clause)

    # vertical implication clauses
    for v in v_implication_list.keys():
        # demorgan's laws applied to the antecedent
        clause = [(v,'x','z',False)]
        for adj in v_implication_list[v]:
            clause.append((adj,'y','z',True))
        clauses.append(clause)

    # mutually exclusive predicates conditions
    if not explicit_disjoint:
        # avoid listing out the mutually disjoint conditions 
        return clauses
    
    predicates = set(h_implication_list.keys()).union(set(v_implication_list.keys()))
    # iterate through all unordered distinct pairs (a,b) of all predicates (a != b)
    while len(predicates) != 0:
        # select any predicate from the set it if is not empty
        p = next(iter(predicates))
        remaining = predicates.copy()
        # remove it from the set of remaining predicates
        remaining.difference_update({p})
        for r in remaining:
            clause = [(p,'x','z',False), (r,'x','z',False)]
            clauses.append(clause)
        # iterate through the next loop
        predicates = remaining
            
    # return the CNF format of predicate logical formulas
    return clauses
