import win32gui
import pyautogui
import numpy as np
from tqdm import tqdm
from itertools import count
import time

col = [
    np.array([[[209,  99,  24]]], dtype=np.uint8),
    np.array([[[179, 192, 203]]], dtype=np.uint8),
]

def f1(pos):
    _pos = pyautogui.position()
    pyautogui.moveTo(pos)
    pyautogui.click()
    pyautogui.moveTo(_pos)
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    pyautogui.keyUp("alt")

def f2():
    _hwnd = win32gui.GetForegroundWindow()
    hwnds = pyautogui.getWindowsWithTitle("Stable Diffusion")
    assert len(hwnds) == 1
    hwnds[0].activate()
    pyautogui.press("enter")
    win32gui.SetForegroundWindow(_hwnd)

pos = pyautogui.position()
print(f"{pos=}")

batchsize = 8

pbar = tqdm()
for c in count():
    img = pyautogui.screenshot(region=(pos[0],pos[1], 1, 1))
    arr = np.array(img)
    if ((col[0]-arr)**2).mean()**.5 < 1:
        f2()
        pbar.update(n=batchsize)
        pbar.set_description(f"ready {c} {pbar.n}")

    elif ((col[1]-arr)**2).mean()**.5 < 1:
        pbar.update(n=0)
        pbar.set_description(f"wait {c} {pbar.n}")
    else:
        print("\x1b[31mSomething went wrong\x1b[m")
        break
    time.sleep(1)