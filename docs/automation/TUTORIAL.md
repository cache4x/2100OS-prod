# Automation System Tutorial

Bem-vindo ao tutorial do 2100OS Automation System! Este guia vai te ensinar passo a passo como usar o sistema de automação.

## 📚 Pré-requisitos

- 2100OS instalado
- Python 3.7+
- Conhecimento básico de linha de comando

## 🎯 Objetivos do Tutorial

Ao final deste tutorial, você será capaz de:
1. Detectar padrões no seu uso do sistema
2. Avaliar propostas de automação
3. Configurar o autopilot
4. Monitorar automações via dashboard
5. Criar suas próprias regras

---

## Lesson 1: Sua Primeira Detecção de Padrões

### O Que São Padrões?

Padrões são comportamentos recorrentes que o sistema detecta:

- **Task Sequences**: Você sempre faz A → B → C junto?
- **Temporal Patterns**: Você sempre faz algo segunda-feira às 9h?
- **Inefficiencies**: Alguma tarefa demora mais que o necessário?

### Detectando Padrões

```bash
# Entre no diretório
cd 2100OS

# Detecte padrões
python3 .gsd/automation/pattern_detector.py
```

**Saída esperada:**
```
🔍 DETECTING PATTERNS...
═════════════════════════════════════════════════════

✅ Task Sequences Found: 2
   - mmc-carrossel → mmc-seo (5 occurrences)
   - mmc-email-profissional → mmc-agendar (3 occurrences)

✅ Temporal Patterns Found: 1
   - mmc-relatorio-ads: Every Monday at 9:00 AM

✅ Inefficiencies Found: 1
   - mmc-email-profissional: 150s average (threshold: 120s)

📊 Total Patterns: 4
```

### Salvando Padrões

```bash
# Salve no banco de dados
python3 .gsd/automation/pattern_detector.py --save
```

**✅ Checkpoint:** Você detectou e salvou seus primeiros padrões!

---

## Lesson 2: Criando Propostas de Ação

### O Que São Propostas?

Propostas são ações sugeridas baseadas nos padrões detectados:
- Criar nova skill
- Otimizar workflow
- Agendar tarefa recorrente
- Arquivar skill obsoleta

### Gerando Propostas

```bash
# Crie propostas a partir dos padrões
python3 .gsd/automation/action_planner.py
```

**Saída esperada:**
```
📝 CREATING PROPOSALS...
═════════════════════════════════════════════════════

✅ Proposal #1: Automate Content Sequence
   Type: CREATE_SKILL
   Impact: 0.8
   Confidence: 0.9

   Combine mmc-carrossel + mmc-seo into single skill.

✅ Proposal #2: Weekly Analytics Report
   Type: SCHEDULE_TASK
   Impact: 0.7
   Confidence: 0.95

   Schedule weekly report for Mondays at 9:00 AM.

✅ Proposal #3: Optimize Email Creation
   Type: OPTIMIZE_WORKFLOW
   Impact: 0.6
   Confidence: 0.7

   Email creation takes 150s, could be optimized.

📊 Total Proposals: 3
```

### Salvando Propostas

```bash
# Salve propostas no banco
python3 .gsd/automation/action_planner.py --save
```

**✅ Checkpoint:** Você criou suas primeiras propostas de automação!

---

## Lesson 3: Avaliando Risco

### O Que É Avaliação de Risco?

Cada proposta é classificada por risco:
- **LOW** 🟢: Seguro para auto-executar
- **MEDIUM** 🟡: Requer revisão
- **HIGH** 🔴: Manual only

### Avaliando Propostas

```bash
# Avalie propostas pendentes
python3 .gsd/automation/risk_assessor.py --update
```

**Saída esperada:**
```
⚠️  RISK ASSESSMENT
═════════════════════════════════════════════════════

Proposal #1: Automate Content Sequence
Risk Level: 🟢 LOW
Score: 0.2
Factors:
  ✓ Non-destructive
  ✓ Reversible
  ✓ No database changes
  → Auto-executable: YES

Proposal #2: Weekly Analytics Report
Risk Level: 🟢 LOW
Score: 0.15
Factors:
  ✓ Non-destructive
  ✓ Reversible
  ✓ No database changes
  → Auto-executable: YES

Proposal #3: Optimize Email Creation
Risk Level: 🟡 MEDIUM
Score: 0.5
Factors:
  ✓ Non-destructive
  ✓ Reversible
  ⚠ Requires testing
  → Auto-executable: NO
```

**✅ Checkpoint:** Você avaliou o risco das suas propostas!

---

## Lesson 4: Usando o Autopilot

### O Que É Autopilot?

Autopilot avalia e executa propostas automaticamente baseado em:
- Modo de operação
- Thresholds de confiança
- Histórico de decisões

### Modos do Autopilot

**OFF**: Nada automático
**CONSERVATIVE**: Apenas LOW risk + altíssima confiança
**BALANCED**: LOW + alguns MEDIUM risk (recomendado)
**AGGRESSIVE**: Quase tudo automático

### Testando o Autopilot

```bash
# Primeiro, faça um dry-run (não executa nada)
python3 .gsd/automation/autopilot.py --mode balanced --dry-run
```

