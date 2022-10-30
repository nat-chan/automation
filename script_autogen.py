import win32gui
import pyautogui
import numpy as np
import time

col = [
    np.array([[[209,  99,  24]]], dtype=np.uint8),
    np.array([[[179, 192, 203]]], dtype=np.uint8),
]

pos = pyautogui.position()
print(f"{pos=}")

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

while True:
    img = pyautogui.screenshot(region=(pos[0],pos[1], 1, 1))
    arr = np.array(img)
    if ((col[0]-arr)**2).mean()**.5 < 1:
        f2()
    elif ((col[1]-arr)**2).mean()**.5 < 1:
        time.sleep(1)
    else:
        print("\x1b[31mSomething Wring\x1b[m")
        break