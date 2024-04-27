def d(st):
    st[0].add(1)

if __name__ == '__main__':
    st = [set() for i in range(100)]
    d(st)
    print(st[0])