**Saída esperada:**
```
🤖 AUTOPILOT - MODE: BALANCED (DRY-RUN)
═════════════════════════════════════════════════════

Evaluating 3 pending proposals...

✅ Proposal #1: AUTO-APPROVED
   Confidence: 0.9 ≥ 0.7 (threshold)
   Risk: LOW
   → Would execute

✅ Proposal #2: AUTO-APPROVED
   Confidence: 0.95 ≥ 0.7 (threshold)
   Risk: LOW
   → Would execute

❌ Proposal #3: REJECTED
   Confidence: 0.7 < 0.85 (threshold for MEDIUM)
   Risk: MEDIUM
   → Requires manual approval

📊 Summary:
   Processed: 3
   Auto-approved: 2
   Rejected: 1
```

### Executando de Verdade

```bash
# Execute proposals (não mais dry-run!)
python3 .gsd/automation/autopilot.py --mode balanced
```

**✅ Checkpoint:** Você configurou e executou o autopilot pela primeira vez!

---

## Lesson 5: Monitorando com Dashboard

### O Que É Dashboard?

Dashboard é uma interface em tempo real para monitorar:
- Métricas principais
- Propostas pendentes
- Performance de automações
- Saúde do autopilot

### Abrindo o Dashboard

```bash
# Dashboard completo
python3 .gsd/automation/dashboard.py
```

**Saída esperada:**
```
📊 2100OS AUTOMATION DASHBOARD
═════════════════════════════════════════════════════

🎯 CORE METRICS
   Total Proposals: 23
   Pending: 3
   Approved: 15
   Executed: 12
   Success Rate: 92%

⏳ PENDING PROPOSALS
   #1: Weekly Report (LOW risk)
   #2: Content Skill (MEDIUM risk)
   #3: Email Optimization (MEDIUM risk)

📈 PERFORMANCE
   Approval Rate: 65%
   Execution Success: 92%
   Avg Duration: 45s

🤖 AUTOPILOT STATUS
   Mode: BALANCED
   Health: 87%
   Decisions Today: 5
   Success Rate: 90%

⏰ SCHEDULED TASKS
   Next: Weekly Report (in 2h 30m)
   Today: 3 tasks
   This Week: 12 tasks
```

### Views Específicas

```bash
# Apenas métricas principais
python3 .gsd/automation/dashboard.py --metrics

# Apenas propostas pendentes
python3 .gsd/automation/dashboard.py --pending

# Apenas status do autopilot
python3 .gsd/automation/dashboard.py --autopilot

# Auto-refresh a cada 5 segundos
python3 .gsd/automation/dashboard.py --watch
```

**✅ Checkpoint:** Você está monitorando suas automações!

---

## Lesson 6: Gerenciando Propostas Manualmente

### Interface Interativa

```bash
# Abra a interface interativa
python3 .gsd/automation/proposal_cli.py --interactive
```

**Menu:**
```
📝 PROPOSAL MANAGER
═════════════════════════════════════════════════════

1. List all proposals
2. List pending proposals
3. View proposal details
4. Approve proposal
5. Reject proposal
6. Batch approve (by risk/confidence)
7. Statistics
0. Exit

Choose an option:
```

### Aprovação Individual

```bash
# Aprovar proposta específica
python3 .gsd/automation/proposal_cli.py --approve 123
```

### Aprovação em Lote

```bash
# Aprovar todas LOW risk
python3 .gsd/automation/proposal_cli.py --batch-approve --risk LOW

# Aprovar todas com confiança ≥ 0.8
python3 .gsd/automation/proposal_cli.py --batch-approve --confidence 0.8
```

**✅ Checkpoint:** Você está gerenciando propostas manualmente!

---

## Lesson 7: Agendando Tarefas

### O Que São Agendamentos?

Tarefas recorrentes executadas automaticamente:
- Relatórios semanais
- Limpezas de banco
- Backups
- Análises periódicas

### Criando Agendamento

```bash
# Adicione um agendamento
python3 .gsd/automation/scheduler.py --add "weekly_report report 0 9 * * 1"
```

**Formato:** `nome tipo cron_expression`

**Cron examples:**
- `0 9 * * *` = Todos os dias às 9h
- `0 9 * * 1` = Toda segunda às 9h
- `*/5 * * * *` = A cada 5 minutos
- `0 0 * * 0` = Todo domingo à meia-noite

### Listar Agendamentos

```bash
# Ver todos os agendamentos
python3 .gsd/automation/scheduler.py --list
```

### Executar Agendamentos

```bash
# Executar tarefas pendentes uma vez
python3 .gsd/automation/scheduler.py --run-once

# Iniciar modo daemon (contínuo)
python3 .gsd/automation/scheduler.py --start
```

**✅ Checkpoint:** Você criou seus primeiros agendamentos!

---

## 🎓 Próximos Passos

Parabéns! Você completou o tutorial básico. Agora você pode:

### Aprofundar Conhecimentos

- Leia o [Autopilot Guide](AUTOPILOT_GUIDE.md)
- Consulte a [API Reference](API_REFERENCE.md)
- Veja a [Arquitetura](ARCHITECTURE.md)

### Explorar Funcionalidades Avançadas

- ML Pattern Detection
- Custom Patterns
- Performance Optimization

### Integrar com Seu Fluxo

- Configure modos do autopilot
- Crie agendamentos personalizados
- Monitore via dashboard regularmente

---

## 💡 Dicas

1. **Comece devagar**: Use modo CONSERVATIVE no início
2. **Monitore sempre**: Use o dashboard regularmente
3. **Teste primeiro**: Sempre use dry-run antes de executar
4. **Ajuste conforme necessário**: Modos e thresholds são configuráveis
5. **Aprende com feedback**: O sistema melhora com o tempo

---

**Tutorial completo!** Você está pronto para automatizar com o 2100OS! 🚀
