import random
from scipy.stats import random_table
from gmpy2 import mpq
import os
from bdd import BDD, BDDNode
import math
import sys

"""
Generates random formulae with a given number of variables and clauses.
Arguments for execution are:
1. num_variables: Number of variables in the formulae
2. ratio_variable_clauses: Ratio of variables to clauses in the formulae
3. num_formulas: Number of formulae to generate
4. dest_path: Path to the file where results will be saved
"""

class formula_generator:
    @staticmethod
    def generate_formulas(num_variables: int, ratio_variable_clauses: float, num_formulas: int, dest_path: str , num_literals: int = 3) -> list[str]:
        contingency_tables = formula_generator.generate_contingency_tables(num_variables)
        variables = list(contingency_tables.keys())
        formulas = []
        #generate formula
        i = 1
        while i <= num_formulas:
            #print(f"{i}: \n")
            formula = ""
            #generate clause
            num_clauses = int(ratio_variable_clauses * num_variables)
            for j in range(1, num_clauses + 1):
                formula = formula + "("
                used_vars = []
                #generate variable
                for k in range(1, num_literals+1):
                    variable = random.randint(1, num_variables)
                    while variable in used_vars:
                        variable = random.randint(1, num_variables)
                    used_vars.append(variable)
                    
                    if bool(random.getrandbits(1)):
                        formula = formula + "not "
                    formula = formula + f"X{variable} or "
                    
                #delete last or
                formula = formula [:-4]
                formula = formula + ") and "
                
            #delete last and
            formula = formula[:-5]
            
            satisfiable = formula_generator.check_formula(formula, variables, dest_path)
            if not satisfiable:
                i = i - 1
            i+=1
            print(f"{num_formulas - i + 1} left")
            #formulas.append(formulas)
        return formulas
    
    @staticmethod
    def generate_contingency_tables(num_variables: int):
        contingency_tables = {}
        for i in range(1, num_variables + 1):
            #avoid too little numbers as they can lead to paths having a probability of 0%
            first_row_sum = random.randint(5, 95)
            second_row_sum = 100 - first_row_sum
            
            first_col_sum = random.randint(5, 95)
            second_col_sum = 100 - first_col_sum
            
            row = [first_row_sum, second_row_sum]
            col = [first_col_sum, second_col_sum]
            table = random_table.rvs(row, col)
            
            #print(table)
            first = int(table[0][0])
            second = int(table[0][1])
            third = int(table[1][0])
            fourth = int(table[1][1])
            
            contingency_tables[f"X{i}"] = [mpq(first,100), mpq(second,100), mpq(third,100), mpq(fourth,100)]
        return contingency_tables
    
    @staticmethod
    def check_formula(formula: str, variables: list[str], dest_path: str):
        bdd = BDD(formula, variables)
        path = dest_path
        out = open(path, "a")
        i = 0
        if bdd.satisfiable:
            out.write(formula + "\n")
            print(f"new satisfiable formula found.")
        else: print("formula not satisfiable.")
        out.close()
        return bdd.satisfiable
        
if __name__ == "__main__":
    num_variables = int(sys.argv[1])
    num_formulae = int(sys.argv[2])
    ratio = float(sys.argv[3])
    dest_path = sys.argv[4]
    formulas = formula_generator.generate_formulas(num_variables, ratio, num_formulae, dest_path)
    
    
    #for i in range(0, 100):
    #    c = formula_generator.generate_contingency_tables(5)
    #    for x in c:
    #        sum = c[x][0]+  c[x][1]+  c[x][2]+  c[x][3]
    #        print(c[x])
    #        print("\n")
    #        print(sum)
    #    print("\n\n-----------")