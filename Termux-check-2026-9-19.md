cd ~/Aqarion-Quantarion-AI

cat > setup-github-auth-termux.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

REPO_DIR="${1:-$PWD}"
HOST="github.com"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$HOME/.config/git-auth-backups/$STAMP"
GIT_CONFIG_BACKUP="$BACKUP_DIR/gitconfig"
REMOTE_BACKUP="$BACKUP_DIR/remotes.txt"

say() {
  printf '
==> %s
' "$*"
}

warn() {
  printf '
WARNING: %s
' "$*" >&2
}

die() {
  printf '
ERROR: %s
' "$*" >&2
  exit 1
}

command -v pkg >/dev/null 2>&1 || die "This script is intended for Termux; pkg was not found."

[ -d "$REPO_DIR/.git" ] || die "Not a Git repository: $REPO_DIR"
cd "$REPO_DIR"

say "Repository: $(pwd)"
say "Installing/updating required Termux packages"
pkg update -y
pkg install -y git gh

mkdir -p "$BACKUP_DIR"
if [ -f "$HOME/.gitconfig" ]; then
  cp -p "$HOME/.gitconfig" "$GIT_CONFIG_BACKUP"
fi
git remote -v > "$REMOTE_BACKUP" 2>/dev/null || true

say "Current Git remotes"
git remote -v || true

if ! git remote get-url origin >/dev/null 2>&1; then
  die "No origin remote exists. Add the HTTPS clone URL first, then rerun:
git remote add origin https://github.com/OWNER/REPOSITORY.git"
fi

ORIGIN_URL="$(git remote get-url origin)"
PUSH_URL="$(git remote get-url --push origin 2>/dev/null || printf '%s' "$ORIGIN_URL")"

say "Checking origin URL for embedded credentials"

if printf '%s
%s
' "$ORIGIN_URL" "$PUSH_URL" | grep -Eq 'https://[^/@:]+:[^/@]+@github.com/'; then
  warn "Embedded credential detected in the GitHub remote."
  warn "It is being removed from the remote configuration."
  warn "If this was a real token, revoke it in GitHub because it may be in shell history."
  CLEAN_URL="$(printf '%s' "$ORIGIN_URL" | sed -E 's#https://[^/@:]+:[^/@]+@github.com/#https://github.com/#')"
  git remote set-url origin "$CLEAN_URL"
  git remote set-url --push origin "$CLEAN_URL"
  ORIGIN_URL="$CLEAN_URL"
fi

case "$ORIGIN_URL" in
  https://github.com/*)
    ;;
  git@github.com:*)
    warn "SSH remote detected. This script configures HTTPS authentication."
    warn "Switching origin to HTTPS form."
    PATH_PART="${ORIGIN_URL#git@github.com:}"
    PATH_PART="${PATH_PART%.git}"
    ORIGIN_URL="https://github.com/${PATH_PART}.git"
    git remote set-url origin "$ORIGIN_URL"
    git remote set-url --push origin "$ORIGIN_URL"
    ;;
  *)
    die "Origin is not a recognizable github.com remote:
$ORIGIN_URL
Set it to the exact HTTPS clone URL from GitHub, then rerun."
    ;;
esac

say "Sanitized remote"
git remote -v

say "Clearing only conflicting GitHub credential-helper settings"
git config --global --unset-all credential.helper 2>/dev/null || true
git config --local --unset-all credential.helper 2>/dev/null || true

say "Checking GitHub CLI authentication"
if ! gh auth status --hostname "$HOST" >/dev/null 2>&1; then
  cat <<'PROMPT'

GitHub browser/device authentication is required next.

In the interactive prompts:
  1. Select GitHub.com.
  2. Select HTTPS for Git operations.
  3. Select Login with a web browser.
  4. Complete the one-time code flow in your phone browser.
  5. Approve access only after confirming the GitHub account is JASKSG9.

Do not paste a PAT into a Git remote URL.
PROMPT
  gh auth login --hostname "$HOST" --git-protocol https --web
fi

say "Configuring Git to use GitHub CLI as credential helper"
gh auth setup-git --hostname "$HOST"

say "Authentication status"
gh auth status --hostname "$HOST"

say "Git credential helper configuration"
git config --show-origin --get-all credential.helper || true

say "Testing read access without changing the repository"
git ls-remote origin HEAD >/dev/null

say "Testing authenticated GitHub API identity"
gh api user --jq '.login'

BRANCH="$(git branch --show-current)"
say "Current branch: ${BRANCH:-detached HEAD}"

cat <<'DONE'

SUCCESS: GitHub CLI is authenticated and configured as Git's credential helper.

Normal future workflow:
  git pull --ff-only
  git add <files>
  git commit -m "message"
  git push

No GitHub password or manually pasted PAT should be required for normal HTTPS pushes.

Backups created at:
DONE
printf '  %s
' "$BACKUP_DIR"

cat <<'OPTIONAL'

Optional write test:
  A read-only auth test already passed. To test a real push, create a harmless
  branch and push that branch:

    TEST_BRANCH="auth-test-$(date +%Y%m%d-%H%M%S)"
    git switch -c "$TEST_BRANCH"
    git commit --allow-empty -m "chore: verify GitHub CLI authentication"
    git push -u origin "$TEST_BRANCH"

  After confirming it appeared on GitHub, remove it:

    git switch main
    git push origin --delete "$TEST_BRANCH"
    git branch -D "$TEST_BRANCH"

Do not run a dummy push directly to main merely to test authentication.
OPTIONAL
EOF

chmod 700 setup-github-auth-termux.sh
