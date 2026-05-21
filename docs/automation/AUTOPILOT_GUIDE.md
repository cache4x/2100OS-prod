# Autopilot Guide

## 🎯 O Que É Autopilot

O Autopilot é um sistema inteligente que avalia e executa automaticamente propostas de automação baseado em:

- **Confiança da proposta** (confidence score)
- **Nível de risco** (risk level)
- **Impacto esperado** (impact score)
- **Histórico de decisões** (learning contínuo)

## 🚀 Modos de Operação

### OFF
Autopilot completamente desligado. Nenhuma ação automática.

**Quando usar:**
- Debugging e troubleshooting
- Testes de novas funcionalidades
- Quando você quer controle total

### CONSERVATIVE
Apenas propostas de baixo risco com altíssima confiança são auto-executadas.

**Thresholds:**
- LOW risk: confiança ≥ 95%
- MEDIUM risk: nunca auto-executa
- HIGH risk: nunca auto-executa

**Quando usar:**
- Começando a usar o autopilot
- Ambientes de produção críticos
- Quando você quer revisar a maioria das decisões

### BALANCED (Recomendado)
Equilíbrio entre automação e segurança.

**Thresholds:**
- LOW risk: confiança ≥ 70%
- MEDIUM risk: confiança ≥ 85%
- HIGH risk: nunca auto-executa

**Quando usar:**
- Uso diário do sistema
- Quando você confia moderadamente no autopilot
- Para maximizar automação mantendo segurança

### AGGRESSIVE
Quase tudo é auto-executado.

**Thresholds:**
- LOW risk: confiança ≥ 50%
- MEDIUM risk: confiança ≥ 70%
- HIGH risk: nunca auto-executa

**Quando usar:**
- Ambientes de teste/desenvolvimento
- Quando você quer máxima automação
- Quando você tem confiança total no sistema

## ⚙️ Configuração

### Definir Modo

```bash
# Usar CLI
python3 .gsd/automation/autopilot.py --set-mode --mode balanced

# Ou programaticamente
from autopilot import Autopilot
autopilot = Autopilot(conn)
autopilot.set_mode('BALANCED')
```

### Thresholds Personalizados

Edite `.gsd/automation/autopilot.py`:

```python
CUSTOM_THRESHOLDS = {
    'my_custom_mode': {
        'low_max_confidence': 0.8,
        'medium_max_confidence': 0.9,
        'high_max_confidence': 0.0
    }
}

autopilot.set_mode('my_custom_mode')
```

## 📊 Monitoramento

### Ver Saúde do Autopilot

```bash
python3 .gsd/automation/autopilot.py --health
```

**Output:**
```
🤖 AUTOPILOT HEALTH REPORT
═════════════════════════════════════════════════════
Mode: BALANCED
Overall Health: 87% ✅

Performance Metrics:
- Total Decisions: 234
- Success Rate: 91%
- Auto-Approval Rate: 68%
- Avg Confidence: 0.78

Recent Performance:
- Last 24h: 89% success
- Last 7 days: 87% success
- Last 30 days: 85% success

Learning Insights:
- Proposal types learned: 12
- Feedback accuracy: 94%
```

### Ver Learning Insights

```bash
python3 .gsd/automation/autopilot.py --insights
```

## 🎮 Como Usar

### 1. Dry-Run (Teste Sem Executar)

```bash
# Testar autopilot sem executar nada
python3 .gsd/automation/autopilot.py --mode balanced --dry-run
```

O dry-run mostra o que seria executado, mas não executa nada.

### 2. Executar Ciclo Manual

```bash
# Executar um ciclo de avaliação
python3 .gsd/automation/autopilot.py --mode conservative
```

O autopilot irá:
1. Buscar propostas pendentes
2. Avaliar cada uma
3. Auto-aprovar as que符合条件的
4. Executar as aprovadas
5. Registrar feedback

### 3. Modo Watch (Contínuo)

```bash
# Executar continuamente
python3 .gsd/automation/autopilot.py --mode balanced --watch
```

O autopilot irá executar ciclos continuamente.

## 🎯 Cenários de Uso

### Cenário 1: Weekly Report

