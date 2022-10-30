from PIL import Image
NEAREST = Image.Resampling.NEAREST
import numpy as np
from pathlib import Path
from tqdm import tqdm
from functools import lru_cache

rgbs = list({tuple(rgb) for rgb in np.random.RandomState(0).randint(0, 255, (10**7,3))})
invs = {rgb:i for i, rgb in enumerate(rgbs)}
#ssize = (512, 724, 3)
ssize = (512*3, 512*3, 3)

def a(n):
    return 3 + n*(n+1)//2

def b(i, j):
    return i*(i*i+17)//6 + j

fnames = list(Path("outputs/txt2img-images").glob("*.png"))
brightness = [(np.array(Image.open(fname).convert("L")).mean(), fname) for fname in fnames]
brightness.sort()
np.random.RandomState(0).shuffle(fnames)

# Σ(40) = 10780
out = list()
for i in range(55):
    img = Image.fromarray(
        np.hstack(
            [
                np.full(ssize, rgbs[b(i,j)], dtype=np.uint8)
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

me_arr = np.array(Image.open(r"/Users/qzrp0/gdrive/alumni/cigarette/me0.png").convert("RGB"))
goods = list(Path("outputs/good").glob("*machine.png"))

def c(i, j, thr):
    if i in range(5):
        z = 0
        for d in ["human", "good"]:
            tname = Path(f"outputs/{d}/{z}{i}_{j}.png")
            if tname.exists():
                return Image.open(tname)
        return Image.open(goods[b(i,j)%len(goods)])
    if i in range(8, 55):
        bij = b(i, j)
        m = me_arr[np.where((fin_arr == rgbs[bij]).all(axis=2))].mean()
#        if m < 254:
        if m < 128:
            return Image.open(np.random.RandomState(bij).choice(np.array(brightness[:100]).transpose()[1]))
#        return Image.open(np.random.RandomState(bij).choice(np.array(brightness[-100:]).transpose()[1]))
    return Image.open(fnames[b(i,j)%len(fnames)])


def d(i, pbar, thr=1000):
    tmp2 = list()
    for j in range(a(i)):
        tmp2.append(c(i, j, thr))
        pbar.update(n=1)
        pbar.set_description(f"{i} {j}")
    img = Image.fromarray(np.hstack(tmp2))
    img2 = img.resize((ssize[0], round(ssize[0]*img.size[1]/img.size[0])), resample=NEAREST)
    return img2


# 完成品
N = 55
with tqdm(total=b(N, 0)) as pbar:
    out2 = list()
    for i in range(N):
        img2 = d(i, pbar)
        out2.append(img2)
    fin2_arr = np.vstack(out2)
    fin2 = Image.fromarray(fin2_arr)
    fin2

H = 2172
h_out = list()
lastline = fin2_arr[-1, :, :].copy()
for h in range(H-len(fin2_arr)):
    _lastline = lastline.copy()
    np.random.RandomState(h).shuffle(_lastline)
    h_out.append(_lastline[None, :, :])
Image.fromarray(np.vstack([fin2_arr]+h_out))

def search():
    for i in range(55, 55+1):
        for j in range(a(i)):
            searched = np.array(np.where((fin_arr == rgbs[b(i, j)]).all(axis=2))).transpose()
            cnt = len(searched)
            print(i,f"{j}/{a(i)}", cnt, np.sqrt(cnt))
            if cnt == 0:
                print("\x1b[31mng\x1b[m")
                return 
    print("\x1b[31mok\x1b[m")
search()

