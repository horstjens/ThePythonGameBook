while True: # endless loop
    print("Pease enter index of column: 0 or 1 or 2")
    print("folled by index of row: 0 or 1 or 2")
    print("like for example: 0 1")
    command = input("and press ENTER: >>>")
    command = command.strip() # remove leading and trailing spaces
    column_string = command[0]# the first char
    row_string = command[-1] # the last (!) char
    if column_string in ["0","1","2"] and row_string in ["0", "1", "2"]:
        break
    print("Wrong input. Please try again")
print("column:", column_string, "row:", row_string)
