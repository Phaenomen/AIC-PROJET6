import subprocess
import os
import ctypes
import random
import winreg
import time


# > PARAMETRAGE DU REGISTRE


def registryKeys() :
    # Raccourcis du bureau (Fichiers de l'utilisateur, Ce PC, Corbeille, OneDrive)

    registry=winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)  # Ouvre la ruche de registre "Current User"
    key=winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel',
                       reserved = 0,
                       access = winreg.KEY_ALL_ACCESS)  # Ouvre la clé "NewStartPanel" avec droit de modification de valeurs
    winreg.SetValueEx(key, '{20D04FE0-3AEA-1069-A2D8-08002B30309D}', 0, winreg.REG_DWORD,
                      0)  # Modifie la valeur '{20D04FE0-..." et lui met "0". Si non présente, la crée et "0" affiche l'icone "Fichiers de l'utilisateur"
    winreg.SetValueEx(key, '{59031a47-3f72-44a7-89c5-5595fe6b30ee}', 0, winreg.REG_DWORD,
                      0)  # Pareil - 0 affiche l'icône "Ce PC"
    winreg.SetValueEx(key, '{018D5C66-4533-4307-9B53-224DE2ED1FE6}', 0, winreg.REG_DWORD,
                      1)  # Pareil - 1 "cache" l'icône OneDrive (si existant)
    winreg.SetValueEx(key, '{645FF040-5081-101B-9F08-00AA002F954E}', 0, winreg.REG_DWORD,
                      0)  # Pareil - 0 affiche la corbeille (si pas affiché par défaut)
    key.Close()  # Ferme l'accès a la clé
    print(" --> Les raccourcis ont été paramamétrés.") # Affiche ce message

    # Message d'accueil personnalisé au démarrage

    registry=winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)  # Ouvre la ruche de registre "Local Machine"
    key=winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Policies\System', reserved = 0,
                       access = winreg.KEY_ALL_ACCESS)  # Ouvre la clé "System" avec droit de modification de valeurs
    winreg.SetValueEx(key, 'legalnoticecaption', 0, winreg.REG_SZ,
                      "Votre ordinateur a été configuré par Nicolas PICARD")  # On modifie la clé en mettant notre message"
    winreg.SetValueEx(key, 'legalnoticetext', 0, winreg.REG_SZ,
                      "Si vous avez des questions, vous pouvez le joindre au 06 02 03 04 05")  # Pareil ici
    key.Close()  # Ferme l'accès a la clé
    print(" --> Un message d'accueil a été paramètré") # Affiche ce message

    # Corbeille ajouté à "Ce PC"

    registry=winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)  # Ouvre la ruche de registre "Local Machine"
    key=winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace',
                       reserved = 0,
                       access = winreg.KEY_ALL_ACCESS)  # Ouvre la clé "NameSpace" avec droit de modification de valeurs
    winreg.CreateKey(key, '{645FF040-5081-101B-9F08-00AA002F954E}')  # Crée la clé qu'on a besoin
    key.Close()  # Ferme l'accès a la clé
    print(" --> La corbeille a été rajouté dans les péréphiques") # Affiche ce message

    # Désactiver Cortana (en laissant le choix)


while True :  # On ouvre une boucle

    registry=winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)  # Ouvre la ruche de registre "Local Machine"
    key=winreg.OpenKey(registry, r'Software\Policies\Microsoft\Windows',
                       reserved = 0,
                       access = winreg.KEY_ALL_ACCESS)  # Ouvre la clé "Windows" avec droit de modification de valeurs
    winreg.CreateKey(key, 'Windows Search')  # Je crée la clé "Windows Search"

    response=input('Voulez-vous desactiver cortana ? [o/N] ') # Affiche cette question
    if response == "o" :  # Si la réponse est "o", cortana sera désactivé
        key=winreg.OpenKey(registry, r'Software\Policies\Microsoft\Windows\Windows Search',
                           reserved = 0, access = winreg.KEY_ALL_ACCESS)  # Ouvre la clé que j'ai crée juste au dessus
        winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 0)  # Crée une valeur DWORD et on la met à 0
        print("OK, Cortana a été désactivé") # Affiche ce message
        break  # On ferme la boucle
    elif response == "n" or response == '' :  # Si la réponse est "n" ou un "blanc", cortana restera actif
        winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 1)  # Crée une valeur DWORD et on la met à 1
        key.Close()  # Ferme l'accès a la clé
        print("OK, nous laissons Cortana actif") # Affiche ce message
        break  # On ferme la boucle

    else :  # Si la condition if ou elif n'est pas remplie, on repose la question
        print("Répondez par 'o' ou 'n' ou appuyez sur entrée") # Affiche de nouveau la question


