import sys

param = sys.argv[1]

def factorial(num):
    n=1
    for i in range(1, num+1):
        n=n*i
    return n

print("factorial: {}".format(factorial(int(param))))
