def opotunity(x, y, cur, n, m, level):
    level[x][y] = cur
    if y + 1 < m:
        if level[x][y + 1] == 0 or (level[x][y + 1] != -1 and level[x][y + 1] > cur):
            opotunity(x, y + 1,cur + 1, n, m, level)
    if x + 1<n:
        if level[x + 1][y] == 0 or (level[x + 1][y] != -1 and level[x + 1][y] > cur):
            opotunity(x + 1, y, cur + 1, n, m, level)
    if x - 1 >= 0:
        if level[x - 1][y] == 0 or (level[x - 1][y] != -1 and level[x - 1][y] > cur):
            opotunity(x - 1, y, cur + 1, n, m, level)
    if y - 1 >= 0:
        if level[x][y - 1] == 0 or (level[x][y -1 ] != -1 and level[x][y - 1] > cur):
            opotunity(x, y - 1, cur + 1, n, m, level)
    return level

def way(level, start1, start2, finish1, finish2):
    x = len(level[0])
    y = len(level)

    pars_level = []
    for i in level:
        well_pars = i.replace('', ' ')
        well_pars = well_pars.replace('1', '-1')
        well_pars = list(map(int, well_pars.split()))
        pars_level.append(well_pars)

    x1, y1 = start1 - 1, start2 - 1
    x2, y2 = finish1 - 1, finish2 - 1
    lab = opotunity(x1, y1, 1, y, x, pars_level)

    if lab[x2][y2] > 0:
        print("Mozhet")
    else:
        print("Ne mozhet")
        
tx_map = [
    '1111111111111111',
    '1000000000111001',
    '1000000000000001',
    '1000011111000001',
    '1000000000000001',
    '1111100000000001',
    '1111100000000001',
    '1111111111111111',
]

way(tx_map, 2, 2, 15, 7)