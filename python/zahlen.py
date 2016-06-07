import random
summe = 0

for x in range(10):
    w = random.randint(1, 6)
    print x, ".Wurf: ", w

    summe += w

print "______________________"
print "summe: ", summe
