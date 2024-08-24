import os
import ctypes

def menu_builder():
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(f" Injectior | Pyjek | {os.getenv('computername')}")
    except:
        pass