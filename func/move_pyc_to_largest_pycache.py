import os 
import shutil
from pystyle import Write, Colors

def move_pyc_to_largest_pycache(compiled_file_path, largest_pycache):
    if compiled_file_path and largest_pycache:
        try:
            shutil.move(compiled_file_path, largest_pycache)
            Write.Print(f"[+] Arquivo .pyc movido para: {largest_pycache}\n", Colors.red_to_yellow, interval=0)
            return os.path.join(largest_pycache, os.path.basename(compiled_file_path))
        except Exception as e:
            Write.Print(f"[e] Erro ao mover o arquivo .pyc: {e}\n", Colors.red_to_yellow, interval=0)
            return None
    return None