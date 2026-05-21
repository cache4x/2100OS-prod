# Começa AGORA - Guia Semana 1

## Meta: Instalar Hermes e fazer ele funcionar

**Tempo necessário:** 10 horas esta semana
**Resultado:** Hermes rodando localmente + Telegram bot respondendo

---

## Segunda-feira (2 horas)

### Tarefa 1: Entender o que é Hermes (1h)

Assista este vídeo (completo):
📺 [Create AI Agents with Memory, Skills, and Telegram 24/7](https://www.youtube.com/watch?v=OFZnlzUvF2g)

**Enquanto assiste, anote:**
- O que é SOUL.md?
- O que é MEMORY.md?
- Como o Telegram bot funciona?
- O que são skills?

### Tarefa 2: Ler documentação (1h)

Leia: 📚 [Hermes Agent - Five Pillars](https://www.mindstudio.ai/blog/hermes-agent-five-pillars-memory-skills-soul-crons/)

**Foque em entender:**
- 5 pilares (Memory, Skills, Soul, Crons, Self-Improvement)
- Como os componentes se conectam
- O que faz o Hermes único

---

## Terça-feira (3 horas)

### Tarefa 1: Instalar Hermes localmente (2h)

```bash
# 1. Clone o repositório
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Verifique instalação
python -m hermes --help
```

**Se der erro:**
- Google o erro
- Leia README do repositório
- Verifique se tem Python 3.10+

### Tarefa 2: Testar comando básico (1h)

```bash
# Rodar Hermes pela primeira vez
python -m hermes

# Deve pedir para criar SOUL.md
# Siga as instruções
```

**Resultado:** Hermes rodando localmente!

---

## Quarta-feira (3 horas)

### Tarefa 1: Criar SOUL.md para 2100OS (2h)

Crie arquivo `~/.hermes/SOUL.md`:

```markdown
# SOUL.md - 2100OS

## Quem Sou
2100OS - Sistema Operacional do Negócio

## Minha Missão
Ajudo empresários a automatizar operações, detectar padrões e executar tarefas automaticamente.

## Como Falo
- Português brasileiro
- Profissional mas acessível
- Direto, sem enrolação
- Prático e orientado a ação

## O Que Faço

### Detecção de Padrões
- Detecto tarefas repetitivas
- Identino ineficiências
- Encontro oportunidades de automação

### Criação de Skills
- Crio habilidades automaticamente
- Baseado em padrões detectados
- Sempre com aprovação do usuário

### Execução Automática
- Executo tarefas no piloto automático
- Com diferentes níveis de risco
- Notifico resultados via Telegram

## O Que Valorizo
- Eficiência acima de tudo
- Automação de tarefas manuais
- Aprendizado contínuo
- Transparência nas ações
- Nunca faço nada sem permissão (exceto risco baixo + aprovado)

## Como Trabalho

### Modos de Operação
- **CONSERVATIVE:** Só executo risco baixo com 95%+ confiança
- **BALANCED:** Risco baixo 70%+, médio 85%+
- **AGGRESSIVE:** Risco baixo 50%+, médio 70%+

### Sempre que Executar
1. Notifico via Telegram
2. Salvo resultado na memória
3. Aprendo com o feedback
4. Melhoro para próxima vez

### Sempre que Detectar Padrão
1. Analiso se é automatizável
2. Calculo confiança e risco
3. Propôs criação de skill
4. Aguardo aprovação

## Contexto do Negócio

### Cliente Alvo
- Donos de pequenas empresas (5-50 funcionários)
- Agências de marketing digital
- E-commerces em crescimento
- Consultores autônomos

### Problemas que Resolvo
- Tarefas repetitivas que consomem tempo
- Falta de visibilidade sobre operações
- Processos manuais que poderiam ser automáticos
- Conhecimento que fica na cabeça das pessoas

### Resultados que Entrego
- 40+ horas economizadas por mês
- Processos documentados automaticamente
- Memória do negócio persistente
- Operações que rodam sozinhas

## O Que NÃO Faço
- Não tomo decisões estratégicas (deixo com o dono)
- Não deleto nada sem confirmação explícita
- Não compartilho dados de clientes
- Não executo ações de risco alto automaticamente

## Como Quero Ser Lembrado
"O 2100OS mudou meu negócio - agora as coisas acontecem sozinhas e eu posso focar no que importa."
```

### Tarefa 2: Testar SOUL.md (1h)

```bash
# Reiniciar Hermes com novo SOUL.md
python -m hermes

# Testar conversação
# Perguntar: "Quem é você?"
# Perguntar: "O que você faz?"
# Verificar se usa contexto do SOUL.md
```

---

## Quinta-feira (2 horas)

### Tarefa 1: Configurar Telegram Bot (2h)

**Passo 1: Criar bot no Telegram (10 min)**
1. Abra Telegram e procure @BotFather
2. Envie `/newbot`
3. Siga as instruções:
   - Nome: `2100OS_bot`
   - Username: `seu_2100os_bot` (deve ser único)
4. Copie o TOKEN que o BotFather te der

**Passo 2: Obter seu User ID (5 min)**
1. No Telegram, procure @userinfobot
2. Envie qualquer mensagem
3. Ele responde com seu ID numérico
4. Copie esse ID

**Passo 3: Configurar Hermes com Telegram (45 min)**

```bash
# 1. Criar arquivo de configuração
export HERMES_TELEGRAM_BOT_TOKEN="seu_token_aqui"
export HERMES_TELEGRAM_USER_ID="seu_id_aqui"

# 2. Ou crie arquivo ~/.hermes/telegram_config.json
echo '{"bot_token": "seu_token_aqui", "user_id": "seu_id_aqui"}' > ~/.hermes/telegram_config.json

# 3. Testar conexão
python -m hermes.gateway.telegram

# 4. No Telegram, envie /start para seu bot
# Deve responder!
```

**Se funcionou:**
✅ Bot responde "/start"
✅ Você consegue conversar com ele

**Se não funcionou:**
- Verifique se o token está correto
- Verifique se o user_id está correto
- Google o erro específico

---

## Sexta-feira (opcional, 2-3 horas)

### Tarefa 1: Testar MEMORY.md (1h)

```bash
# 1. Adicionar memórias
echo "# Memórias do 2100OS

## Cliente Teste
- Nome: Empresa XYZ
- Setor: Marketing Digital
- Objetivo: Automatizar relatórios semanais

## Padrão Detectado
- Toda segunda às 9h: Gerar relatório de métricas
- Tarefa leva 2 horas
- É sempre a mesma sequência de passos

## Ação Tomada
- Proposta de automação criada
- Aguardando aprovação do cliente
" > ~/.hermes/MEMORY.md

# 2. Testar recuperação
python -m hermes
# Perguntar: "O que você lembra sobre Cliente Teste?"
# Deve recuperar do MEMORY.md
```

### Tarefa 2: Documentar aprendizado (1h)

Crie arquivo `NOTAS_SEMANA1.md`:

```markdown
# Notas - Semana 1 Hermes

## O que aprendi
- [Seus aprendizados aqui]

## O que funcionou
- [O que deu certo]

## O que não funcionou
- [O que deu errado]

## Dúvidas para próxima semana
- [Suas dúvidas]

## Próxima semana
- Integrar Hermes com 2100OS
- Melhorar Pattern Detector
- Criar primeira skill automática
```

---

## Checklist Semana 1

- [ ] Assisti vídeo completo do Hermes
- [ ] Li documentação dos 5 pilares
- [ ] Instalei Hermes localmente
- [ ] Criei SOUL.md para 2100OS
- [ ] Testei conversação com SOUL.md
- [ ] Criei bot no Telegram
- [ ] Configurei integração Telegram
- [ ] Bot responde /start
- [ ] Testei MEMORY.md
- [ ] Documentei aprendizados

---

## Se Der Tudo Certo...

**Parabéns!** Você está 12.5% do caminho (1/8 semanas).

**Próxima semana:** Integrar Hermes com código 2100OS existente.

---

## Se Der Errado...

**Problemas comuns:**

### Erro: Python não encontrado
```bash
# Instale Python 3.10+
# Mac: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

### Erro: Falta permissão
```bash
# Use chmod para dar permissão
chmod +x arquivo.sh
```

### Erro: Bot não responde
```bash
# Verifique se o token está correto
# Verifique se o user_id está correto
# Teste curl:
curl https://api.telegram.org/botSEU_TOKEN/getMe
```

### Erro: Não entendi algo
- Google o erro específico
- Leia README do Hermes no GitHub
- Pergunte em comunidades de Python/AI

---

## Precisa de Ajuda?

Se travar em algum ponto:
1. Google o erro específico
2. Leia documentação do Hermes
3. Teste com exemplo simples
4. Volte e tente de novo

**Lembre:** Nada de quebrar. É só código. Pode testar à vontade.

---

## Comemore no Final da Semana! 🎉

Se completou tudo:
- ✅ Hermes instalado
- ✅ SOUL.md criado
- ✅ Telegram bot funcionando
- ✅ MEMORY.md testado

**Mande no grupo/família:** "Semana 1 completa! Implementando sistema de AI único no mercado 😎"

---

## Próximo Passo

Semana 2: Integrar Hermes com código 2100OS

(Continue com o mesmo ritmo, 10h por semana)

**Boa sorte! 🚀**
