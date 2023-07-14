from functools import cache


@cache
def a(x):
    if x == 0:
        return 0
    return x + a(x - 1) 


@cache
def b(g):
    return lambda x: g(x) + 0.5


f = b(a)


for i in range(1000_000):
    f(i)
print('1')

f(1000_007)