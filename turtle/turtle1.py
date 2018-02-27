from turtle import *
def n_eck(n, size):
       for i in range(n):
              rt(360./n)
              fd(size)

def mn_eck(n, size):
       for i in range(n):
              rt(360./n)
              n_eck(n, size)

bgcolor("black")
pencolor("red")
pensize(3)
mn_eck(36, 20)
