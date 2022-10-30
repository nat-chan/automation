from PIL import Image
NEAREST = Image.Resampling.NEAREST
import numpy as np

rgbs = list({tuple(rgb) for rgb in np.random.RandomState(0).randint(0, 255, (10**7,3))})
invs = {rgb:i for i, rgb in enumerate(rgbs)}
#ssize = (512, 724, 3)
ssize = (512*3, 512*3, 3)
start = 3

def a(n):
    return start + n*(n+1)//2

b = dict()
t = 0
for i in range(100):
    for j in range(a(i)):
        b[i, j] = t + j
    t += a(i)

# Σ(40) = 10780
out = list()
for i in range(55):
    img = Image.fromarray(
        np.hstack(
            [
                np.full(ssize, rgbs[b[i,j]], dtype=np.uint8)
                for j in range(a(i))
            ]
        )
    )
    img2 = img.resize((ssize[0], round(ssize[0]*img.size[1]/img.size[0])), resample=NEAREST)
#    len({tuple(rgb) for rgb in np.array(img2).reshape(-1, 3)})
    out.append(np.array(img2))

fin_arr = np.vstack(out)
fin = Image.fromarray(fin_arr)
fin

def search():
    for i in range(55, 55+1):
        for j in range(a(i)):
            searched = np.array(np.where((fin_arr == rgbs[b[i, j]]).all(axis=2))).transpose()
            cnt = len(searched)
            print(i,f"{j}/{a(i)}", cnt, np.sqrt(cnt))
            if cnt == 0:
                print("\x1b[31mng\x1b[m")
                return 
    print("\x1b[31mok\x1b[m")
search()

