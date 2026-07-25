#!/usr/bin/env bash
# ==============================================================================
# Script de Simulation d'Onboarding — AIPE_Framework (Étape 6.2)
# ==============================================================================
# Ce script automatise la validation du scénario « Zero-Setup Friction » :
# un développeur externe clone le projet, installe les dépendances et démarre
# le serveur, le tout en moins de 5 minutes.
#
# Il effectue un clonage propre dans un dossier temporaire, mesure le temps
# écoulé à chaque étape, et produit un rapport final.
#
# Usage :
#   ./scripts/simulate_onboarding.sh
#
# Ce script peut aussi être lancé via la cible Makefile :
#   make onboarding-check
# ==============================================================================

set -euo pipefail

# ==============================================================================
# SECTION 1 : CONSTANTES ET INITIALISATION
# ==============================================================================

# URL du dépôt distant (identique à `git remote get-url origin`)
REPO_URL="git@github.com:mdaadoun/AIPE_Framework.git"

# Seuil maximal d'onboarding en secondes (5 minutes = 300 secondes)
MAX_ONBOARDING_SECONDS=300

# Durée maximale d'attente pour le démarrage du serveur (en secondes)
SERVER_STARTUP_TIMEOUT=30

# Port sur lequel le serveur FastAPI écoutera pendant le test
TEST_PORT=8765

# Couleurs pour l'affichage (compatibles ANSI)
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color (réinitialisation)

# ==============================================================================
# SECTION 2 : FONCTIONS UTILITAIRES
# ==============================================================================

# Affiche un message d'étape avec horodatage
step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}▶ $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Affiche un message de succès
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Affiche un message d'erreur et quitte
fail() {
    echo -e "${RED}❌ ÉCHEC : $1${NC}"
    cleanup
    exit 1
}

