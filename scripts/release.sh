#!/bin/bash

# 2100OS Release Script
# Gera build e envia para repositório de release

set -e

echo "🚀 2100OS Release Script"
echo "========================"

VERSION=$(node -p "require('../package.json').version")
PRODUCT_NAME="2100os-hermes"
BUILD_DIR="../dist"
RELEASE_DIR="${BUILD_DIR}/${PRODUCT_NAME}-${VERSION}"
DEV_REPO="git@github.com:cache4x/2100OS-dev.git"
RELEASE_REPO="git@github.com:cache4x/2100OS.git"

# 1. Verificar se estamos no branch de dev
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "⚠️ Você não está no branch main. Branch atual: $CURRENT_BRANCH"
  read -p "Continuar mesmo assim? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# 2. Build
echo ""
echo "📦 Gerando build..."
cd /Users/maxcurtolo/2100OS/scripts
bash build.sh

# 3. Preparar diretório de release
echo ""
echo "📋 Preparando release..."
cd "${RELEASE_DIR}"

# Inicializar git se não existir
if [ ! -d .git ]; then
  echo "Inicializando git..."
  git init
  git branch -M main
fi

# Adicionar remote de release
if ! git remote | grep -q release; then
  echo "Adicionando remote de release..."
  git remote add release "${RELEASE_REPO}"
fi

# 4. Commitar versão
echo ""
echo "📝 Commitando release..."
git add .
git commit -m "Release v${VERSION}" || echo "Nada mudou, atualizando..."

# 5. Forçar update para latest tag
echo ""
echo "🏷️ Atualizando tag latest..."
git tag -f latest
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# 6. Enviar para repo de release
echo ""
echo "📤 Enviando para repositório de release..."
git push release main --tags -f

echo ""
echo "✅ Release v${VERSION} enviado com sucesso!"
echo ""
echo "📦 Links:"
echo "   Repo dev:     https://github.com/cache4x/2100OS-dev"
echo "   Repo release: https://github.com/cache4x/2100OS"
echo "   Download:     https://github.com/cache4x/2100OS/releases"
echo ""
echo "📝 Cliente instala com:"
echo "   curl -sSL https://raw.githubusercontent.com/cache4x/2100OS/main/install.sh | bash"
echo ""
