
import copy
#r_path = r'simplesat_testcases/sat/4.cnf'
import re
import os
import time


def read_file(filepath):
        
    with open(filepath) as f:
        samp_cnf_lines = f.readlines()
    
    comments = []
    config = []
    clauses = []
    temp_row = []
    
    for row in samp_cnf_lines:
        row = row.rstrip('\n')
        row = row.lstrip()
        row = re.sub(' +', ' ', row)
        row_split= row.split(' ')
        #print(row_split)
        if row_split[0]=='c':
            comments.append(row_split)
        elif row_split[0]=='p':
            config=row_split
        else:
            if row_split[-1] !='0':
                temp_row += row_split
            else:
                clauses.append(row_split[:-1])
                temp_row = []
    return config[2], config[3], clauses
            


def unit_propagate(literal,clause_list, var_dict):
    
    literal_ref,assignment_bool = (literal,True) if literal[0]!='-' else (literal[1:],False)
    var_dict[literal_ref]=assignment_bool
    
    return [clause for clause in clause_list if literal not in clause]
    
def assign_pure_literal(literal,clause_list):
    inverse_literal = '-'+literal if literal[0]!='-' else literal[1:]
    #print(literal,inverse_literal,clause_list,"lil")
    #print([len(x) for x in clause_list])
    a = [[l1 for l1 in clause if l1 != inverse_literal] for clause in clause_list]
    #print(a,"clmin")
    #print([len(x) for x in a])
    return a

def check_null_clause(clause_list):
    #print("h1",clause_list)
    #if len(clause_list) == 0:
    #    return True
    for clause in clause_list:
        if len(clause) == 0:
            return True
    return False
    
def negate_literal(l1):
    
    if l1[0]=="-":
        return l1[1:]
    else:
        return "-"+l1
    
    
    
def choose_literal(clause_list):  
    for clause in clause_list:
        for l1 in clause:
            #print("cl1nl",clause_list,"l11",l1)
            return l1

def DPLL(clause_list, var_dict):
    nc_list = copy.deepcopy(clause_list)
    #-print(nc_list, time.time())
    #time.sleep(10)
    while True:
        c_lengths = [len(x) for x in nc_list]
        #print("cl",c_lengths)
        if 1 in c_lengths:
            prop_literal = nc_list[c_lengths.index(1)][0]
            #print(prop_literal, "pl1")
            nc_list = unit_propagate(prop_literal,nc_list,var_dict)
            nc_list = assign_pure_literal(prop_literal, nc_list)
        else:
            break
    
    #print("out of while", nc_list)
    if check_null_clause(nc_list):
        #print("F2")
        return False
    #print(nc_list, len(nc_list),"prr")
    if len(nc_list) == 0:
        #print("t2")
        return True
    
    next_literal = choose_literal(nc_list)
    negate_next_literal = negate_literal(next_literal)
    #print("nl",next_literal)
    cnf_branch1 = nc_list + [[next_literal]]
    
    dpll_split_left = DPLL(cnf_branch1,var_dict)
    
    if not dpll_split_left:
        cnf_branch2 = nc_list + [[negate_next_literal]]
        #print("PP1", cnf_branch1,"pp2",cnf_branch2)
        dpll_split_right = DPLL(cnf_branch2,var_dict) 
        #print("h112",ret_val)
        return dpll_split_right
   
    return dpll_split_left 

def variable_dict_generation(clause_list):
    
    flat_list = set([item if item[0]!='-' else item[1:] for sublist in clause_list for item in sublist ])
    
    var_dict = {x:"" for x in flat_list}
    
    return var_dict

#%%

if __name__ == "__main__":
        
    r_path = r'simplesat_testcases/sat/3.cnf'
    
    yes_path = "aim_sat/yes"
    
    no_path = "aim_sat/no"
    yes_sat_list = os.listdir(yes_path)
    no_sat_list = os.listdir(no_path)
    
    yes_sat_list.sort()
    no_sat_list.sort()
    
    
    for sat_name in yes_sat_list:
        #time.sleep(2)
        r_path = os.path.join(yes_path, sat_name)
        variables_n, clause_n, clauses = read_file(r_path)
        if variables_n == "100" or variables_n == '200':
            continue
        print("variable number {0}, clause number {1}, filename {2}".format(variables_n,clause_n,sat_name))    
        var_dict = variable_dict_generation(clauses)
        
        sat_state = DPLL(clauses, var_dict)
        print("SAT State = ",sat_state)
        if sat_state:
            print("Mismatch!")