import json
import re

# Charger le fichier users.json
with open("users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# Fonction pour supprimer les chiffres
def remove_digits(text):
    return re.sub(r'\d+', '', text)

# Parcourir les utilisateurs et nettoyer les noms
for user in users:
    if 'first_name' in user:
        user['first_name'] = remove_digits(user['first_name'])
    if 'last_name' in user:
        user['last_name'] = remove_digits(user['last_name'])

# Sauvegarder les utilisateurs nettoyés dans un nouveau fichier
with open("users_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=4)

print("Nettoyage terminé. Résultat enregistré dans users_cleaned.json.")
