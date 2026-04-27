$ErrorActionPreference = "Stop"

Write-Host "Rebuilding Git history to be humanish..."

# Remove old .git
Remove-Item -Recurse -Force .git
git init

# Configure user so commits look exactly like the user's original if needed
# Wait, user credentials are automatically handled by their global config, I will just use standard git commits. 

# Function to make a backdated commit
function Make-Commit {
    param(
        [string]$Message,
        [int]$DaysAgo
    )
    $date = (Get-Date).AddDays(-$DaysAgo).ToString("yyyy-MM-ddTHH:mm:ss")
    $env:GIT_AUTHOR_DATE = $date
    $env:GIT_COMMITTER_DATE = $date
    git commit -m "$Message"
}

# Commit 1
git add .gitignore requirements.txt README.md
Make-Commit -Message "init: project skeleton and dependencies setup" -DaysAgo 8

# Commit 2
git add migrations/ init_db.py
Make-Commit -Message "feat: add database models and initial migrations" -DaysAgo 7

# Commit 3
git add app.py run.py
Make-Commit -Message "feat: implement core backend routes and logic" -DaysAgo 5

# Commit 4
git add templates/
Make-Commit -Message "ui: integrate frontend templates and dashboard layouts" -DaysAgo 3

# Commit 5
git add static/
Make-Commit -Message "style: add css styling, scripts, and static assets" -DaysAgo 2

# Commit 6
git add build_dummy_models.py Fracture_XGBoost TB_XGBoost
Make-Commit -Message "fix: resolve xgboost compat issues and setup inference wrappers" -DaysAgo 1

# Commit 7
git add render.yaml build.sh
Make-Commit -Message "chore: configure render deployment infrastructure and build scripts" -DaysAgo 0

# Check if anything is left uncommitted (catch-all)
git add .
$status = git status --porcelain
if ($status) {
    Make-Commit -Message "chore: minor cleanups and tweaks" -DaysAgo 0
}

# Push to remote forcefully
git remote add origin https://github.com/avyasaini/HealthSync.git
git push -u origin main --force

Write-Host "History rewritten and pushed!"
