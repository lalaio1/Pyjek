from pystyle import Colors, Colorate, Center, Anime
import random 
import os

def print_intro():
    banner_dir = './banner'
    if not os.path.isdir(banner_dir):
        print(Colorate.Horizontal(Colors.red, f"Erro: Diretório de banners não encontrado: {banner_dir}"))
        return

    banner_files = [f for f in os.listdir(banner_dir) if f.endswith('.txt')]
    if not banner_files:
        print(Colorate.Horizontal(Colors.red, "Erro: Nenhum arquivo de banner encontrado no diretório"))
        return

    banner_file = random.choice(banner_files)
    banner_path = os.path.join(banner_dir, banner_file)
    
    with open(banner_path, 'r', encoding='utf-8') as file:
        banner = file.read()

    Anime.Fade(Center.Center(banner), Colors.red_to_black, Colorate.Vertical, interval=0.085, enter=True)