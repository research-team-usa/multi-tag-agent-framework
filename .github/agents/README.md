# Auron Test & Review Agent

## 📋 Übersicht

Der **Auron Test & Review Agent** ist ein automatisierter GitHub Agent für das **Multi-Tag Agent Framework**. Er führt Tests durch, validiert YAML-Konfigurationen, überprüft PRs auf Sicherheitsprobleme und hält ein Audit-Log für prompt-injection-Muster.

## 🎯 Hauptaufgaben

1. **PR-Checks (schnell)**
   - Lint-Validierung
   - Unit-Tests (Smoke)
   - YAML-Fixture-Validierung
   - Prompt-Injection-Erkennung

2. **Geplante Tests (täglich 03:00 UTC)**
   - Vollständige Test-Suite (Integration, Security, Telemetry)
   - Coverage-Reports
   - Audit-Log-Verwaltung

3. **Issue-Triage**
   - Schnelle Kategorisierung
   - Prioritätsbestimmung
   - Verknüpfung mit bestehenden PRs

4. **Sicherheitsüberwachung**
   - Erkennung verdächtiger Muster
   - Lokale Datei-Referenzen protokollieren
   - Sicherheitsrelevante Dateien überwachen

## ⚙️ Konfiguration

### Agent aktivieren

Die Agent-Konfiguration befindet sich in `.github/agents/auron-test-review.yml`:

```bash
# Im GitHub-Interface:
# 1. Settings → Agents (oder Actions → Agents)
# 2. "Create agent" → YAML einlesen
# 3. Permissions bestätigen (read, write PR comments only)
# 4. Speichern
```

### Berechtigungen

Setze diese Berechtigungen:
- ✅ **Read**: Repository contents, issues, pull requests
- ✅ **Write**: Pull request comments (nur!)
- ❌ **Nicht**: Push zu Branches, Merging, Secrets

## 🚀 Trigger

| Event | Aktion | Beschreibung |
|-------|--------|-------------|
| Pull Request opened | Schnelle P0-Checks | Lint, Unit-Smoke, YAML-Validierung |
| Pull Request updated | Re-run checks | Erneute Validierung nach Updates |
| Issue opened | Triage-Vorschlag | Schnelle Kategorisierung |
| Schedule (03:00 UTC) | Volle Test-Suite | Integration, Security, Coverage |

## 📋 PR-Comment-Format

Der Agent postet einen strukturierten Kommentar mit:

```
✅ / ❌ Status (Lint, Unit, YAML)
- Failing tests (falls vorhanden)
- Suggested fixes (minimal repro)
- Security notes (Injektionen, lokale Dateien)
- Next steps
```

Beispiel:
```
Auron Test & Review Agent report:

Quick Checks: ✅
- Lint: ✅
- Unit smoke tests: ✅
- YAML validation: ✅

All checks passed! ✨

Audit trail: reports/logs/audit.log
```

## 🔒 Sicherheitsregeln (KRITISCH)

**Diese Regeln MÜSSEN eingehalten werden:**

1. ❌ **NIEMALS** `file://` URLs ausführen oder öffnen
2. ❌ **NIEMALS** lokale Dateien automatisch laden
3. ❌ **NIEMALS** verdächtige Tab-Befehle ausführen
4. ✅ **IMMER** lokale Datei-Referenzen protokollieren
5. ✅ **IMMER** verdächtige Muster als Log-Eintrag speichern

Bei Verdacht auf Sicherheitsproblem → Eintrag in `reports/logs/audit.log` + Kommentar zum PR

## 📊 Audit-Log

Das Audit-Log (`reports/logs/audit.log`) ist append-only und dokumentiert:

```
2026-06-17T18:57:00Z | LOCAL_FILE_REF | auron_test_suite.pdf | tabId=1577049782 | action=logged
2026-06-17T19:02:15Z | PROMPT_INJECTION | tests/fixtures/edge_cases.yaml:42 | pattern=<|im_start|> | action=flagged
2026-06-17T20:15:30Z | PR_CHECK_COMPLETE | PR#123 | status=passed | duration=45s
```

Zugriff:
```bash
cat reports/logs/audit.log
```

## ✅ Verifications-Checkliste

Nach Einrichtung überprüfen:

- [ ] Agent erstellt mit korrektem Namen (`Auron Test & Review Agent`)
- [ ] Konfigurationsdatei geladen: `.github/agents/auron-test-review.yml`
- [ ] Berechtigungen: read + PR comments only
- [ ] Trigger aktiviert: PR (opened, synchronize), Issue (opened), Schedule (03:00 UTC)
- [ ] Erster PR-Kommentar wird gepostet (Test mit echtem PR)
- [ ] Audit-Log-Datei erstellt: `reports/logs/audit.log`
- [ ] Täglicher Scheduled Job läuft (nachts 03:00 UTC)
- [ ] Agent führt KEINE `file://` URLs aus (siehe Audit-Log)

## 🔧 Troubleshooting

### Agent postet keinen Kommentar
- ✅ PR-Berechtigungen überprüfen
- ✅ Agent ist aktiv (Settings → Agents)
- ✅ Trigger ist für "pull_request.opened" konfiguriert

### Audit-Log wird nicht aktualisiert
- ✅ `reports/logs/` Verzeichnis existiert
- ✅ Agent hat Write-Zugriff auf Repository
- ✅ Agent führt Checks aus (siehe Actions-Log)

### Lokale Dateien werden geladen
- ⚠️ **SICHERHEITSPROBLEM!** Immediately:
  1. Agent deaktivieren
  2. Logs überprüfen (`reports/logs/audit.log`)
  3. Security-Issue erstellen
  4. Investigate & Fix

## 📝 Weitere Ressourcen

- [Agent Configuration](./auron-test-review.yml)
- [PR Comment Template](./templates/pr-comment.md)
- [Audit Logs](../../reports/logs/audit.log)
- [GitHub Agents Docs](https://docs.github.com/en/actions/creating-github-agents)

---

**Fragen?** Erstellen Sie ein Issue mit Label `[agent-setup]`.
