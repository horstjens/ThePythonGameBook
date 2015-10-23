import turtle as t
import random

t.speed(0)


def tree(age=100):
    """paint a tree"""
    t.pd()
    t.fd(age * 0.3)
    t.lt(90)
    t.fd(age * 1.3)
    t.lt(90)
    t.fd(age * 0.15)
    t.circle(age * -0.6)
    t.fd(age * 0.15)
    t.lt(90)
    t.fd(age * 1.3)
    t.lt(90)
    t.pu()


def forest(amount=100):
    """paint a forest"""
    t.clear()
    t.pu()
    for x in range(amount):
        t.setpos(random.randint(-400, 400), random.randint(-300, 300))
        tree(random.randint(10, 200))


if __name__ == "__main__":
    forest()
