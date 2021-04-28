import copy
clauses0=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [-1, -2], [-1, -3], [-2, -3], [-4, -5], [-4, -6], [-5, -6], [-7, -8], [-7, -9], [-8, -9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [-1, -4], [-1, -7], [-4, -7], [-2, -5], [-2, -8], [-5, -8], [-3, -6], [-3, -9], [-6, -9], [1, 8], [-1, -8], [4, 2], [-2, -4]]

def load_dimacs(filename):
    with open(filename, 'r') as f:
        l1 = f.readline()
        while l1[0] == 'c':
            l1 = f.readline()
        l1 = l1.split(' ')
        N = int(l1[2])
        M = int(l1[3])
        count = 0
        clause_set = []
        while count < M:
            line = f.readline()
            if line[0] != 'c':
                line_list = line.split(' ')
                count += 1
                clause = []
                # print(line_list)
                for c in line_list:
                    if c != '0' and c != '' and c != '0\n':
                        clause.append(int(c))
                clause_set.append(clause)
        return clause_set, N

def simple_sat_solve(clause_set):
    if clause_set == []:
        return []
    flat_list = []
    for l in clause_set:
        flat_list.extend(l)
    if flat_list == []:
        return False
    flat_set = set(flat_list)
    minimum = min(flat_set)
    maximum = max(flat_set)
    new_max = max(0-minimum, maximum)
    truth_assignment = []
    sat = False
    for i in range(2**new_max):
        binary = f"{i:b}".zfill(new_max)
        truth_assignment = [0-j if binary[j-1] == '0' else j for j in range(1, new_max+1)]
        for clause in clause_set:
            sat = False
            for k in clause:
                if k in truth_assignment:
                    sat = True
                    break
            if sat == False:
                break
        if sat:
            return truth_assignment
    return False

def branching_sat_solve(clause_set, partial_assignment=[]):
    flat_list = []
    for clause in clause_set:
        flat_list.extend(clause)
    variables = set()
    for i in flat_list:
        if i > 0:
            variables.add(i)
        else:
            variables.add(0-i)
    new_clause_set = copy.deepcopy(clause_set)
    # print('1', partial_assignment, new_clause_set)
    for i in partial_assignment:
        if i in variables or 0-i in variables:
            for clause in new_clause_set:
                if i in clause:
                    new_clause_set = list(filter(lambda a: a != clause, new_clause_set))
                elif 0-i in clause:
                    clause.remove(0-i) #do same filter thing above here and hope it works lol
                    # new_clause_set[]
            variables.discard(i)
            variables.discard(0-i)
    # print('2', partial_assignment, new_clause_set)
    if variables == set():
        if new_clause_set == []:
            return partial_assignment
        else:
            return False
    branch_var = list(variables)[0]
    positive_partial_assignment = copy.copy(partial_assignment)
    negative_partial_assignment = copy.copy(partial_assignment)
    positive_partial_assignment.append(branch_var)
    negative_partial_assignment.append(0-branch_var)
    positive_branch_result = branching_sat_solve(new_clause_set, positive_partial_assignment)
    negative_branch_result = branching_sat_solve(new_clause_set, negative_partial_assignment)
    if positive_branch_result:
        return positive_branch_result
    if negative_branch_result:
        return negative_branch_result
    return False   

clauses1, N = load_dimacs('dimacs.txt')

print(simple_sat_solve(clauses1))
print('result', branching_sat_solve(clauses1, []))
