from itertools import product
import numpy as np

B = [[1,2],[3,4,5]]
A = list(product(*B))

print A
print A[0]
print list(A[0])