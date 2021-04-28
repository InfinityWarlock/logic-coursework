def load_dimacs(filename):
    with open(filename, 'r') as f:
        l1 = f.readline()
        while l1[0] == 'c':
            l1 = f.readline()
        l1 = l1.split(' ')
        N = l1[2]
        M = l1[3]
        count = 0
        clause_set = []
        while count < M:
            line = f.readline()
            if line[0] != 'c':
                line_list = line.split(' ')
                count += 1
                clause = []
                for c in line_list:
                    if c != '0':
                        clause.append(int(c))
                clause_set.append(clause)
        return clause_set, N

clauses0=[]

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




print(simple_sat_solve(clauses0))
if []:
    print('hello')