# > DESACTIVER LA MISE EN VEILLE PROLONGEE


def hibernate() :
    subprocess.run(['powershell', '-Command', 'powercfg -h off'],
                   capture_output = True)  # Lance une commande pour désactiver la veille
    print(" --> La mise en veille prolongée est désactivée.") # Affiche ce message


# > CHANGEMENT DU FOND D'ECRAN


def changeWallpapers() :
    images=[]  # Déclare une liste vide
    for image in os.listdir(
            os.getcwd() + r'\WallPapers') :  # Boucle parcourant les fichiers du répertoire WallPapers (image est le nom d'un fichier)
        # print(image) # On peut décommenter pour voir la liste des images disponible dans notre dossier
        images.append(image)  # Ajoute le fichier à la liste
    image=os.getcwd() + r'\WallPapers\\' + images[random.randint(0, len(os.listdir(
        os.getcwd() + r'\WallPapers')) - 1)]  # os.getcwd() donne le répertoire ou est executé le script, auquel on rajoute le dossier
    # Wallpapers, auquel s'ajoute un élément de la liste, pris aléatoirement entre 0 et le nombre d'image dans le dossier.
    # print(image) #On peut décommenter pour voir le chemin du dossier
    os.popen(
        'copy ' + image + ' c:\\Windows\Web\Wallpaper\Windows\wallpaper.jpg')  # Copie l'image choisie dans le dossier indiqué
    time.sleep(0.5)  # Applique un temps de pause pour laisser le temps de la copie
    ctypes.windll.user32.SystemParametersInfoW(20, 0, 'C:\\Windows\Web\Wallpaper\Windows\wallpaper.jpg',
                                               3)  # Modifie un fichier système pour changer le fond d'écran
    print(" --> Un fond d'écran a été choisi et appliqué à notre ordinateur.")  # Affiche ce message


# > INSTALLATION AUTOMATIQUE DE LOGICIELS (via Ninite)


def runNinite() :
    print(" --> Ninite va démarrer une installation de logiciel.") # Affiche ce message
    print(
        " --> A la fin de l'installation, appuyez sur 'Close' pour terminer le script ou attendez le redémarrage programmé.")
    for file in os.listdir() :  # Parcours le dossier, et dès qu'un fichier avec "Ninite" dans le nom est trouvé, il est considéré comme étant le Ninite a executer
        if 'Ninite' in file :
            ninite=file

    subprocess.run(os.getcwd() + '\\' + ninite)  # Lance le fichier ninite trouvé précedemment
    print(" --> Ninite à terminé.") # Affiche ce message


# > MISE A JOUR WINDOWS


def windowsUpdate() :
    subprocess.run(['powershell', '-Command', 'Install-WUUpdates -Updates $(Start-WUScan)'],
                   capture_output = True)  # Lance une commande lancer les MAJ windows
    print(" --> Les MAJ Windows sont lancées.") # Affiche ce message


# > CHANGEMENT DE DNS (CloudFlare)


def changeDns() :
    subprocess.run(['powershell', '-Command', 'netsh interface ip set dns name="Ethernet" static 1.1.1.1'],
                   capture_output = True)  # Lance une commande pour modifier les paramètres DNS de la carte "Ethernet"
    print(" --> Les DNS ont été changés.") # Affiche ce message


# > CHANGEMENT DU NOM DE POSTE


def computerName() :
    name=input("Que voulez-vous comme nom de poste ? ")  #
    subprocess.run(['powershell', '-Command', 'Rename-Computer -NewName', name],
                   capture_output = True)  # Lance une commande pour changer le nom du PC.
    print(" --> Maintenant notre poste s'appelle " + name + ".") # Affiche ce message


# > PLANIFIE UN REDEMARRAGE


def planReboot(timer) :
    subprocess.run(['powershell', '-Command', 'shutdown /r /t ' + str(timer)],
                   # Lance la commande pour planifier un redémarrage
                   capture_output = True)
    print(" --> L'ordinateur va redémarrer " + str(timer) + ' secondes.') # Affiche ce message


registryKeys()  # Modifie le registre pour plusieurs actions (Raccourcis, Corbeille, Message d'accueil)
changeWallpapers()  # Pioche au hasard parmis des fond d'écrans selectionnés afin d'en appliquer un
changeDns()  # Modifie les paramètres DNS IPV4 de la carte choisie
computerName()  # Modifie le nom du poste en posant la question
hibernate()  # Désactive la mise en veille
windowsUpdate()  # Lance les mises a jour windows qui s'appliqueront au prochain redémarrage
planReboot(900)  # Planifie un redémarrage pour finaliser l'installation et les paramètrages
runNinite()  # Lance ninite. Se trouve en dernier car le script attend que l'on ferme ninite pour continuer.
