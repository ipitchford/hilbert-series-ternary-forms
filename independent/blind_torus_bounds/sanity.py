from poles import *
# hand examples
assert kappa([(1,0),(-1,0)])==1 and order_o([(1,0),(-1,0)])==2
assert kappa([(1,0),(0,1),(-1,-1)])==1 and order_o([(1,0),(0,1),(-1,-1)])==3
assert kappa([(1,0),(0,1)])==0
assert kappa([(0,0)])==1 and order_o([(0,0)])==1
assert kappa([(1,0),(-1,0),(0,1),(0,-1)])==2          # 4 vars, rank 2
assert kappa([(1,0),(-1,0),(0,1)])==1                 # (0,1) can't be positive
assert kappa([(2,0),(-1,0)])==1 and order_o([(2,0),(-1,0)])==3   # relation (1,2), sum 3
assert kappa([(1,0),(-1,0),(2,0),(-2,0)])==3 and order_o([(1,0),(-1,0),(2,0),(-2,0)])==1  # (1,1)->2,(2,1)?  -> gcd
W=weights(3); assert len(W)==10 and kappa(W)==8
print("sanity ok")
