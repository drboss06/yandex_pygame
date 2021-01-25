def voln(x,y,cur,n,m,lab):
    lab[x][y] = cur
    if y+1<m:
        if lab[x][y+1] == 0 or (lab[x][y+1] != -1 and lab[x][y+1] > cur):
            voln(x,y+1,cur+1,n,m,lab)
    if x+1<n:
        if lab[x+1][y] == 0 or (lab[x+1][y] != -1 and lab[x+1][y] > cur):
            voln(x+1,y,cur+1,n,m,lab)
    if x-1>=0:
        if lab[x-1][y] == 0 or (lab[x-1][y] != -1 and lab[x-1][y] > cur):
            voln(x-1,y,cur+1,n,m,lab)
    if y-1>=0:
        if lab[x][y-1] == 0 or (lab[x][y-1] != -1 and lab[x][y-1] > cur):
            voln(x,y-1,cur+1,n,m,lab)
    return lab

def main():
    lab = []
    rdl = list(map(int,input().split()))
    n, m = rdl
    for i in range(n):
        rdl = input()
        cur = []
        for k in range(m):
            if int(rdl[k]) == 1:
                cur.append(-1)   
            else:    
                cur.append(int(rdl[k]))
        lab.append(cur)
    rdl = list(map(int,input().split()))
    x1, y1 = rdl[0]-1, rdl[1]-1
    rdl = list(map(int,input().split()))
    x2, y2 = rdl[0]-1, rdl[1] -1
    lab = voln(x1,y1,1,n,m,lab)

    if lab[x2][y2] > 0:
        print("Mozhet")
        print(x1, y1, x2, y2)
    else:
        print("Ne mozhet")

#main()
print(len('1111111111111111'))