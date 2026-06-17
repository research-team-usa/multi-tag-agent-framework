
# 🚀 Auron Agent - Quick-Start Setup

## Step 1: Merge Branch
This PR contains all necessary files. After the merge, the agent files will be available in the main branch.

```bash
git checkout main
git pull origin main
````

## Step 2: Enable Agent in GitHub

### Option A: Via GitHub Web Interface

1. Go to **Settings** → **Agents** (or **Actions** → **Agents**)
2. Click **"Create agent"** or **"Import from repository"**
3. Select the file: `.github/agents/auron-test-review.yml`
4. Confirm the permissions:
   * ✅ Read: repository contents, issues, PRs
   * ✅ Write: pull request comments (only!)
   * ❌ No push/merge permissions
5. **Save**

### Option B: Via GitHub CLI

```bash
gh agent create --config .github/agents/auron-test-review.yml \
  --permissions "contents:read,pull_requests:write"
```

## Step 3: Test the Agent

### Test 1: Create a PR manually

```bash
git checkout -b test/agent-check
echo "# Test PR for Auron Agent" >> README.md
git add .
git commit -m "Test: Verify Auron Agent works"
git push -u origin test/agent-check
```

Open a pull request and wait \~2-3 minutes. The agent should post a comment with:

* ✅ Status of the quick checks
* Link to the audit log

### Test 2: Verify audit log

```bash
cat reports/logs/audit.log
```

Should contain entries like:

```
2026-06-17T... | PR_CHECK_COMPLETE | PR#1 | status=passed
```

### Test 3: Test scheduled job (optional)

Trigger manually via GitHub Actions:

1. Go to **Actions** → **Scheduled Jobs**
2. Click **"Run workflow"**
3. Wait for completion → Artifacts should be available in `reports/`

## Step 4: Final permission validation

Make sure that the agent does **NOT**:

* ❌ Push code to branches
* ❌ Merge PRs
* ❌ Write secrets to logs
* ❌ Execute `file://` URLs

If any of these issues occur → disable immediately and create a security issue!

## 🔍 Verification Checklist

```
✅ Agent created and enabled
✅ Test PR posted (agent commented)
✅ Audit log contains entries
✅ Permissions are correct (read + PR comments only)
✅ Scheduled job runs without errors
✅ No local files are loaded
✅ Security rules are followed
```

## 📞 Problems?

| Problem                       | Solution                                                |
| ----------------------------- | ------------------------------------------------------- |
| Agent does not post a comment | Check permissions in Settings                           |
| Audit log is empty            | Agent has no write access; check repository permissions |
| Tests do not run              | Check Actions in workflows; install dependencies        |
| `file://` URLs are executed   | ⚠️ SECURITY ISSUE! Disable the agent immediately        |

## 📚 Additional Documents

---

- [Agent Configuration](./auron-test-review.yml)
- [PR Comment Template](./templates/pr-comment.md)
- [Audit Logs](../../reports/logs/audit.log)
- [GitHub Agents Docs](https://docs.github.com/en/actions/creating-github-agents)

---
