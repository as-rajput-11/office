

a = [(3, 10, 'MIRZAPUR', 3, 1), (7, 11, 'MIRZAPUR', 2, 1), (19, 15, 'MIRZAPUR', 3, 1), (22, 16, 'MIRZAPUR', 3, 1)]
b = [(19, 20, 'MIRZAPUR', 3, 1), (22, 40, 'MIRZAPUR', 3, 1),(23, 50, 'MIRZAPUR', 3, 1),(24, 55, 'MIRZAPUR', 3, 1)]
d = [(19, 20, 'MIRZAPUR', 3, 1), (22, 40, 'MIRZAPUR', 3, 1),(23, 50, 'MIRZAPUR', 3, 1),(24, 55, 'MIRZAPUR', 3, 1)]
c =[]
cap = 3
test = cap
tt = 0

for index,i in enumerate(b):
    if cap > index:
        print(a[index][1],b[index][1],'aaa')
        subi = (a[index][1]-b[index][1])

        print([index],subi)
        print(b[index])        
        
        # c.append(update)

    else:
        sub = (b[tt][1],b[test][1],'bbb')
        print(b[tt][0])
        print(b[tt][1],b[test][1],'bbb')
        
        test = test + 1
        tt = tt + 1