**Proposta:**
```json
{
  "proposal_type": "SCHEDULE_TASK",
  "title": "Weekly Analytics Report",
  "confidence_score": 0.95,
  "risk_level": "LOW",
  "impact_score": 0.7
}
```

**Avaliação em BALANCED mode:**
- ✅ Risco LOW, confiança 95% ≥ 70%
- ✅ **Auto-aprovado e executado**

### Cenário 2: Nova Skill

**Proposta:**
```json
{
  "proposal_type": "CREATE_SKILL",
  "title": "New Content Skill",
  "confidence_score": 0.8,
  "risk_level": "MEDIUM",
  "impact_score": 0.8
}
```

**Avaliação em CONSERVATIVE mode:**
- ❌ Risco MEDIUM
- ❌ **Não auto-aprovado** (requer aprovação manual)

**Avaliação em AGGRESSIVE mode:**
- ✅ Risco MEDIUM, confiança 80% ≥ 70%
- ✅ **Auto-aprovado e executado**

### Cenário 3: Deletar Skill

**Proposta:**
```json
{
  "proposal_type": "DELETE_SKILL",
  "title": "Delete Unused Skill",
  "confidence_score": 0.99,
  "risk_level": "HIGH",
  "impact_score": 0.6
}
```

**Avaliação em QUALQUER mode:**
- ❌ Risco HIGH
- ❌ **Nunca auto-aprovado** (requer aprovação manual)

## 📈 Learning Contínuo

O autopilot aprende com cada decisão:

### 1. Feedback Automático

Quando uma proposta é executada:
- Se teve sucesso: aumenta confiança naquele tipo
- Se falhou: diminui confiança naquele tipo

### 2. Feedback Manual

```bash
# Registrar feedback manual
python3 .gsd/automation/autopilot.py --feedback --proposal-id 123 --correct
```

### 3. Ajuste Dinâmico de Thresholds

O autopilot ajusta automaticamente os thresholds baseado em:
- Taxa de sucesso recente
- Número de decisões
- Variância nas decisões

## ⚠️ Best Practices

### 1. Comece no Modo CONSERVATIVE

```bash
# Comece conservador
python3 .gsd/automation/autopilot.py --mode conservative --dry-run
```

### 2. Monitore a Saúde Regularmente

```bash
# Ver saúde diariamente
python3 .gsd/automation/autopilot.py --health
```

### 3. Use Dry-Run para Mudanças

```bash
# Teste novos modos com dry-run
python3 .gsd/automation/autopilot.py --mode aggressive --dry-run
```

### 4. Revise Propostas Pendentes

```bash
# Veja o que não foi auto-aprovado
python3 .gsd/automation/proposal_cli.py --list pending
```

### 5. Ajuste Baseado em Seu Fluxo

Se o autopilot está aprovando demais:
- Diminua para um modo mais conservador
- Aumente os thresholds

Se está aprovando de menos:
- Aumente para um modo mais agressivo
- Diminua os thresholds

## 🐛 Troubleshooting

### Autopilot não aprova nada

**Causa provável:** Mode muito conservador ou confiança baixa

**Solução:**
```bash
# Ver thresholds atuais
python3 .gsd/automation/autopilot.py --health

# Tentar modo mais agressivo
python3 .gsd/automation/autopilot.py --mode balanced
```

### Autopilot aprova tudo errado

**Causa provável:** Mode muito agressivo

**Solução:**
```bash
# Diminuir para modo conservador
python3 .gsd/automation/autopilot.py --mode conservative

# Registrar feedback negativo
python3 .gsd/automation/autopilot.py --feedback --proposal-id 123 --incorrect
```

### Saúde do Autopilot baixa

**Causa provável:** Muitas decisões incorretas

**Solução:**
```bash
# Ver insights
python3 .gsd/automation/autopilot.py --insights

# Possivelmente resetar learning
python3 .gsd/automation/autopilot.py --reset-learning
```

## 📚 Recursos Adicionais

- [Dashboard Guide](DASHBOARD_GUIDE.md) - Monitoramento em tempo real
- [API Reference](API_REFERENCE.md) - Referência completa da API
- [Troubleshooting](TROUBLESHOOTING.md) - Problemas comuns

---

**Autopilot** - Seu copiloto inteligente 🤖