# Affiche un avertissement
warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Nettoie le dossier temporaire et tue les processus résiduels
cleanup() {
    # Tuer le serveur de test s'il tourne encore
    if [ -n "${SERVER_PID:-}" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi

    # Supprimer le dossier temporaire
    if [ -n "${TEMP_DIR:-}" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

# Enregistrer le nettoyage en cas de sortie (même en cas d'erreur ou Ctrl+C)
trap cleanup EXIT

# ==============================================================================
# SECTION 3 : SIMULATION D'ONBOARDING
# ==============================================================================

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🚀 AIPE_Framework — Simulation d'Onboarding            ║"
echo "║        Validation du scénario Zero-Setup Friction           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# --- Chronomètre global ---
GLOBAL_START=$(date +%s)

# --- Étape 1 : Création du dossier temporaire isolé ---
step "Étape 1/5 : Création d'un dossier temporaire isolé"

TEMP_DIR=$(mktemp -d /tmp/aipe_onboarding_XXXXXX)
echo "  Dossier temporaire créé : $TEMP_DIR"
success "Environnement isolé prêt"

# --- Étape 2 : Clonage du dépôt ---
step "Étape 2/5 : Clonage du dépôt depuis GitHub"

CLONE_START=$(date +%s)
git clone "$REPO_URL" "$TEMP_DIR/AIPE_Framework" 2>&1 || fail "Le clonage Git a échoué"
CLONE_END=$(date +%s)
CLONE_DURATION=$((CLONE_END - CLONE_START))

success "Clonage terminé en ${CLONE_DURATION}s"

# Se positionner dans le projet cloné
CLONE_DIR="$TEMP_DIR/AIPE_Framework"

# --- Étape 3 : Installation via make install ---
step "Étape 3/5 : Exécution de 'make install' (Poetry + pre-commit)"

INSTALL_START=$(date +%s)

# Configurer Poetry pour créer le .venv localement (in-project)
# Cette commande est un prérequis que le développeur doit avoir configuré globalement
# ou que le README documente. On le force ici pour la simulation.
cd "$CLONE_DIR"
poetry config virtualenvs.in-project true --local 2>/dev/null || true
make install 2>&1 || fail "'make install' a échoué"

INSTALL_END=$(date +%s)
INSTALL_DURATION=$((INSTALL_END - INSTALL_START))

success "'make install' terminé en ${INSTALL_DURATION}s"

# --- Étape 4 : Vérifications de cohérence post-installation ---
step "Étape 4/5 : Vérifications de cohérence de l'environnement"

# 4a. Le .venv doit exister
if [ -d "$CLONE_DIR/.venv" ]; then
    success ".venv/ créé localement"
else
    fail "Le dossier .venv/ n'a pas été créé par 'make install'"
fi

# 4b. L'interpréteur Python doit être fonctionnel
if "$CLONE_DIR/.venv/bin/python" --version 2>/dev/null; then
    success "Interpréteur Python fonctionnel dans .venv/"
else
    fail "L'interpréteur Python dans .venv/ ne fonctionne pas"
fi

# 4c. Les dépendances de production doivent être importables
"$CLONE_DIR/.venv/bin/python" -c "import fastapi; import pydantic; import uvicorn; print('  FastAPI', fastapi.__version__, '| Pydantic', pydantic.__version__, '| Uvicorn', uvicorn.__version__)" \
    || fail "Les dépendances de production ne sont pas importables"
success "Dépendances de production importables"

# 4d. Les fichiers de configuration IDE doivent être présents
if [ -f "$CLONE_DIR/.vscode/settings.json" ]; then
    success ".vscode/settings.json présent"
else
    warn ".vscode/settings.json absent (étape 6.1 non commitée ?)"
fi

# 4e. Le hook pre-commit doit être installé
if [ -f "$CLONE_DIR/.git/hooks/pre-commit" ]; then
    success "Hook pre-commit installé dans .git/hooks/"
else
    warn "Hook pre-commit absent (le dépôt est-il un repo Git ?)"
fi

# --- Étape 5 : Démarrage du serveur FastAPI et test du healthcheck ---
step "Étape 5/5 : Démarrage de 'make dev' et test du healthcheck"

# Démarrer le serveur en arrière-plan sur un port de test dédié
cd "$CLONE_DIR"
"$CLONE_DIR/.venv/bin/python" -m uvicorn src.main:app --port "$TEST_PORT" &
SERVER_PID=$!

# Attendre que le serveur soit prêt (polling toutes les secondes)
echo "  Attente du démarrage du serveur (PID: $SERVER_PID)..."
WAIT_COUNT=0
SERVER_READY=false

while [ "$WAIT_COUNT" -lt "$SERVER_STARTUP_TIMEOUT" ]; do
    if curl -sf "http://localhost:${TEST_PORT}/health" > /dev/null 2>&1; then
        SERVER_READY=true
        break
    fi
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

if [ "$SERVER_READY" = true ]; then
    success "Serveur FastAPI démarré en ${WAIT_COUNT}s"

    # Récupérer la réponse du healthcheck
    HEALTH_RESPONSE=$(curl -sf "http://localhost:${TEST_PORT}/health")
    echo "  Réponse /health : $HEALTH_RESPONSE"

    # Vérifier que la réponse contient les champs attendus
    if echo "$HEALTH_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
assert data.get('status') == 'healthy', f'status={data.get(\"status\")}'
assert 'version' in data, 'version manquante'
assert 'environment' in data, 'environment manquant'
print('  Champs validés : status=healthy, version=' + data['version'] + ', environment=' + data['environment'])
" 2>&1; then
        success "Healthcheck /health conforme au contrat d'interface"
    else
        fail "La réponse /health ne respecte pas le contrat d'interface"
    fi
else
    fail "Le serveur n'a pas démarré dans les ${SERVER_STARTUP_TIMEOUT}s imparties"
fi

# Arrêter le serveur proprement
kill "$SERVER_PID" 2>/dev/null || true
wait "$SERVER_PID" 2>/dev/null || true
unset SERVER_PID

# ==============================================================================
# SECTION 4 : RAPPORT FINAL
# ==============================================================================

GLOBAL_END=$(date +%s)
TOTAL_DURATION=$((GLOBAL_END - GLOBAL_START))

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║               📊 RAPPORT D'ONBOARDING                      ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC}  Clonage Git .......................... ${GREEN}${CLONE_DURATION}s${NC}"
echo -e "${BLUE}║${NC}  make install ......................... ${GREEN}${INSTALL_DURATION}s${NC}"
echo -e "${BLUE}║${NC}  Vérifications de cohérence ........... ${GREEN}ok${NC}"
echo -e "${BLUE}║${NC}  Démarrage serveur + healthcheck ...... ${GREEN}${WAIT_COUNT}s${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"

if [ "$TOTAL_DURATION" -le "$MAX_ONBOARDING_SECONDS" ]; then
    echo -e "${BLUE}║${NC}  ${GREEN}⏱️  DURÉE TOTALE : ${TOTAL_DURATION}s / ${MAX_ONBOARDING_SECONDS}s (< 5 min) ✅${NC}"
    echo -e "${BLUE}║${NC}  ${GREEN}🏆 KPI Zero-Setup Friction : VALIDÉ${NC}"
    EXIT_CODE=0
else
    echo -e "${BLUE}║${NC}  ${RED}⏱️  DURÉE TOTALE : ${TOTAL_DURATION}s / ${MAX_ONBOARDING_SECONDS}s (> 5 min) ❌${NC}"
    echo -e "${BLUE}║${NC}  ${RED}📉 KPI Zero-Setup Friction : NON VALIDÉ${NC}"
    EXIT_CODE=1
fi

echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"

exit $EXIT_CODE
