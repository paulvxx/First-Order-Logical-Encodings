"""
Utilities for encoding functions from structural format to string-formulas
"""

def format_literal(literal_tuple, capitalize_first_only=False):
    """
    Formats a structured literal tuple into a First-Order Logic atomic string.

    Serializes an internal predicate representation into standard mathematical 
    predicate syntax (e.g., `P_3(z,x)` or `~P_5(z,y)`). Integer symbols are automatically 
    prefixed with 'P_', string symbols are normalized by case, and negative 
    polarity prepends a negation operator.

    Args:
        literal_tuple (tuple[Union[int, str], str, str, bool]): A 4-tuple 
            `(predicate_id, arg1, arg2, sign)` denoting the predicate symbol, 
            its two relational coordinates, and its boolean truth sign.
        capitalize_first_only (bool, optional): If True, capitalizes only the 
            first character of string predicates; otherwise uppercases all. 
            Defaults to False.

    Returns:
        str: Serialized literal string with arguments and optional negation[cite: 8].

    Raises:
        TypeError: If `predicate_id` is neither an integer nor a string[cite: 8].
    """
    pred, arg1, arg2, sign = literal_tuple
    
    # Format the predicate symbol (e.g., 3 -> P_3)
    if isinstance(pred, int):
        pred_str = f"P_{pred}"
    elif isinstance(pred, str):
        if capitalize_first_only: 
            pred_str = f"{pred.capitalize()}"
        else:
            pred_str = f"{pred.upper()}"
    else:
        raise TypeError("Error : Predicate symbol must either be a String or Integer.")
    
    # Prepend negation symbol '~' if sign is False
    negation = "~" if not sign else ""
    return f"{negation}{pred_str}({arg1},{arg2})"


def to_fol_cnf_formula(clauses, add_exists_front=False, wrap_single=False, pretty=False):
    """
    Encodes a clausal collection into an AEA-prefix First-Order Logic sentence[cite: 8].

    Aggregates disjunctive clauses into Conjunctive Normal Form (CNF) under an 
    unbounded $\forall x \exists y \forall z$ quantifier prefix. Supports optional Skolemized 
    origin anchors ($\exists a$) and multi-line indented formatting.

    Args:
        clauses (list[list[tuple[Union[int, str], str, str, bool]]]): Collection 
            of clauses, where each clause is a disjunction of 4-tuple literals.
        add_exists_front (bool, optional): Prepend leading existential quantifier 
            `∃a` to anchor initial state conditions. Defaults to False.
        wrap_single (bool, optional): Force enclosing parentheses around unit 
            clauses containing a single literal. Defaults to False.
        pretty (bool, optional): Format with standard multi-line indentation 
            and logical line breaks. Defaults to False.

    Returns:
        str: Fully qualified First-Order Logic sentence in CNF syntax.
    """
    if not clauses:
        return "∀x∃y∀z { True }"
    
    exists_front = "∃a" if add_exists_front else ""
    clause_strings = []
    for clause in clauses:
        literals = [format_literal(lit) for lit in clause]
        clause_str = " || ".join(literals)
        
        # Wrap in parentheses if there are multiple literals, or if wrap_single is True
        if len(literals) > 1 or wrap_single:
            clause_str = f"({clause_str})"
            
        clause_strings.append(clause_str)
        
    if pretty:
        # Multi-line pretty-printed output
        indent = "  "
        joined_clauses = f"\n{indent}&& ".join(clause_strings)
        return f"{exists_front}∀x∃y∀z {{\n{indent}{joined_clauses}\n}}"
    else:
        # Single-line output
        joined_clauses = " && ".join(clause_strings)
        return f"{exists_front}∀x∃y∀z {{ {joined_clauses} }}"
