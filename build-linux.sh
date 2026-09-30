#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -c "import tkinter" 2>/dev/null || {
  printf 'Tkinter is required. Install python3-tk, then run this script again.\n' >&2
  exit 1
}

pyinstaller \
  --noconfirm \
  --clean \
  --onefile \
  --windowed \
  --name Azure-Learning \
  azure_learning_app.py

rm -rf release/Azure-Learning
mkdir -p release/Azure-Learning
cp dist/Azure-Learning release/Azure-Learning/
cp dist/Azure-Learning ./Azure-Learning
chmod +x release/Azure-Learning/Azure-Learning
chmod +x ./Azure-Learning

if [[ -d "${HOME}/Desktop" ]]; then
  cp dist/Azure-Learning "${HOME}/Desktop/Azure-Learning"
  chmod +x "${HOME}/Desktop/Azure-Learning"
fi

cat > release/Azure-Learning/run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec ./Azure-Learning
EOF
chmod +x release/Azure-Learning/run.sh

cat > release/Azure-Learning/Azure-Learning.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Azure Learning
Comment=Local AZ-900 exam preparation
Exec=/home/dimitri/workspace/projects/azure-learning/release/Azure-Learning/Azure-Learning
Path=/home/dimitri/workspace/projects/azure-learning/release/Azure-Learning
Icon=utilities-terminal
Terminal=false
Categories=Education;Development;
StartupNotify=true
EOF

printf 'Created release/Azure-Learning/\n'
