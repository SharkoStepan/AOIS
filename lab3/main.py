from log_parser import *
from evaluator import *
from minimizer import *

def main():
    input_str = input("Enter a logical formula: ").strip()
    input_str = remove_spaces(input_str)

    if not is_valid_symbols(input_str):
        print("Error: Invalid symbols in the formula.")
        return

    if not check_parentheses(input_str):
        print("Error: Unbalanced parentheses.")
        return

    variables = extract_variables(input_str)
    tokens = tokenize(input_str)
    if not tokens:
        print("Error: Tokenization failed.")
        return

    postfix = shunting_yard(tokens)

    try:
        truth_table = generate_truth_table(variables, postfix)
        print_truth_table(variables, truth_table)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()