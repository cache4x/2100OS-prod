# 2100OS Hermes v2.0

**Sistema de Aprendizado Contínuo com Automação Inteligente**

---

## 🎯 O Que É

O 2100OS Hermes é um sistema que **aprende com o uso** e **cria automações automaticamente**:

- 🔍 Detecta padrões de uso repetitivos
- 🤖 Gera habilidades (skills) automaticamente
- 💾 Memória semântica com busca vetorial
- 📱 Controle via Telegram
- 🔄 Sincronização contínua entre bancos de dados

---

## 📋 Requisitos

- **Node.js** 18+ ([download](https://nodejs.org))
- **npm** (vem com Node.js)
- **Telegram Bot Token** ([obter em @BotFather](https://t.me/botfather))
- (Opcional) **OpenAI API Key** para embeddings semânticos

---

## 🚀 Instalação (3 minutos)

### 1. Descompactar

```bash
tar -xzf 2100os-hermes-2.0.0.tar.gz
cd 2100os-hermes-2.0.0
```

### 2. Executar Instalador

```bash
./install.sh
```

### 3. Configurar

Edite o arquivo `.env` com suas configurações:

```bash
# Telegram Bot (obter em @BotFather)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_USER_ID=987654321

# OpenAI (opcional)
OPENAI_API_KEY=sk-...

# Ambiente
NODE_ENV=production
```

### 4. Iniciar

```bash
npm run analyze
```

---

## 🎮 Comandos Disponíveis

```bash
npm run analyze     # Inicia análise de padrões
npm run promote     # Inicia promoção de skills
npm test            # Verifica status do sistema
```

---

## 📱 Controle via Telegram

Depois de configurado, use estes comandos no Telegram:

| Comando | Descrição |
|---------|-----------|
| `/status` | Ver status do sistema |
| `/patterns` | Ver padrões detectados |
| `/execute` | Executar skill |
| `/analytics` | Ver análises |
| `/memory` | Buscar na memória |
| `/help` | Ver todos os comandos |

---

## 📁 Estrutura do Sistema

```
2100os-hermes/
├── .hermes/
│   ├── learning/        # Detecção de padrões
│   ├── embeddings/      # Busca semântica
│   ├── sync/            # Sincronização
│   └── gateway/         # Integração Telegram
├── package.json
├── install.sh
└── .env.example
```

---

## 🔧 Configuração Avançada

### Modificar Frequência de Análise

Edite `.hermes/learning/batch_analyzer.js`:

```javascript
// Padrão: 2 AM todos os dias
cron.schedule('0 2 * * *', analyzePatterns);

// Exemplo: a cada hora
cron.schedule('0 * * * *', analyzePatterns);
```

### Ajustar Threshold de Padrões

Edite `.hermes/config.yaml`:

```yaml
learning:
  min_frequency: 3        # Mínimo de ocorrências
  confidence_threshold: 0.6 # Confiança mínima (0-1)
```

---

## 🐛 Problemas Comuns

**Erro: Cannot find module**
```bash
# Solução: reinstalar dependências
rm -rf node_modules
npm install
```

**Bot não responde**
```bash
# Verificar se token está correto no .env
# Verificar se chat_id está correto
```

---

## 📞 Suporte

- 📧 Email: [seu email]
- 📱 WhatsApp: [seu número]
- 📚 Documentação: [link da wiki]

---

**Versão:** 2.0.0 | **Licença:** Proprietária
