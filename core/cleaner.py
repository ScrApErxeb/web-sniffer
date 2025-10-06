import re

def clean_text(text: str) -> str:
    """
    Nettoie le texte brut extrait :
    - Supprime les références type [34]
    - Corrige certains problèmes d'espacement
    - Supprime les espaces multiples
    """
    # Supprimer références [xx]
    text = re.sub(r'\[\d+\]', '', text)
    # Ajouter espace après ponctuation si manquant
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Supprimer espaces multiples
    text = ' '.join(text.split())
    return text
