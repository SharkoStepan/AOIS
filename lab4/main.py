from logic.table_truth.truth_table import TruthTable
from logic.table_truth.logical_function import LogicalFunction
from logic.minimizer import Minimizer

ODS_SUM_TRUTH_TABLE = [
    # A, B, C, S
    [0, 0, 0, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 1],
]

ODS_CARRY_OUT_TRUTH_TABLE = [
    # A, B, C, P
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
]

D8421_PLUS_2_TRUTH_TABLE = [
    # A, B, C, D, A', B', C', D'
    [0, 0, 0, 0, 0, 0, 1, 0],  # 0 -> 2
    [0, 0, 0, 1, 0, 0, 1, 1],  # 1 -> 3
    [0, 0, 1, 0, 0, 1, 0, 0],  # 2 -> 4
    [0, 0, 1, 1, 0, 1, 0, 1],  # 3 -> 5
    [0, 1, 0, 0, 0, 1, 1, 0],  # 4 -> 6
    [0, 1, 0, 1, 0, 1, 1, 1],  # 5 -> 7
    [0, 1, 1, 0, 1, 0, 0, 0],  # 6 -> 8
    [0, 1, 1, 1, 1, 0, 0, 1],  # 7 -> 9
    [1, 0, 0, 0, 0, 0, 0, 0],  # 8 -> don't care
    [1, 0, 0, 1, 0, 0, 0, 0],  # 9 -> don't care
    [1, 0, 1, 0, 0, 0, 0, 0],  # 10 -> don't care
    [1, 0, 1, 1, 0, 0, 0, 0],  # 11 -> don't care
    [1, 1, 0, 0, 0, 0, 0, 0],  # 12 -> don't care
    [1, 1, 0, 1, 0, 0, 0, 0],  # 13 -> don't care
    [1, 1, 1, 0, 0, 0, 0, 0],  # 14 -> don't care
    [1, 1, 1, 1, 0, 0, 0, 0],  # 15 -> don't care
]

def main():
    # ODS-3 Sum
    sum_truth_table = TruthTable(table=ODS_SUM_TRUTH_TABLE, variables=["A", "B", "C"])
    print("Sum Truth Table:")
    sum_truth_table.display()
    sum_pcnf = sum_truth_table.get_pcnf()
    print("Sum PCNF: ", sum_pcnf)

    sum_pcnf_logical_function = LogicalFunction(sum_pcnf)
    sum_pcnf_truth_table = TruthTable(logical_function=sum_pcnf_logical_function)
    minimized_sum_pcnf = Minimizer(sum_pcnf_truth_table).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=True
    )
    print("Minimized Sum PCNF: ", minimized_sum_pcnf)

    print("------------------------------------------------------")

    # ODS-3 Carry Out
    carry_out_truth_table = TruthTable(
        table=ODS_CARRY_OUT_TRUTH_TABLE, variables=["A", "B", "C"]
    )
    print("Carry Out Truth Table:")
    carry_out_truth_table.display()
    carry_out_pcnf = carry_out_truth_table.get_pcnf()
    print("Carry Out PCNF: ", carry_out_pcnf)

    carry_out_pcnf_logical_function = LogicalFunction(carry_out_pcnf)
    carry_out_pcnf_truth_table = TruthTable(
        logical_function=carry_out_pcnf_logical_function
    )
    minimized_carry_out_pcnf = Minimizer(
        carry_out_pcnf_truth_table
    ).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=True)
    print("Minimized Carry Out PCNF: ", minimized_carry_out_pcnf)

    print("------------------------------------------------------")

    # D8421+2 Output A'
    d8421_plus_2_truth_table_a = TruthTable(
        table=list(map(lambda x: x[:4] + [x[4]], D8421_PLUS_2_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_2_pcnf_a = Minimizer(d8421_plus_2_truth_table_a).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=True
    )
    print("Minimized D8421 Plus 2 PCNF A': ", minimized_d8421_plus_2_pcnf_a, end="\n\n")

    # D8421+2 Output B'
    d8421_plus_2_truth_table_b = TruthTable(
        table=list(map(lambda x: x[:4] + [x[5]], D8421_PLUS_2_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_2_pcnf_b = Minimizer(d8421_plus_2_truth_table_b).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=True
    )
    print("Minimized D8421 Plus 2 PCNF B': ", minimized_d8421_plus_2_pcnf_b, end="\n\n")

    # D8421+2 Output C'
    d8421_plus_2_truth_table_c = TruthTable(
        table=list(map(lambda x: x[:4] + [x[6]], D8421_PLUS_2_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_2_pcnf_c = Minimizer(d8421_plus_2_truth_table_c).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=True
    )
    print("Minimized D8421 Plus 2 PCNF C': ", minimized_d8421_plus_2_pcnf_c, end="\n\n")

    # D8421+2 Output D'
    d8421_plus_2_truth_table_d = TruthTable(
        table=list(map(lambda x: x[:4] + [x[7]], D8421_PLUS_2_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_2_pcnf_d = Minimizer(d8421_plus_2_truth_table_d).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=True
    )
    print("Minimized D8421 Plus 2 PCNF D': ", minimized_d8421_plus_2_pcnf_d, end="\n\n")

if __name__ == "__main__":
    main()