# ATTENTION : Si vous exécutez ce script dans Google Colab pour la première fois,
# l'installation des bibliothèques ci-dessous (Étape 1) peut nécessiter un
# redémarrage du "runtime" (noyau).
#
# 1. Exécutez cette cellule une première fois.
# 2. Si le runtime redémarre (ou si vous voyez un message vous le demandant),
#    c'est normal.
# 3. Après le redémarrage, **ré-exécutez simplement cette même cellule**
#    pour lancer le script complet.

# ÉTAPE 1: Installer les bibliothèques nécessaires
# Installation du SDK Gemini, de Pandas pour la manipulation des données, et d'openpyxl pour l'export Excel.
!pip install google-genai pandas openpyxl

# ÉTAPE 2: Importer les bibliothèques
import os
import json
import pandas as pd
from google import genai
from google.genai import types
from google.genai.errors import APIError
from google.colab import files # Pour les fonctions d'upload et de download dans Colab

# ÉTAPE 3: Configuration de l'API Gemini
# REMPLACEZ "VOTRE_CLE_API_ICI" PAR VOTRE VRAIE CLÉ API GEMINI
GEMINI_API_KEY = "VOTRE_CLE_API_ICI"

try:
    # Note: L'ancien 'genai.Client' est obsolète. Utilisation de 'genai.configure' et 'GenerativeModel'
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Erreur lors de la configuration de genai : {e}")
    exit()

# ÉTAPE 4: Définition du NOUVEAU Schéma de Données (JSON Schema)
# Ce schéma force Gemini à extraire uniquement les champs demandés.
schema_simple_cv = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "Nom": types.Schema(type=types.Type.STRING, description="Nom de famille."),
        "Prenom": types.Schema(type=types.Type.STRING, description="Prénom."),
        "Sexe": types.Schema(type=types.Type.STRING, description="Déduire le sexe (Homme/Femme/Préfère ne pas le dire) basé sur le nom ou le contexte, sinon 'N/A'."),
        "Telephone": types.Schema(type=types.Type.STRING, description="Numéro de téléphone principal. 'N/A' si non trouvé."),
        "Email": types.Schema(type=types.Type.STRING, description="Adresse email principale. 'N/A' si non trouvé."),
        "Poste_Actuel": types.Schema(type=types.Type.STRING, description="Titre du poste le plus récent. 'N/A' si non trouvé."),
        "Entreprise_Actuelle": types.Schema(type=types.Type.STRING, description="Nom de l'entreprise la plus récente. 'N/A' si non trouvé."),
        "Annees_Experience": types.Schema(type=types.Type.STRING, description="Nombre total d'années d'expérience professionnelle (ex: '5 ans'). Si non trouvé, 'N/A'."),
        "Competences": types.Schema(
            type=types.Type.ARRAY,
            description="Liste des compétences clés (techniques et soft skills).",
            items=types.Schema(type=types.Type.STRING)
        ),
        "Niveau_Etudes": types.Schema(type=types.Type.STRING, description="Le plus haut diplôme ou niveau d'études (ex: 'Master en Informatique', 'Bac+5'). 'N/A' si non trouvé."),
        "Langues": types.Schema(
            type=types.Type.ARRAY,
            description="Liste des langues et leur niveau (ex: 'Français (Natif)', 'Anglais (Courant)').",
            items=types.Schema(type=types.Type.STRING)
        ),
        "Lien_CV": types.Schema(type=types.Type.STRING, description="Lien vers portfolio, LinkedIn ou site web, si présent. Sinon 'N/A'."),
        "Ville": types.Schema(type=types.Type.STRING, description="Ville de résidence actuelle, si présente. Sinon 'N/A'.")
    },
    # Optionnel : Forcer tous les champs à être présents, même si 'N/A'
    required=["Nom", "Prenom", "Sexe", "Telephone", "Email", "Poste_Actuel", "Entreprise_Actuelle", "Annees_Experience", "Competences", "Niveau_Etudes", "Langues", "Lien_CV", "Ville"]
)


# ÉTAPE 5: Téléchargement du fichier PDF par l'utilisateur
print("\n--- Veuillez télécharger le fichier PDF du CV ---")
try:
    uploaded = files.upload()

    if not uploaded:
        print("? Aucun fichier n'a été téléchargé. Opération annulée.")
        exit()

    # Obtention du nom du fichier téléchargé
    pdf_filename = list(uploaded.keys())[0]
    pdf_data = list(uploaded.values())[0]

except Exception as e:
    print(f"Erreur lors de l'upload via Colab : {e}")
    print("Veuillez réessayer d'exécuter la cellule.")
    exit()


