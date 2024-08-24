import os 
from pystyle import Write, Colors


def find_largest_pycache(project_path):
    pycache_dirs = []
    
    for root, dirs, files in os.walk(project_path):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            pycache_dirs.append(pycache_path)
    
    if not pycache_dirs:
        Write.Print("[!] Nenhuma pasta '__pycache__' encontrada no projeto.\n", Colors.red_to_yellow, interval=0)
        return None

    largest_pycache = None
    max_pyc_count = -1
    
    for pycache_path in pycache_dirs:
        pyc_files = [f for f in os.listdir(pycache_path) if f.endswith('.pyc')]
        if len(pyc_files) > max_pyc_count:
            max_pyc_count = len(pyc_files)
            largest_pycache = pycache_path
    
    return largest_pycache