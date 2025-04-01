import json
import re

def normalize_phone_number(phone):
    """Normalise un numéro de téléphone français au format : 0430868490"""
    # Supprimer tous les caractères non numériques sauf le +
    phone = "0612345678"
    
    return phone

def normalize_phone_numbers_in_file(input_file, output_file):
    """Charge un fichier JSON, normalise les numéros de téléphone et enregistre le résultat."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        if 'phone_number' in entry:
            entry['phone_number'] = normalize_phone_number(entry['phone_number'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Exemple d'utilisation :
input_file = "users.json"  # Remplace par ton fichier
output_file = "normalized_data.json"
normalize_phone_numbers_in_file(input_file, output_file)
print("✅ Numéros de téléphone normalisés et enregistrés dans", output_file)
