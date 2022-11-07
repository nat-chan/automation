import win32gui
import pyautogui
import numpy as np
from tqdm import tqdm
from itertools import count
import time
from pathlib import Path
import requests
import win32clipboard
import re
import os

datadir = Path("/data")
outdir = datadir/"out"
outdir.mkdir(exist_ok=True)

sim = sorted((datadir/"whitechest_sim_val").glob("**/*.png"))
val = sorted((datadir/"whitechest_val").glob("**/*.png"))
assert 7499 == len(sim) == len(val)
np.random.RandomState(0).shuffle(sim)
np.random.RandomState(0).shuffle(val)
fold_sim = [sim[j*10**3:(j+1)*10**3] for j in range(len(sim)//10**3)]
fold_val = [sim[j*10**3:(j+1)*10**3] for j in range(len(val)//10**3)]


col = [
    np.array([[[0,  0,  0]]], dtype=np.uint8),
    np.array([[[24, 24, 24]]], dtype=np.uint8),
]

try:
    s2p_path = r'C:\Users\qzrp0\Documents\style2paints45beta1214B\style2paints.exe'
    backend_path = r'C:\Users\qzrp0\Documents\style2paints45beta1214B\assets\Style2PaintsV45.exe'
    os.system(f'start "" "{s2p_path}"')
    for c in count():
        s2p_launcher = pyautogui.getActiveWindow()
        if 'Style2Paints Launcher' == getattr(s2p_launcher, "title", ""):
                break
    pyautogui.press("enter")
    for c in count():
        s2p_backend = pyautogui.getActiveWindow()
        if backend_path  == getattr(s2p_backend, "title", ""):
                break

    for c in count():
        s2p_app = pyautogui.getActiveWindow()
        if 'Style2Paints Version 4.5' == getattr(s2p_app, "title", ""):
                break

    time.sleep(5) # wait app init

    #skip = 38 + 33 + 6 + 65 + 48 + 11 + 123 + 130 + 136 + 129 + 145 + 120
    skip = 0
    for i, fname in enumerate(tqdm(fold_sim[0][skip:])):
        i = i + skip
        up_point = pyautogui.Point(x=3542, y=1788)
        pyautogui.moveTo(up_point)
        for c in count():
            time.sleep(0.2)
            pyautogui.click()
            open_file = pyautogui.getActiveWindow()
            if 'Open File' == getattr(open_file, "title", ""):
                break
        pyautogui.keyDown("ctrl")
        pyautogui.press("l")
        pyautogui.keyUp("ctrl")
        pyautogui.typewrite(str(fname.parent))
        pyautogui.press("enter")
        pyautogui.keyDown("shift")
        for _ in range(7):
            pyautogui.press("tab")
        pyautogui.keyUp("shift")
        pyautogui.typewrite(str(fname.name))
        pyautogui.press("enter")


        gus = [
        [(1916, 590), (1916, 250)],
        [(1422, 1065), (1082, 1065)],
        [(1916, 1558), (1916, 1898)],
        [(2411, 1065), (2751, 1065)]]
        for gu in gus:
            pyautogui.moveTo(*gu[0])
            pyautogui.dragTo(*gu[1], button="left", duration=0.5)
        pyautogui.moveTo(pyautogui.Point(x=1672, y=1995))
        pyautogui.click()


        status_pos = pyautogui.Point(x=2685, y=1833)
        for c in count():
            img = pyautogui.screenshot(region=(status_pos[0],status_pos[1], 1, 1))
            arr = np.array(img)
            print(arr)
            if ((col[1]-arr)**2).mean()**.5 < 1:
                print("ok")
                break
            else:
                print(arr)
            time.sleep(0.5)

        pyautogui.moveTo(3710, 1814)
        for c in count():
            time.sleep(0.2)
            pyautogui.click()
            about = pyautogui.getActiveWindow()
            if 'about:blank' == getattr(about, "title", ""):
                break
        time.sleep(0.2)
        pyautogui.moveTo(2663, 923)
        pyautogui.click(button="right")
        time.sleep(0.2)
        pyautogui.moveTo(2771, 1102)
        for c in count():
            time.sleep(0.2)
            pyautogui.click()
            memo = pyautogui.getActiveWindow()
            if "メモ帳" in memo.title:
                break
        pyautogui.keyDown("ctrl")
        pyautogui.press("a")
        pyautogui.press("c")
        pyautogui.keyUp("ctrl")
        memo.close()
        about.close()

        win32clipboard.OpenClipboard()
        clipboard = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        urls = re.findall(r'http://.*?png', clipboard)
        for url in urls:
            if "sketch.png" in url: continue
            print(url)
            img_data = requests.get(url).content
            stat = url.split(".")[-2]
            with open(outdir/f"{i}.{fname.stem}.{stat}.png", "wb") as f:
                f.write(img_data)
except Exception as e:
    print(e)
finally:
    s2p_backend.close()
    s2p_app.close()