#!/bin/bash
# Script to configure the Git post-commit monitoring and push workflow
# Target Repository: ~/AQARION-BRT-LAB-20260919

set -euo pipefail

REPO_DIR="$HOME/AQARION-BRT-LAB-20260919"
HOOK_FILE="$REPO_DIR/.git/hooks/post-commit"
ALERT_EMAIL="${ALERT_EMAIL:-developer@example.com}"

cd "$REPO_DIR"

# 1. Create executable Git post-commit hook
cat << 'EOF' > "$HOOK_FILE"
#!/bin/bash
set -eo pipefail

REPO_DIR="$(git rev-parse --show-toplevel)"
ALERT_EMAIL="${ALERT_EMAIL:-developer@example.com}"
SMTP_SERVER="${SMTP_SERVER:-localhost}"
SMTP_PORT="${SMTP_PORT:-25}"

echo "==> [AQARION-BRT Monitor] Running automated verification..."

# Execute verification script and capture output
BUILD_OUTPUT=$(mktemp)
VERIFY_EXIT=0

if [ -f "$REPO_DIR/verify.sh" ]; then
    "$REPO_DIR/verify.sh" > "$BUILD_OUTPUT" 2>&1 || VERIFY_EXIT=$?
else
    echo "ERROR: verify.sh not found at root" > "$BUILD_OUTPUT"
    VERIFY_EXIT=1
fi

if [ $VERIFY_EXIT -eq 0 ]; then
    echo "==> [AQARION-BRT Monitor] Verification PASSED. Triggering auto-push to origin master..."
    
    # Push changes to origin master
    if git push origin master; then
        echo "==> [AQARION-BRT Monitor] Push to origin master completed successfully."
    else
        echo "==> [AQARION-BRT Monitor] ERROR: Git push failed." >&2
        VERIFY_EXIT=2
    fi
else
    echo "==> [AQARION-BRT Monitor] FAILURE DETECTED (Exit Code $VERIFY_EXIT). Aborting auto-push." >&2
fi

# Send Email Alert if build/validation or push failed
if [ $VERIFY_EXIT -ne 0 ]; then
    echo "==> [AQARION-BRT Monitor] Sending failure alert email to $ALERT_EMAIL..."
    
    python3 - <<PYTHON_ALERT
import smtplib
from email.message import EmailMessage
import os

email_to = os.environ.get("ALERT_EMAIL", "$ALERT_EMAIL")
smtp_server = os.environ.get("SMTP_SERVER", "$SMTP_SERVER")
smtp_port = int(os.environ.get("SMTP_PORT", "$SMTP_PORT"))

commit_hash = "$USER"
try:
    import subprocess
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
except Exception:
    pass

msg = EmailMessage()
msg['Subject'] = f"[ALERT] AQARION-BRT Automated Build/Validation Failed (Commit {commit_hash[:7]})"
msg['From'] = "aqarion-monitor@local"
msg['To'] = email_to

with open("$BUILD_OUTPUT", "r") as f:
    logs = f.read()

body = f"""AUTOMATED VALIDATION ALERT

Repository: AQARION-BRT-LAB-20260919
Commit: {commit_hash}
Exit Code: {VERIFY_EXIT}

--- VERIFICATION LOGS ---
{logs}
"""
msg.set_content(body)

try:
    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.send_message(msg)
    print("Email notification dispatched successfully.")
except Exception as e:
    print(f"Failed to send email alert via SMTP ({smtp_server}:{smtp_port}): {e}")
PYTHON_ALERT

fi

rm -f "$BUILD_OUTPUT"
exit $VERIFY_EXIT
EOF

# 2. Make hook executable
chmod +x "$HOOK_FILE"

echo "AQARION-BRT post-commit hook configured successfully at $HOOK_FILE"
