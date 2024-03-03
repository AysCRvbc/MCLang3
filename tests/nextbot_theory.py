a = (3.88, 44.18)
b = (6.48, 42.05)


def psfloat(x):
    return int(x*100)


def frac(x, y):
    return int(x*100/y)


def mul(x, y):
    return int(x * y / 100)


pi = 314


def psantiabs(x):
    if x < 0:
        return x
    return -x


def pspow(x, y):
    res = x
    while y > 1:
        res = mul(res, x)
        y -= 1
    return res


def psatan(x):
    sign = 1
    if x > 0:
        sign = -1
    x = psantiabs(x)

    if x < -362:
        return -140
    x += 200

    res = -110
    res += mul(20, x)
    res += mul(8, pspow(x, 2))
    res += mul(3, pspow(x, 3))
    res += mul(1, pspow(x, 4))

    return sign*res


intA = [psfloat(x) for x in a]
intB = [psfloat(x) for x in b]

dx = intB[0] - intA[0]
dz = intB[1] - intA[1]

r = psatan(frac(dz, dx))

res = mul(200, r)
res = frac(res, 314)
res -= 100
res = mul(res, 9000)

print(res)