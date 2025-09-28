# tup = (4,5,6)

# print(tup)

# tup = tuple('string')
# tup[0]

a = 1
b = 2
values = 1, 2,3 ,4,5

a,b, *rest = values

print(rest) # 3,4,5

# _ means ignore the rest of the values
a, b, *_ = values
print(_)

print(2 in values)

for y in values:
    print(f"{(lambda x:x * 2)(y)}")

import math
print(math.log(1000, 10))

some_dict = {"a": 1, 2: "x", "ds": 3 }
[ print(y) for y in some_dict ]