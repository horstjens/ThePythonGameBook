import random
# attack with random.random()
output = {}
for x in range(1000):
    attack = random.random()
    if round(attack, 2) in output:
        output[round(attack, 2)] += 1
    else:
        output[round(attack, 2)] = 1
mycsv = open("attack-values.csv", "w")
for v in output:
    mycsv.write(str(v) + "," + str(output[v]) + "\n")
mycsv.close()
# defense with random.gauss()

output = {}
for x in range(1000):
    defense = random.gauss(0.5, .2)
    if round(defense, 2) in output:
        output[round(defense, 2)] += 1
    else:
        output[round(defense, 2)] = 1
mycsv = open("defense-values.csv", "w")
for v in output:
    mycsv.write(str(v) + "," + str(output[v]) + "\n")
mycsv.close()


# damage (integer) with re_roll function
def re_roll(faces=6, start=0):
    """open ended die throw, can re-roll at highest face)"""
    while True:
        roll = random.randint(1, faces)
        if roll != faces:
            return roll + start
        return re_roll(faces, roll - 1 + start)


output = {}
for x in range(1000):
    damage = re_roll()
    if damage in output:
        output[damage] += 1
    else:
        output[damage] = 1
mycsv = open("damage-values.csv", "w")
for v in output:
    mycsv.write(str(v) + "," + str(output[v]) + "\n")
mycsv.close()

print("csv files ready")
