import copy

def load_dimacs(filename):
    with open(filename, 'r') as f:
        l1 = f.readline()
        while l1[0] == 'c':
            l1 = f.readline()
        l1 = l1.split(' ')
        M = int(l1[3])
        count = 0
        clause_set = []
        while count < M:
            line = f.readline()
            if line[0] != 'c':
                line_list = line.split(' ')
                count += 1
                clause = []
                for c in line_list:
                    if c != '0' and c != '' and c != '0\n':
                        clause.append(int(c))
                clause_set.append(clause)
        return clause_set

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
    for i in partial_assignment:
        if i in variables or 0-i in variables:
            for clause in new_clause_set:
                if i in clause:
                    new_clause_set = list(filter(lambda a: a != clause, new_clause_set))
                elif 0-i in clause:
                    new_clause_set[new_clause_set.index(clause)] = list(filter(lambda a: a != 0-i, new_clause_set[new_clause_set.index(clause)]))
            variables.discard(i)
            variables.discard(0-i)
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

def unit_propagate(clause_set, dpll = False):
    cont = True
    new_clause_set = copy.deepcopy(clause_set)
    chosen_literals = []
    while cont:
        cont = False
        chosen = 0
        for i in range(len(new_clause_set)):
            if len(new_clause_set[i]) == 1:
                cont = True
                chosen = new_clause_set[i][0]
                chosen_literals.append(chosen)
                break
        if cont:
            for clause in new_clause_set:
                if chosen in clause:
                    new_clause_set = list(filter(lambda a: a != clause, new_clause_set))
                elif 0-chosen in clause:
                    new_clause_set[new_clause_set.index(clause)] = list(filter(lambda a: a != 0-chosen, new_clause_set[new_clause_set.index(clause)]))
    if dpll:
        return new_clause_set, chosen_literals
    return new_clause_set

def pure_literal_eliminate(clause_set, dpll = False):
    new_clause_set = copy.deepcopy(clause_set)
    pure_exist = True
    pures = []
    while pure_exist:
        pure = 0
        pure_exist = False
        checked_literals = []
        for clause in new_clause_set:
            for l in clause:
                if l not in checked_literals and 0-l not in checked_literals:
                    pure = l
                    for c in new_clause_set:
                        if 0-l in c:
                            pure = 0
                            break
                    if pure == l:
                        pures.append(l)
                        pure_exist = True
                        break
                    else:
                        checked_literals.append(l)
            if pure_exist:
                break
        for clause in new_clause_set:
            if pure in clause:
                new_clause_set = list(filter(lambda a: a != clause, new_clause_set))
    if dpll:
        return new_clause_set, pures
    return new_clause_set
        
def dpll_sat_solve(clause_set, partial_assignment=[]):
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

    for i in partial_assignment:
        if i in variables or 0-i in variables:
            for clause in new_clause_set:
                if i in clause:
                    new_clause_set = list(filter(lambda a: a != clause, new_clause_set))
                elif 0-i in clause:
                    # clause.remove(0-i) #do same filter thing above here and hope it works lol
                    new_clause_set[new_clause_set.index(clause)] = list(filter(lambda a: a != 0-i, new_clause_set[new_clause_set.index(clause)]))
            variables.discard(i)
            variables.discard(0-i)

    new_clause_set, chosen_literals = unit_propagate(new_clause_set, True)
    new_clause_set, pures = pure_literal_eliminate(new_clause_set, True)
    partial_assignment.extend(chosen_literals)
    partial_assignment.extend(pures)

    flat_list = []
    for clause in new_clause_set:
        flat_list.extend(clause)
    new_variables = set()
    for i in flat_list:
        if i > 0:
            new_variables.add(i)
        else:
            new_variables.add(0-i)

    if new_variables == set():
        if new_clause_set == []:
            if variables == set():
                return partial_assignment
            for l in variables:
                if l not in partial_assignment and 0-l not in partial_assignment:
                    partial_assignment.append(l)
            return partial_assignment
        return False
    
    branch_var = list(new_variables)[0]
    positive_partial_assignment = copy.copy(partial_assignment)
    negative_partial_assignment = copy.copy(partial_assignment)
    positive_partial_assignment.append(branch_var)
    negative_partial_assignment.append(0-branch_var)
    positive_branch_result = dpll_sat_solve(new_clause_set, positive_partial_assignment)
    negative_branch_result = dpll_sat_solve(new_clause_set, negative_partial_assignment)
    if positive_branch_result:
        return positive_branch_result
    if negative_branch_result:
        return negative_branch_result
    return False

clause_set = load_dimacs('dimacs.txt')
print(dpll_sat_solve(clause_set))