# ÉTAPE 6: Traitement du fichier avec Gemini API
# Utilisation de la nouvelle API 'genai'
print(f"? Fichier '{pdf_filename}' téléchargé sur Colab.")
print("--- Envoi du fichier à l'API Gemini pour analyse ---")
try:
    # 1. Uploader le fichier à l'API
    # Nous utilisons 'display_name' pour garder une trace du nom original
    gemini_file = genai.upload_file(contents=pdf_data, display_name=pdf_filename, mime_type="application/pdf")
    print(f"? Fichier bien chargé sur Gemini API. (URI: {gemini_file.uri})")

    # 2. Configuration du modèle et de la requête
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

    # Configuration pour forcer la sortie JSON
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=schema_simple_cv
    )

    # NOUVEAU Prompt
    prompt_text = "Extrayez les informations spécifiques du CV ci-joint (Nom, Prénom, Sexe, Téléphone, Email, Poste actuel, Entreprise actuelle, Années d'expérience, Compétences, Niveau d'études, Langues, Lien CV, Ville) et structurez-les dans le schéma JSON spécifié. Répondez en français. Si une information n'est pas trouvée, mettez 'N/A'."

    # 3. Appel au modèle
    response = model.generate_content(
        contents=[
            gemini_file, # Le fichier uploadé
            prompt_text  # Le prompt
        ],
        generation_config=generation_config
    )

    # 4. Récupération et parsing du JSON
    json_data = response.text
    cv_data = json.loads(json_data)
    print("? Extraction des données réussie au format JSON.")

except APIError as e:
    print(f"? Erreur de l'API Gemini : {e}")
    if 'gemini_file' in locals():
        genai.delete_file(gemini_file.name)
    exit()
except json.JSONDecodeError as e:
    print(f"? Erreur de décodage JSON : {e}. Le modèle n'a pas retourné de JSON valide.")
    print(f"Sortie brute de Gemini (pour vérification) : {response.text}")
    if 'gemini_file' in locals():
        genai.delete_file(gemini_file.name)
    exit()
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")
    if 'gemini_file' in locals():
        genai.delete_file(gemini_file.name)
    exit()
finally:
    # Nettoyage : Suppression du fichier sur l'API Gemini
    if 'gemini_file' in locals():
        try:
            genai.delete_file(gemini_file.name)
            print(f"? Fichier '{gemini_file.display_name}' supprimé de Gemini API.")
        except Exception as e:
            print(f"?? Attention : Échec de la suppression du fichier sur Gemini API. ({e})")


# ÉTAPE 7: Conversion en fichier Excel (Feuille Unique)
# =================================================================================
print("--- Création du fichier Excel ---")

# Préparation des données pour le DataFrame
# Les champs 'Competences' et 'Langues' sont des listes, nous les joignons en une chaîne de caractères.
competences_str = ', '.join(cv_data.get('Competences', []) or ['N/A'])
if competences_str.strip() == '': competences_str = 'N/A'

langues_str = ', '.join(cv_data.get('Langues', []) or ['N/A'])
if langues_str.strip() == '': langues_str = 'N/A'

# Création d'un dictionnaire de données pour une seule ligne
# Les clés du dictionnaire (ex: "N° de téléphone") deviendront les en-têtes de colonnes dans Excel.
# Nous utilisons .get(key, 'N/A') pour récupérer les données du JSON et éviter les erreurs.
data_dict = {
    "Fichier_Source": [pdf_filename],
    "Nom": [cv_data.get('Nom', 'N/A')],
    "Prénom": [cv_data.get('Prenom', 'N/A')],
    "Sexe": [cv_data.get('Sexe', 'N/A')],
    "N° de téléphone": [cv_data.get('Telephone', 'N/A')],
    "Email": [cv_data.get('Email', 'N/A')],
    "Poste Actuel": [cv_data.get('Poste_Actuel', 'N/A')],
    "Entreprise actuel": [cv_data.get('Entreprise_Actuelle', 'N/A')],
    "Nbre d'années d’expérience": [cv_data.get('Annees_Experience', 'N/A')],
    "Compétences": [competences_str],
    "Niveau d'études": [cv_data.get('Niveau_Etudes', 'N/A')],
    "Langue": [langues_str], # Nom de colonne au singulier comme demandé
    "Lien du CV": [cv_data.get('Lien_CV', 'N/A')],
    "Ville": [cv_data.get('Ville', 'N/A')]
}

# Création du DataFrame final
df_final = pd.DataFrame(data_dict)

# Définition du nom du fichier de sortie
excel_filename = f"Extraction_CV_Simple_{os.path.splitext(pdf_filename)[0].replace(' ', '_')}.xlsx"

# Écriture du DataFrame dans UNE SEULE feuille Excel
try:
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_final.to_excel(writer, sheet_name='Extraction_CV', index=False)

    print(f"\n--- Processus terminé ---")
    print(f"? Le fichier Excel '{excel_filename}' a été créé avec 1 feuille.")

    # ÉTAPE 8: Téléchargement du fichier Excel sur votre machine
    files.download(excel_filename)

except Exception as e:
    print(f"Erreur lors de la création ou du téléchargement du fichier Excel : {e}")
