# Quick Reference - Automation System

## Command Summary

```bash
# Pattern Detection
python3 .gsd/automation/pattern_detector.py              # All patterns
python3 .gsd/automation/pattern_detector.py --save        # Save patterns

# Proposal Management
python3 .gsd/automation/proposal_cli.py --list pending    # List pending
python3 .gsd/automation/proposal_cli.py --approve 123     # Approve
python3 .gsd/automation/proposal_cli.py --interactive     # Interactive

# Autopilot
python3 .gsd/automation/autopilot.py --health             # Check health
python3 .gsd/automation/autopilot.py --mode balanced      # Run cycle
python3 .gsd/automation/autopilot.py --dry-run            # Test mode

# Dashboard
python3 .gsd/automation/dashboard.py                      # Full dashboard
python3 .gsd/automation/dashboard.py --watch              # Auto-refresh

# Scheduler
python3 .gsd/automation/scheduler.py --list               # List schedules
python3 .gsd/automation/scheduler.py --add "task type cron"  # Add
```

## Risk Levels

- 🟢 **LOW**: Auto-executable
- 🟡 **MEDIUM**: Requer aprovação
- 🔴 **HIGH**: Manual only

## Autopilot Modes

- **OFF**: Nada automático
- **CONSERVATIVE**: LOW + 95%+ confiança
- **BALANCED**: LOW + 70%, MEDIUM + 85%
- **AGGRESSIVE**: LOW + 50%, MEDIUM + 70%

## Cron Examples

```
0 9 * * *      # Diário às 9h
0 9 * * 1      # Segundas às 9h
0 0 * * 0      # Domingos à meia-noite
*/5 * * * *    # A cada 5 minutos
0 */2 * * *    # A cada 2 horas
```

## Common Issues

| Problema | Solução |
|----------|---------|
| Autopilot não aprova | Diminua modo ou verifique confiança |
| Dashboard vazio | Execute pattern_detector primeiro |
| Erro de execução | Use dry-run para debug |
| Scheduler não funciona | Verifique expressão cron |

## File Locations

```
.gsd/automation/
├── pattern_detector.py      # Detection
├── action_planner.py        # Planning
├── risk_assessor.py         # Risk assessment
├── execution_engine.py      # Execution
├── scheduler.py             # Scheduling
├── autopilot.py             # Autopilot
└── dashboard.py             # Dashboard

tests/
├── unit/                    # Unit tests
├── integration/             # Integration tests
└── run_tests.py             # Test runner

docs/automation/
├── README.md                # Main doc
├── AUTOPILOT_GUIDE.md       # Autopilot guide
└── TUTORIAL.md              # Tutorial
```
