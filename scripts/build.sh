#!/bin/bash

# 2100OS Build Script
# Gera versão limpa do produto para deployment

set -e

echo "🔨 2100OS Build Script"
echo "======================"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuração
VERSION=$(node -p "require('../package.json').version")
PRODUCT_NAME="2100os-hermes"
BUILD_DIR="../dist"
PRODUCT_DIR="${BUILD_DIR}/${PRODUCT_NAME}-${VERSION}"

echo -e "${BLUE}Versão:${NC} ${VERSION}"
echo -e "${BLUE}Diretório de build:${NC} ${PRODUCT_DIR}"

# Limpar build anterior
echo ""
echo "🧹 Limpando build anterior..."
rm -rf "${BUILD_DIR}"
mkdir -p "${PRODUCT_DIR}"

# Criar estrutura do produto
echo ""
echo "📦 Criando estrutura do produto..."

# Copiar código fonte (.hermes/)
echo "  → Copiando .hermes/"
cp -r ../.hermes "${PRODUCT_DIR}/"

# Copiar package.json
echo "  → Copiando package.json"
cp ../package.json "${PRODUCT_DIR}/"

# Criar .env.example se não existir
if [ ! -f "${PRODUCT_DIR}/.env.example" ]; then
  echo "  → Criando .env.example"
  cat > "${PRODUCT_DIR}/.env.example" << 'EOF'
# 2100OS - Configurações do Cliente

# Telegram Bot
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_USER_ID=seu_chat_id_aqui
WEBHOOK_DOMAIN=seudominio.com

# OpenAI (opcional - para embeddings)
OPENAI_API_KEY=sk-...

# Ambiente
NODE_ENV=production
LOG_LEVEL=info
EOF
fi

# Criar README do produto
echo "  → Criando README_PRODUTO.md"
cat > "${PRODUCT_DIR}/README.md" << 'EOF'
# 2100OS Hermes - Sistema de Aprendizado Contínuo

Versão 2.0.0

## 🚀 Instalação Rápida

```bash
# 1. Instalar dependências
npm install

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 3. Inicializar banco de dados
node .hermes/embeddings/init_db.js

# 4. Iniciar o sistema
npm run analyze
```

## 📚 Documentação

Consulte a documentação completa em: [link da sua wiki/docs]

## 🆘 Suporte

Para suporte, contate: [seu email/WhatsApp]
EOF

# Criar script de instalação
echo "  → Criando install.sh"
cat > "${PRODUCT_DIR}/install.sh" << 'EOF'
#!/bin/bash

echo "🚀 2100OS Hermes - Instalação"
echo "=============================="

# Verificar Node.js
if ! command -v node &> /dev/null; then
  echo "❌ Node.js não encontrado. Instale em https://nodejs.org"
  exit 1
fi

echo "✅ Node.js encontrado: $(node --version)"

# Instalar dependências
echo ""
echo "📦 Instalando dependências..."
npm install

# Inicializar bancos de dados
echo ""
echo "🗄️ Inicializando bancos de dados..."
node .hermes/embeddings/init_db.js

# Configurar ambiente
if [ ! -f .env ]; then
  echo ""
  echo "⚙️ Configurando ambiente..."
  cp .env.example .env
  echo "✅ Arquivo .env criado. Edite com suas configurações."
fi

echo ""
echo "✅ Instalação completa!"
echo ""
echo "Próximos passos:"
echo "  1. Edite o arquivo .env com suas configurações"
echo "  2. Execute: npm run analyze"
echo ""
EOF

chmod +x "${PRODUCT_DIR}/install.sh"

# Calcular tamanho
echo ""
echo "📊 Estatísticas do build:"
SIZE=$(du -sh "${PRODUCT_DIR}" | cut -f1)
FILES=$(find "${PRODUCT_DIR}" -type f | wc -l)
echo "  → Tamanho: ${SIZE}"
echo "  → Arquivos: ${FILES}"

# Criar archive
echo ""
echo "📦 Criando archive..."
cd "${BUILD_DIR}"
tar -czf "${PRODUCT_NAME}-${VERSION}.tar.gz" "${PRODUCT_NAME}-${VERSION}"
echo "  → Archive: ${PRODUCT_NAME}-${VERSION}.tar.gz"

echo ""
echo -e "${GREEN}✅ Build completo!${NC}"
echo ""
echo "Arquivo gerado: ${BUILD_DIR}/${PRODUCT_NAME}-${VERSION}.tar.gz"
echo ""
echo "Para deploy:"
echo "  1. Copie o .tar.gz para o servidor do cliente"
echo "  2. Descompacte: tar -xzf ${PRODUCT_NAME}-${VERSION}.tar.gz"
echo "  3. Execute: cd ${PRODUCT_NAME}-${VERSION} && ./install.sh"
echo ""
