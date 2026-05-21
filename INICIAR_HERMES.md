# Como Iniciar 2100OS + Hermes via Terminal

## 🚀 Iniciação Rápida

### Opção 1: Via Terminal (Direto)
```bash
# Entrar no diretório do projeto
cd 2100OS

# Iniciar Hermes
npm start

# Ou iniciar análise de padrões
npm run analyze

# Ou iniciar promoção de skills
npm run promote
```

### Opção 2: Via Antigravity
```bash
# Iniciar Antigravity com contexto 2100OS
antigravity --context 2100OS --start hermes

# Ou iniciar com CLI específica
antigravity --cli hermes --project ./2100OS
```

## 🔄 Arquitetura de Funcionamento

```
┌──────────────────────────────────────────────────────────────┐
│                     HERMES (Terminal)                        │
├──────────────────────────────────────────────────────────────┤
│ 1. Carrega contexto de 2100OS/                               │
│    - CLAUDE.md                                               │
│    - SOUL.md                                                 │
│    - MEMORY.md                                               │
│    - _memoria/                                               │
│                                                               │
│ 2. Lê skills de .claude/skills/                              │
│    - mmc-carrossel                                           │
│    - mmc-salvar                                              │
│    - mmc-analytics                                           │
│    - etc.                                                    │
│                                                               │
│ 3. Inicia gateway de interação                              │
│    - Telegram (opcional)                                     │
│    - Terminal CLI                                            │
│    - Antigravity interface                                   │
│                                                               │
│ 4. Sincroniza com GSD                                        │
│    - Registra operações                                     │
│    - Aprende padrões                                        │
│    - Gera novas skills                                      │
└──────────────────────────────────────────────────────────────┘
```

## 📋 Estrutura de Inicialização

### 1. **Carregamento de Contexto**
Quando você inicia o Hermes, ele carrega automaticamente:

```bash
# Hermes busca estes arquivos nesta ordem:
2100OS/CLAUDE.md          # Configurações do sistema
2100OS/SOUL.md            # Alma do negócio
2100OS/MEMORY.md          # Memória do sistema
2100OS/_memoria/empresa.md     # Contexto da empresa
2100OS/_memoria/preferencias.md # Preferências
2100OS/_memoria/estrategia.md   # Estratégia atual
```

### 2. **Carregamento de Skills**
```bash
# Hermes carrega skills de:
.claude/skills/            # Skills locais do 2100OS
~/.claude/skills/          # Skills globais do sistema

# Skills disponíveis:
/mmc-carrossel            # Criar carrosséis
/mmc-salvar               # Salvar no GitHub
/mmc-analytics            # Análise e insights
/mmc-instalar             # Instalar sistema
# ... (mais 13 skills)
```

### 3. **Interface de Interação**

#### Terminal CLI:
```bash
# Iniciar Hermes no terminal
hermes-cli --context 2100OS

# Comandos disponíveis:
hermes> /status          # Status do sistema
hermes> /patterns        # Padrões detectados
hermes> /execute [skill] # Executar skill
hermes> /memory [query]  # Buscar na memória
hermes> /help            # Ajuda
```

#### Antigravity:
```bash
# Iniciar via Antigravity
antigravity --project 2100OS --mode hermes

# Interface gráfica com:
- Dashboard de métricas
- Visualização de skills
- Controle de memória
- Análise de padrões
```

## 🎯 Comandos Principais

### Iniciar Sistema Completo:
```bash
# Terminal
cd 2100OS
npm start

# Antigravity
antigravity --context 2100OS --start full
```

### Análise de Padrões:
```bash
# Executar análise
npm run analyze

# Ver resultados
cat .hermes/logs/analysis.log
```

### Promoção de Skills:
```bash
# Promover skills detectadas
npm run promote

# Ver skills promovidas
ls .claude/skills/
```

### Status do Sistema:
```bash
# Verificar status
npm run status

# Ou via CLI
hermes-cli --status
```

## 🔧 Configuração para Cliente

### 1. Editar `.hermes/config.yaml`:
```yaml
paths:
  soul: "/caminho/do/cliente/2100OS/SOUL.md"
  memory: "/caminho/do/cliente/2100OS/MEMORY.md"

telegram:
  enabled: true
  bot_token_env: "TELEGRAM_BOT_TOKEN_CLIENTE"
```

### 2. Configurar Variáveis de Ambiente:
```bash
# .env
TELEGRAM_BOT_TOKEN=token_do_bot_do_cliente
TELEGRAM_USER_ID=id_do_cliente
NODE_ENV=production
```

### 3. Iniciar Sistema:
```bash
# Cliente inicia
cd 2100OS
npm start

# Sistema carrega:
- Contexto do negócio (_memoria/)
- Skills disponíveis (.claude/skills/)
- Configuração (CLAUDE.md)
- GSD integration (.gsd/)
```

## 📱 Fluxo Completo de Uso

```
1. Cliente: npm start
   ↓
2. Hermes carrega contexto de 2100OS/
   ↓
3. Carrega skills de .claude/skills/
   ↓
4. Inicia interface (Telegram/Terminal/Antigravity)
   ↓
5. Cliente executa: /mmc-carrossel
   ↓
6. Hermes executa skill
   ↓
7. GSD registra operação
   ↓
8. Sistema aprende e melhora
```

## 🎓 Exemplos Práticos

### Exemplo 1: Cliente via Terminal
```bash
# Cliente abre terminal
cd ~/2100OS

# Inicia Hermes
npm start

# Sistema responde:
"Hermes 2100OS v3.0 iniciado
Contexto carregado: [Nome da Empresa]
Skills disponíveis: 17
Interface: Terminal CLI

Comandos disponíveis:
  /status    - Ver status do sistema
  /patterns  - Ver padrões detectados
  /execute   - Executar skill
  /help      - Ajuda completa

hermes> _"

# Cliente digita:
hermes> /execute mmc-carrossel

# Hermes executa skill e registra no GSD
```

### Exemplo 2: Cliente via Antigravity
```bash
# Cliente inicia Antigravity
antigravity --context 2100OS

# Interface gráfica abre com:
- Dashboard principal
- Lista de skills disponíveis
- Memória do negócio
- Métricas e analytics

# Cliente clica em "Criar Carrossel"
# Antigravity chama Hermes
# Hermes executa /mmc-carrossel
# Resultado é exibido na interface
```

### Exemplo 3: Cliente via Telegram
```bash
# Cliente já configurou bot no .env
# Sistema inicia automaticamente gateway Telegram

# Cliente manda mensagem no Telegram:
"Quero criar um carrossel sobre novembro"

# Bot Hermes responde:
"Vou usar a skill /mmc-carrossel
Tema: Novembro
Identidade: Carregada
Analisando tendências...

[Carrossel gerado]

Deseja salvar? s/n"

# Cliente: "s"
# Hermes executa /mmc-salvar
# GSD registra operação completa
```

## 🔍 Verificação de Instalação

```bash
# Verificar se Hermes está funcionando:
cd 2100OS
npm run status

# Saída esperada:
✓ Hermes v3.0.0
✓ Contexto carregado: 2100OS/
✓ Skills carregadas: 17
✓ GSD conectado: .gsd/gsd.db
✓ Memória ativa: 543 registros
✓ Telegram: configurado (opcional)
```

## 📞 Suporte

Para problemas:
```bash
# Ver logs
cat .hermes/logs/hermes.log

# Verificar configuração
cat .hermes/config.yaml

# Testar conexão GSD
npm run test-gsd
```