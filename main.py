

import time

clauses0=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [-1, -2], [-1, -3], [-2, -3], [-4, -5], [-4, -6], [-5, -6], [-7, -8], [-7, -9], [-8, -9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [-1, -4], [-1, -7], [-4, -7], [-2, -5], [-2, -8], [-5, -8], [-3, -6], [-3, -9], [-6, -9], [1, 8], [-1, -8], [4, 2], [-2, -4]]
[-1, 8, -7, -9, -2, -5, 3, 4, -6]


#print(clauses0)

import mpll19

start=time.time()
print(mpll19.dpll_sat_solve(clauses0,[]))
end=time.time()
print(end-start)

#import dcs1bdm

#start=time.time()
#print(dcs1bdm.dpll_sat_solve(clauses0,[]))
#end=time.time()
#print(end-start)
