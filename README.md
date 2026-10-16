# Extracteur de CV avec l'API Gemini (Google Colab)

Ce projet est un script Python conçu pour être exécuté dans **Google Colab**. Il automatise l'extraction d'informations clés à partir d'un curriculum vitæ (CV) au format PDF en utilisant l'intelligence artificielle (modèle Gemini de Google) et exporte ces données dans un tableau Excel prêt à l'emploi.

## 🌟 Fonctionnalités

*   **Analyse Multimodale** : Téléversement et traitement natif des fichiers PDF sans avoir besoin d'un outil de reconnaissance optique de caractères (OCR) tiers.
*   **Extraction Structurée (JSON Schema)** : Force l'IA à renvoyer un format strict pour éviter les erreurs. Les champs extraits incluent : Nom, Prénom, Sexe, Téléphone, Email, Poste actuel, Entreprise, Expérience, Compétences, Niveau d'études, Langues, Liens et Ville.
*   **Export Excel Automatique** : Conversion immédiate des données JSON en un fichier `.xlsx` (Pandas/Openpyxl).
*   **Protection des données** : Le script intègre une étape de nettoyage automatique qui supprime le PDF des serveurs de Google immédiatement après l'analyse.

## 📋 Prérequis

Pour utiliser ce script, vous aurez besoin de :
1.  Un compte Google pour accéder à [Google Colab](https://colab.research.google.com/).
2.  Une clé API Gemini (gratuite ou payante), que vous pouvez générer sur [Google AI Studio](https://aistudio.google.com/).

## 🚀 Instructions d'utilisation

1.  **Créer un Notebook** : Ouvrez Google Colab et créez un nouveau notebook vierge.
2.  **Insérer le code** : Copiez l'intégralité du script Python et collez-le dans une cellule de code.
3.  **Ajouter votre clé API** : À l'Étape 3 du script, remplacez la valeur `"VOTRE_CLE_API_ICI"` par votre véritable clé API Gemini.
4.  **Exécuter le script** : Cliquez sur le bouton "Play" pour lancer la cellule.
    *   *Attention : Lors de la toute première exécution, l'installation des bibliothèques (`pip install`) peut vous demander de redémarrer l'environnement d'exécution (Runtime). Cliquez sur "Restart Session", puis relancez la cellule.*
5.  **Téléverser un CV** : Lorsque le script affiche le bouton d'importation, sélectionnez un fichier PDF depuis votre ordinateur.
6.  **Télécharger le résultat** : Une fois le traitement terminé par l'IA (généralement en moins de 10 secondes), le fichier Excel final sera généré et se téléchargera automatiquement sur votre machine.

## ⚠️ Note technique (Mise à jour SDK)

Si vous rencontrez une erreur du type `module 'google.genai' has no attribute 'configure'`, cela est dû à une transition en cours chez Google concernant leurs bibliothèques Python. 

Pour résoudre ce problème sans modifier le code, modifiez simplement la première ligne du script (Étape 1) pour installer l'ancienne version de la bibliothèque :
```bash
!pip install google-generativeai pandas openpyxl
```
Et remplacez `from google import genai` par `import google.generativeai as genai` à l'Étape 2.