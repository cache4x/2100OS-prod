# Como 2100OS + Hermes + Skills Funcionam

## 📋 Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    2100OS PRODUTO                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ Claude Code      │         │ Hermes Agent     │         │
│  │                  │         │                  │         │
│  │ Lê skills de:    │◄───────►│ Sincroniza:      │         │
│  │ .claude/skills/  │         │ .hermes/         │         │
│  │ ~/.claude/skills/│         │ .gsd/            │         │
│  └──────────────────┘         └──────────────────┘         │
│         ▲                            ▲                       │
│         │                            │                       │
│         └────────────┬───────────────┘                       │
│                      ▼                                       │
│              ┌──────────────┐                                │
│              │ 2100OS/      │                                │
│              │ CLAUDE.md    │                                │
│              │ SOUL.md      │                                │
│              │ MEMORY.md    │                                │
│              │ _memoria/    │                                │
│              └──────────────┘                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Como Funciona

### 1. **Skills do Claude Code**
As skills em `.claude/skills/` **são lidas pelo Claude Code**, não pelo Hermes:

```bash
# Claude Code busca skills aqui:
~/.claude/skills/          # Skills globais (seu sistema)
.local/2100OS/.claude/skills/  # Skills locais (projeto)
```

**Exemplo de uso:**
```
Você: /mmc-carrossel
Claude: Encontra .claude/skills/mmc-carrossel/SKILL.md
       Lê instruções e executa
       GSD registra a execução
       Hermes sincroniza com banco de dados
```

### 2. **Hermes Agent**
Gerencia sincronização e aprendizado contínuo:

```yaml
# .hermes/config.yaml
paths:
  gsd_db: "[CAMINHO]/.gsd/gsd.db"
  state_db: "[CAMINHO]/.hermes/state.db"

sync:
  enabled: true
  interval_seconds: 300  # Sincroniza a cada 5 min
```

### 3. **GSD (Google-Style Development)**
Registra tudo que acontece:
- Tasks executadas
- Skills usadas
- Aprendizados
- Padrões detectados

## 🚀 Como Instalar para Cliente

### Passo 1: Instalar 2100OS
```bash
# Cliente descompacta
tar -xzf 2100os-prod.tar.gz
cd 2100OS
```

### Passo 2: Configurar Caminhos
```bash
# Editar .hermes/config.cliente.yaml
# Substituir [CAMINHO_INSTALACAO] pelo caminho real
cp .hermes/config.cliente.yaml .hermes/config.yaml
```

### Passo 3: Instalar Dependências
```bash
npm install
```

### Passo 4: Iniciar Sistema
```bash
# Claude Code automaticamente carrega:
# - .claude/skills/ (skills locais)
# - 2100OS/CLAUDE.md (configuração)
# - 2100OS/_memoria/ (contexto do negócio)
```

## 🎯 Fluxo Completo de Operação

```
1. Cliente inicia: claude-code .
2. Claude Code lê:
   - 2100OS/CLAUDE.md
   - 2100OS/_memoria/empresa.md
   - 2100OS/_memoria/preferencias.md
   - 2100OS/_memoria/estrategia.md

3. Cliente executa skill: /mmc-carrossel
4. Claude executa skill
5. GSD registra execução
6. Hermes sincroniza bancos
7. Sistema aprende e melhora
```

## 📝 Estrutura de Arquivos

```
2100OS-prod/
├── 2100OS/                    # SISTEMA OPERACIONAL DO NEGÓCIO
│   ├── CLAUDE.md             # Configuração do Claude
│   ├── SOUL.md               # Alma do sistema
│   ├── MEMORY.md             # Memória do sistema
│   ├── _memoria/             # Memória do negócio
│   │   ├── empresa.md        # Template para cliente preencher
│   │   ├── preferencias.md   # Template para cliente preencher
│   │   └── estrategia.md     # Template para cliente preencher
│   ├── .claude/
│   │   └── skills/           # Skills do 2100OS (17 skills)
│   │       ├── mmc-carrossel/
│   │       ├── mmc-salvar/
│   │       └── ...
│   └── .gsd/                 # Sistema GSD completo
│
├── .hermes/                  # SISTEMA HERMES
│   ├── config.cliente.yaml  # Template de configuração
│   ├── state.db             # Banco de estado
│   └── sync/                # Sincronização
│
└── identidade/              # TEMPLATE DE MARCA
    ├── design-guide.md      # Template para personalizar
    ├── tokens.css           # Template para personalizar
    └── logo.svg             # Placeholder para logo
```

## 🔧 Configuração para Cliente

### Personalizar `_memoria/`:
```markdown
# empresa.md
**Nome:** [Nome da empresa]
**Negócio:** [O que fazem]
**O que faz:** [Descrição detalhada]
...
```

### Personalizar `identidade/`:
```bash
# Substituir campos [EM_COLCHETES] no design-guide.md
# Colocar logo real da empresa
# Ajustar cores e fontes
```

### Personalizar `.hermes/config.yaml`:
```yaml
paths:
  soul: "/caminho/real/2100OS/SOUL.md"
  # ... outros caminhos
```

## ✅ Resumo

- **Skills Claude Code**: Lidas automaticamente pelo Claude Code
- **Hermes**: Sincroniza bancos de dados e gerencia estado
- **GSD**: Registra operações e aprendizados
- **2100OS/**: Sistema operacional completo do negócio
- **Cliente preenche**: Apenas `_memoria/`, `identidade/` e `config.yaml`