# 2100OS Automation System

Sistema inteligente de automação que detecta padrões, propõe ações e executa tarefas automaticamente.

## 🚀 Quick Start

```bash
# Detect patterns
python3 .gsd/automation/pattern_detector.py

# Run autopilot
python3 .gsd/automation/autopilot.py --mode balanced

# View dashboard
python3 .gsd/automation/dashboard.py
```

## 📋 Overview

O Automation System transforma o 2100OS de um sistema reativo para proativo:

1. **Detecta** padrões de uso automaticamente
2. **Propõe** ações baseadas em padrões detectados
3. **Avalia** o risco de cada proposta
4. **Executa** automaticamente (autopilot) ou solicita aprovação
5. **Aprende** com feedback contínuo

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    2100OS AUTOMATION ENGINE                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Analytics   │─────▶│  Pattern     │─────▶│  Action   │ │
│  │   Engine      │      │  Detector    │      │  Planner  │ │
│  └───────────────┘      └──────────────┘      └─────┬─────┘ │
│                                                       │       │
│                                                       ▼       │
│                                              ┌──────────────┐ │
│                                              │  Risk        │ │
│                                              │  Assessor    │ │
│                                              └──────┬───────┘ │
│                                                     │        │
│                     ┌───────────────┬──────────────┼────────┘ │
│                     ▼               ▼              │          │
│              ┌─────────────┐ ┌─────────────┐      │          │
│              │  Autopilot  │ │  Supervised │      │          │
│              │  (Auto)     │ │  (Ask User) │      │          │
│              └──────┬──────┘ └──────┬──────┘      │          │
│                     │                │             │          │
│                     ▼                ▼             │          │
│              ┌──────────────────────────────┐     │          │
│              │      Execution Engine        │◀────┘          │
│              └──────────────┬───────────────┘                │
│                             │                                │
│                             ▼                                │
│              ┌──────────────────────────────┐                │
│              │      Feedback Loop           │                │
│              └──────────────────────────────┘                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Components

### Pattern Detector
Detecta padrões recorrentes no uso do sistema:

- **Task Sequences**: Sequências de tarefas que ocorrem juntas
- **Temporal Patterns**: Tarefas que ocorrem em horários específicos
- **Inefficiencies**: Tarefas que levam mais tempo que o necessário
- **Underutilized Skills**: Skills com potencial mas pouco uso
- **Repetitive Tasks**: Tarefas repetitivas que poderiam ser automatizadas

### Action Planner
Transforma padrões detectados em propostas de ação:

- **CREATE_SKILL**: Criar nova skill para padrão repetitivo
- **OPTIMIZE_WORKFLOW**: Otimizar workflow existente
- **SCHEDULE_TASK**: Agendar tarefa recorrente
- **MERGE_SKILLS**: Combinar skills sempre usadas juntas
- **ARCHIVE_SKILL**: Arquivar skills obsoletas
- **CLEANUP**: Limpar padrões antigos

### Risk Assessor
Classifica o risco de cada proposta:

- **LOW** 🟢: Pode ser auto-executado
- **MEDIUM** 🟡: Requer aprovação
- **HIGH** 🔴: Manual only

### Execution Engine
Executa propostas aprovadas:

- Integração com GSD-2
- Suporte a dry-run
- Logging completo

### Autopilot
Executa ações automaticamente baseado em:

- Modo de operação (OFF, CONSERVATIVE, BALANCED, AGGRESSIVE)
- Thresholds dinâmicos
- Learning contínuo

### Dashboard
Interface de monitoramento em tempo real:

- Métricas principais
- Análise de performance
- Status do autopilot
- Agendamentos

## 📖 Usage

### Pattern Detection

```bash
# Detect all patterns
python3 .gsd/automation/pattern_detector.py

# Detect specific pattern types
python3 .gsd/automation/pattern_detector.py --type temporal
python3 .gsd/automation/pattern_detector.py --type sequences

# Save patterns to database
python3 .gsd/automation/pattern_detector.py --save
```

### Proposal Management

```bash
# List pending proposals
python3 .gsd/automation/proposal_cli.py --list pending

# View proposal details
python3 .gsd/automation/proposal_cli.py --view 123

# Approve proposal
python3 .gsd/automation/proposal_cli.py --approve 123

# Interactive mode
python3 .gsd/automation/proposal_cli.py --interactive
```

### Autopilot

```bash
# Check autopilot health
python3 .gsd/automation/autopilot.py --health

# Run autopilot in conservative mode
python3 .gsd/automation/autopilot.py --mode conservative --dry-run

# Run autopilot in production
python3 .gsd/automation/autopilot.py --mode balanced

# View learning insights
python3 .gsd/automation/autopilot.py --insights
```

### Dashboard

```bash
# Full dashboard
python3 .gsd/automation/dashboard.py

# Specific views
python3 .gsd/automation/dashboard.py --metrics
python3 .gsd/automation/dashboard.py --pending
python3 .gsd/automation/dashboard.py --autopilot

# Auto-refresh mode
python3 .gsd/automation/dashboard.py --watch
```

### Scheduler

```bash
# List schedules
python3 .gsd/automation/scheduler.py --list

# Add new schedule
python3 .gsd/automation/scheduler.py --add "weekly_report report 0 9 * * 1"

# Run pending tasks
python3 .gsd/automation/scheduler.py --run-once

# Start daemon
python3 .gsd/automation/scheduler.py --start
```

## ⚙️ Configuration

### Autopilot Modes

- **OFF**: Autopilot desligado
- **CONSERVATIVE**: Apenas LOW risk + alta confiança
- **BALANCED**: LOW + alguns MEDIUM risk
- **AGGRESSIVE**: Quase tudo automático

### Risk Thresholds

Configure em `autopilot.py`:

```python
# Ajuste thresholds conforme necessário
THRESHOLDS = {
    'CONSERVATIVE': {
        'low_max_confidence': 0.95,
        'medium_max_confidence': 0.0  # Never auto-approve medium
    },
    'BALANCED': {
        'low_max_confidence': 0.7,
        'medium_max_confidence': 0.85
    },
    'AGGRESSIVE': {
        'low_max_confidence': 0.5,
        'medium_max_confidence': 0.7
    }
}
```

## 🧪 Testing

```bash
# Run all tests
python tests/run_tests.py

# Run unit tests
python tests/run_tests.py unit

# Run integration tests
python tests/run_tests.py integration

# Verbose output
python tests/run_tests.py --verbose
```

## 📚 Documentation

- [API Reference](API_REFERENCE.md)
- [Architecture](ARCHITECTURE.md)
- [Autopilot Guide](AUTOPILOT_GUIDE.md)
- [Dashboard Guide](DASHBOARD_GUIDE.md)
- [Tutorial](TUTORIAL.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## 🤝 Contributing

O sistema está em constante evolução. Para contribuir:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 License

Este projeto é parte do 2100OS e segue a mesma licença.

---

**2100OS Automation System** - Seu negócio, no piloto automático 🚀
