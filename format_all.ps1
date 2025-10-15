# Assurez-vous d'être dans l'environnement virtuel sniffer_venv
Write-Host "✅ Formatage et vérification du projet web-sniffer"

# Black : formate le code en excluant sniffer_venv
Write-Host "🔹 Running Black..."
black . --exclude "sniffer_venv|.venv"

# Isort : trie les imports en excluant sniffer_venv
Write-Host "🔹 Running Isort..."
isort . --skip "sniffer_venv" --skip ".venv"

# Ruff : lint & erreurs PEP8, exclut sniffer_venv
Write-Host "🔹 Running Ruff..."
ruff . --exclude "sniffer_venv,.venv,build,dist"

# Mypy : typage statique sur tes packages, ignore venv
Write-Host "🔹 Running Mypy..."
mypy web_sniffer core scrapers

Write-Host "✅ Tous les checks terminés."
