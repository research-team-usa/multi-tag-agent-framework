# 🚀 Auron Agent - Quick-Start Setup

## Schritt 1: Branch mergen
Diese PR enthält alle notwendigen Dateien. Nach dem Merge sind die Agent-Dateien im Main-Branch vorhanden.

```bash
git checkout main
git pull origin main
```

## Schritt 2: Agent in GitHub aktivieren

### Variante A: Über GitHub Web-Interface
1. Gehe zu **Settings** → **Agents** (oder **Actions** → **Agents**)
2. Klick **"Create agent"** oder **"Import from repository"**
3. Wähle die Datei: `.github/agents/auron-test-review.yml`
4. Bestätige die Berechtigungen:
   - ✅ Read: repository contents, issues, PRs
   - ✅ Write: pull request comments (only!)
   - ❌ Keine Push/Merge-Rechte
5. **Speichern**

### Variante B: Über GitHub CLI
```bash
gh agent create --config .github/agents/auron-test-review.yml \
  --permissions "contents:read,pull_requests:write"
```

## Schritt 3: Teste den Agent

### Test 1: Manuell einen PR erstellen
```bash
git checkout -b test/agent-check
echo "# Test PR for Auron Agent" >> README.md
git add .
git commit -m "Test: Verify Auron Agent works"
git push -u origin test/agent-check
```

Öffne einen Pull Request und warte ~2-3 Minuten. Der Agent sollte einen Kommentar posten mit:
- ✅ Status der Quick-Checks
- Link zum Audit-Log

### Test 2: Audit-Log überprüfen
```bash
cat reports/logs/audit.log
```

Sollte Einträge enthalten wie:
```
2026-06-17T... | PR_CHECK_COMPLETE | PR#1 | status=passed
```

### Test 3: Scheduled Job testen (optional)
Manuell auslösen über GitHub Actions:
1. Gehe zu **Actions** → **Scheduled Jobs**
2. Klick **"Run workflow"**
3. Warte auf Completion → Artifacts sollten in `reports/` verfügbar sein

## Schritt 4: Berechtigungen final validieren

Stelle sicher, dass der Agent **NICHT**:
- ❌ Code zu Branches pusht
- ❌ PRs mergt
- ❌ Secrets in Logs schreibt
- ❌ `file://` URLs ausführt

Falls eines dieser Probleme auftritt → sofort deaktivieren und Security-Issue erstellen!

## 🔍 Verifikations-Checkliste

```
✅ Agent erstellt und aktiviert
✅ Test-PR gepostet (Agent kommentierte)
✅ Audit-Log enthält Einträge
✅ Berechtigungen sind korrekt (nur read + PR comments)
✅ Scheduled Job läuft ohne Fehler
✅ Keine lokalen Dateien werden geladen
✅ Sicherheitsregeln werden eingehalten
```

## 📞 Probleme?

| Problem | Lösung |
|---------|--------|
| Agent postet keinen Kommentar | Berechtigungen in Settings überprüfen |
| Audit-Log ist leer | Agent hat kein Schreib-Zugriff; Repository-Berechtigungen überprüfen |
| Tests laufen nicht | Actions in Workflows überprüfen; Dependencies installieren |
| `file://` URLs werden geladen | ⚠️ SICHERHEITSPROBLEM! Agent sofort deaktivieren |

## 📚 Weitere Dokumente

- [Agent Configuration](.github/agents/auron-test-review.yml)
- [Agent README](.github/agents/README.md)
- [Audit Logs](./reports/logs/audit.log)

---

**Erfolg!** 🎉 Der Auron Test & Review Agent ist jetzt bereit für die Aktivierung.
