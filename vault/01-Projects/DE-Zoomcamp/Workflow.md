# 🔄 Data Engineering Co-working Workflow

This guide details how to work seamlessly between your **Local Windows** environment (Personal OS) and **Google Cloud Shell** (Development Environment).

---

## 1. Environment Philosophy

- **Use Windows for:**
    - 🧠 **Thinking**: Writing in Obsidian.
    - 📋 **Planning**: Managing tasks in Linear.
    - 🤖 **Automation**: Running skills like `/wrap-session`.
- **Use Cloud Shell for:**
    - 💻 **Coding**: Writing Python, SQL, Terraform.
    - 🐳 **Running**: Executing Docker containers.
    - ☁️ **Deploying**: Interacting with GCP.

---

## 2. One-Time Setup (Do This First)

We need to link your environments to your specific repository: `de-zoomcamp-2026`.

### On Local Windows
Open your database project folder and link the remote:
```powershell
cd "projects/data-engineering-zoomcamp"
git remote add origin https://github.com/oronculzac/de-zoomcamp-2026.git
git branch -M main

# Force push to overwrite the empty repo with your course materials
git push -u origin main --force
```

### On Cloud Shell
Inside your SSH session, verify the repo is correct:
```bash
cd ~/data-engineering-zoomcamp
git remote set-url origin https://github.com/oronculzac/de-zoomcamp-2026.git
git fetch
git reset --hard origin/main
```

---

## 3. The Golden Cycle

To make "Learning-in-Public" work, we must sync the state of these two worlds.

### Phase A: Start Session (Windows)

1. **Open Terminal**:
   ```powershell
   cd "C:\Users\Oron Culzac\antigravity_general"
   # Connect to your dev machine
   gcloud cloud-shell ssh --authorize-session
   ```

2. **Open Obsidian**:
   - Go to `Areas/DataEngineering/Modules`
   - Open current module note (e.g., `Module-01-Docker-Terraform`).

### Phase B: Do The Work (Cloud Shell)

Inside your SSH session:
1. **Navigate**: `cd data-engineering-zoomcamp`
2. **Code**: Use `vim`, `nano` or the built-in Editor.
3. **Run**: Execute your `docker run` or `python` commands.

> **💡 Note-taking Strategy**:
> - Keep Obsidian open on your side monitor.
> - When you learn a concept -> **Write in Obsidian**.
> - When you hit a bug -> **Paste error in Obsidian**.
> - When you solve it -> **Write solution in Obsidian**.

### Phase C: Save & Sync (Cloud Shell)

**Crucial Step**: Before you finish, you must push your code so your Assistant can see it.

```bash
# 1. Check what you changed
git status

# 2. Stage changes
git add .

# 3. Commit with a descriptive message
git commit -m "feat: implemented docker ingestion pipeline"

# 4. Push to GitHub
git push origin main
```

### Phase D: Wrap & Publish (Windows)

1. **Pull Changes**:
   ```powershell
   # In a local Windows terminal (not the SSH one)
   cd "projects/data-engineering-zoomcamp"
   git pull origin main
   ```

2. **Run Automation**:
   - Use the command: `/wrap-session`
   - The AI will read your local git changes + Linear tickets and generate your session log.

---

## 4. Troubleshooting

**"I can't push from Cloud Shell!"**
- Ensure you have a Personal Access Token (PAT) or SSH keys set up in GitHub.
- Config user: `git config --global user.email "oron.culzac@gmail.com"`

**"My session log is empty!"**
- Did you `git pull` locally?
- Did you actually commit changes in Cloud Shell?
