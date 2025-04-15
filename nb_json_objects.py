import json

def compter_utilisateurs(nom_fichier):
    """
    Compte le nombre d'objets JSON (représentant des utilisateurs)
    dans un fichier JSON contenant une liste d'objets.

    Args:
        nom_fichier (str): Le chemin d'accès au fichier JSON.

    Returns:
        int: Le nombre d'utilisateurs trouvés.
             Retourne None si le fichier n'existe pas ou s'il y a une erreur de lecture/décodage.
    """
    try:
        with open(nom_fichier, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return len(data)
            else:
                print("Erreur: Le fichier ne contient pas une liste d'objets JSON à la racine.")
                return None
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{nom_fichier}' n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print("Erreur: Le fichier contient un JSON invalide.")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier: {e}")
        return None

nom_du_fichier = 'users600_GAP.json'  

nombre_utilisateurs = compter_utilisateurs(nom_du_fichier)

if nombre_utilisateurs is not None:
    print(f"Le fichier '{nom_du_fichier}' contient {nombre_utilisateurs} utilisateurs.")