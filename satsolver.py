import random


#def read_sudoku(filepath=None):

sudoku_size = 4
filepath =None

if filepath:
    pass

else:
    print("random sudoku")

    with open("testcases/{0}x{0}.txt".format(sudoku_size)) as f:
        sudoku_list = f.readlines()


rules_path = 'rules/sudoku-rules-{0}x{0}.txt'.format(sudoku_size)



test_sudoku = sudoku_list[2]
print(test_sudoku)
sudoku_dict = {str(i):{str(j): test_sudoku[(i-1)*sudoku_size+j-1] for j in range(1,sudoku_size+1)} for i in range(1,sudoku_size+1)} 


def sudoku_dict_to_cnf(s_dict):

    p_clauses = []
    
    for i in range(1,sudoku_size+1):
        for j in range(1,sudoku_size+1):
            cell_val_t = s_dict[str(i)][str(j)] 
            if cell_val_t != '.':
                p_clauses.append([str(i)+str(j)+cell_val_t])

    return p_clauses

puzzle_clauses = sudoku_dict_to_cnf(sudoku_dict)



def sudoku_cnf_to_normal(clause_var_dict):
    
    true_list = [key_val for key_val, bool_val in clause_var_dict.items() if bool_val]
    true_list.sort()
    
    index_list = [x[:-1] for x in true_list]
    val_list = [x[-1] for x in true_list]
    val_nested = [ val_list[i:i+sudoku_size] for i in range(0,len(val_list),sudoku_size)]
    print(index_list, val_list,"\n")
    [print(*a) for a in val_nested]
    

from sat_funcs import *

variables_n, clause_n, rules_clauses = read_file(rules_path)

clauses = rules_clauses + puzzle_clauses
var_dict = variable_dict_generation(clauses)

DPLL(clauses,var_dict)

sudoku_cnf_to_normal(var_dict)



