
import subprocess
import os

def get_installed_packages():
    try:
        # Exécutez la commande "pip freeze" via subprocess
        result = subprocess.run(['pip3', 'freeze'], capture_output=True, text=True, check=True)
        # Récupérez et retournez la sortie de la commande
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Appel de la fonction pour obtenir la liste des paquets installés
#installed_packages = get_installed_packages()
#print(installed_packages)

def afficher_contenu_repertoire(chemin):
    # Vérifier si le chemin spécifié est un répertoire
    if os.path.isdir(chemin):
        # Liste tous les éléments dans le répertoire
        contenu = os.listdir(chemin)

        # Afficher chaque élément
        for element in contenu:
            print(element)
    else:
        print("Le chemin spécifié n'est pas un répertoire.")

#afficher_contenu_repertoire("/app/share/gconvert/gconvert")
afficher_contenu_repertoire("/app/share/gconvert/gconvert/")


def progress_callback(progress):
    print(f'Progress: {progress:.2%}')


