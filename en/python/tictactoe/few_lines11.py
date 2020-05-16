# https://www.reddit.com/r/madeinpython/comments/gdsv8f/tictactoe_in_just_11_lines_of_code_vanilla_python/
s = int(input(f'please enter number of rows: \n'))
b, player, i, z = [['-']*s for i in range(s)], 'X', 1, ''.join(map(str,range(s)))
while '-' in (y for x in b for y in x):
    r, c, i = *(int(input(f'please enter {x}: \n'))-1 for x in ("row","column")), i+1
    if b[r][c] == '-':
        player, b[r][c] = ['X' if i%2 else 'O']*2
    print('   '+'   C%d'*s%tuple(range(1,s+1)),*(f' R{x+1} {b[x]}'for x in range(s)),sep='\n')
    if any(any(all(b[int(c)][int(d)]==t for c,d in g) for t in'OX') for g in [(lambda w:list(zip(w[:s],w[s:])))(u) for u in [(x*s+z)[::y]for y in[1,-1]for x in z]+[z*2,z[::-1]+z]]):
        print(player, 'wins')
        break
else:
    print('tie')