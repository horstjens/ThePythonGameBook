# ---- one dimensional array -----
array1 = [100,200,300,444]
print("array1:", array1)
print("iterating over a one-dimensional array:")
for element in array1:
    print(element)
# ---- two dimensional array -----
array2 = [ ["a","b","c"],
           ["d","e","f"] ]
print("array2:", array2)
print("iterating over a two-dimensional array:")
for row in array2:
    for element in row:
        print(element, end=" ")
    print() # force a new line
