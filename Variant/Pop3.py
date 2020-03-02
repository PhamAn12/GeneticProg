# delete return stsm
def mid(a, b):
    if a == 0:
        print(b)
        r = b
        
        return r
    while b != 0:
        if a > b:
            a = a - b
        else:
            b = b - a
    print(a)
    r = a