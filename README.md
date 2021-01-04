# PROJET 6
> Dans le cadre de mon projet chez OpenClassRooms en tant que Administrateur infrastructure et cloud, j'ai décidé de faire un script qui automatise la préparation d'un ordinateur neuf ou fraîchement formaté. (Windows 10 uniquement)

## Table des matières
* [Information générale](#information-générale)
* [Exemples utilisation](#exemples-utilisation)
* [Prérequis](#prérequis)
* [Comment utiliser mon script](#comment-utiliser-mon-script)
* [Code](#code)
* [Status](#status)
* [Contact](#contact)

## Information générale

Après 8 ans en tant que technicien informatique, j'ai remarqué que beaucoup de tâches étaient répétitives et que l'automatisation nous ferait gagner énormément de temps. J'ai crée un script Python, qui "prépare" un ordinateur vierge. Voici la liste des actions : 

- Ajout raccourcis bureau "Ce PC" / "Fichiers de l'utilisateurs" / "Corbeille" et suppression du raccourci "OneDrive" si existant.
- "Corbeille" rajouté dans le menu "Periphériques et lecteurs".
- Message d'accueil personnalisé au démarrage. 
- Possibilité de désactiver Cortana (le script pose la question).
- Désactivation de la mise en veille prolongée.
- Changement du fond d'écran (le script prend un fond d'écran au hasard dans le dossier WallPapers que vous aurez rempli au préalable).
- Installation automatique de logiciels via Ninite (vous devez télécharger Ninite en choissisant les logiciels que vous désirez au préalable).
- Recherche et installation des mises à jour Windows.
- Changement des DNS en 1.1.1.1.
- Changement du nom du poste (le script demande quel nom vous désirez)
- Planifie un rédémarrage dans 15 minutes.

## Exemples utilisation

*Imaginez que vous êtes un technicien informatique et que vous devez installer une dizaine d'ordinateurs neufs (ou des ordinateurs que vous venez de formater par exemple) dans une société, vous pouvez utilisez ce script ! 

*Imaginez que vous êtes un revendeur informatique et que vous voulez configurer les ordinateurs neufs pour tous les clients qui achètent un ordinateur chez vous et bien, vous pourrez utiliser ce script ! 

*Ou alors imaginez tout simplement que vous êtes un utilisateur classique, vous venez d'acheter un ordinateur ou vous venez de le remettre à zéro. Utilisez ce script, vous gagnerez beaucoup de temps et vous aurez un ordinateur bien configuré et à jour ! 

## Prérequis

- Le script s'applique UNIQUEMENT sur Windows 10. 
- Vous devez installer Python sur votre ordinateur pour exécuter le script.
- Pour l'action "Changement du fond d'écran", vous devez créer un dossier "Wallpapers" qui se situera au même endroit que le script. Dans ce dossier, vous devez mettre autant d'images que vous désirez pour votre fond d'écran.
- Pour l'action "Installation automatique de logiciels" vous devez aller sur www.ninite.com, vous cochez les logiciels que vous désirez et ensuite vous appuyez sur "Get Your Ninite". Cela va télécharger un Ninite.exe, que vous placerez au même endroit que le script. 
- Pour l'action "Message d'accueil personnalisé au démarrage" vous devez modifier les deux messages que j'ai mis. "Votre ordinateur a été configuré par Nicolas PICARD" et "Si vous avez des questions, vous pouvez le joindre au 06 02 03 04 05". Remplacez ces deux phrases par ce que vous désirez ! 


## Comment utiliser mon script 

Comme mentionné dans les prérequis, vous devez installer Python sur votre ordinateur Windows. Pour cela je vous invite à vous rendre sur https://www.python.org/downloads/windows/ 
Une fois téléchargé, il vous suffira de suivre le processus d'installation (qui est plutôt rapide), vous pourrez laisser tous les choix par défaut. 
Une fois installé, nous allons pouvoir exécuter notre script. Je vous rappelle qu'il faut avoir notre exe "Ninite" et notre dossier "WallPapers" dans le même dossier que notre script. Vous pouvez exécuter le script depuis une clé USB, lecteur réseau etc... 
Une fois que vous êtes dans votre dossier où se trouve le script, nous allons exécuter notre script via "Powershell". Pour cela, faites "Fichier" en haut à gauche ensuite "Ouvrir Windows PowerShell" et pour finir "Ouvrir Windows Powershell en tant qu'administrateur".
Une console s'est ouverte et je vous invite à taper "py .\PréparationPC.py" (Remplacez  "PréparationPC" par le nom du script si vous avez renommez le script.) 
Le script commence...
Durant le script, deux questions seront posées : 

- "Voulez-vous desactiver cortana ? [o/N]" --> Si vous répondez "o", cortana sera désactivé. Si vous répondez "n" ou si vous laissez le champ vide, cortana ne sera pas désactivé. Si vous répondez autre chose, la question sera reposé jusqu'à temps que vous donniez une réponse acceptable. 

- "Que voulez-vous comme nom de poste ?" --> Entrez tout simplement le nom de poste que vous desirez. 

## Code 

Voici un exemple du code que vous trouverez dans le script, celui-ci réalise l'action de modifier le registre pour afficher/masquer certains raccourcis sur le bureau : 


    def registryKeys() :

    # Raccourcis du bureau (Fichiers de l'utilisateur, Ce PC, Corbeille, OneDrive)
    
     try: # Permet de tester le code
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
    except: # Si le code ne s'execute pas bien
        print (" --> Les raccourcis n'ont pas pu être paramétrés.") # Affiche ce message
    else: # Si le code s'execute bien
        print(" --> Les raccourcis ont été paramamétrés.") # Affiche ce message`


## Status

Le projet est terminé, tout est fonctionnel cependant nous pourrions faire des ajouts dans le futur. Voici quelques exemples d'idées à explorer :

- Action simple de modifier le registre pour changer le navigateur internet par défaut. (Google Chrome au lieu de Edge)
- Action complexe de supprimer les logiciels préinstallés inutiles (Les constructeurs adorent mettre pleins de logiciels inutiles et gourmands sur les ordinateurs neufs)
- Action complexe d'installer un logiciel de sauvegarde automatique et de mettre en place une sauvegarde tous les "x" jours par exemple. L'utilisateur final n'aura qu'a brancher son disque dur ou clé USB avant le lancement de le sauvegarde. 

etc... Pleins de choses peuvent être ajoutés et améliorés, la seule limite, c'est notre imagination ! 

## Contact
Crée par @Phaenomen - N'hésitez pas à me contacter en cas de besoin ! 
