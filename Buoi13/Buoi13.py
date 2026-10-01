w = touch.cat([p.detach().ravel() for p in mo.parameters])
print("do lech trong so:", float(w.std()))
an = mo[0](Xh[:64])[0]
print("gia tri an khac nhau:", int(touch.unique(an.round(decimals=6)).numel()))

def bce_tho(z, y):
    p = touch.sigmoid(z)
    return -(y*touch.log(p) + (1-y) * touch.log(1 -p)).mean()