from pystyle import Colors, Colorate, Center, Anime, System, Write

def banner_intro():
    banner = r'''
   _______  ___  ___  ___      __       __   ___  
  |   __ "\|"  \/"  ||"  |    /""\     |/"| /  ") 
  (. |__) :)\   \  / ||  |   /    \    (: |/   /  
  |:  ____/  \\  \/  |:  |  /' /\  \   |    __/   
  (|  /      /   /___|  /  //  __'  \  (// _  \   
 /|__/ \    /   //  :|_/ )/   /  \\  \ |: | \  \  
(_______)  |___/(_______/(___/    \___)(__|  \__) 

                                             
'''
    Write.Print((banner), Colors.red_to_black, interval=0.0025)