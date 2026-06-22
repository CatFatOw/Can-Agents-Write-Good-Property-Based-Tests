#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

rm -rf frontend-dist
mkdir -p frontend-dist

cp index.html app.js styles.css logo_new.png config.js frontend-dist/

if [ -d assets ]; then
  cp -R assets frontend-dist/assets
fi

if [ -d examples ]; then
  cp -R examples frontend-dist/examples
fi

cat > frontend-dist/config.js <<EOF
window.__IBD_CONFIG__ = {
  apiBaseUrl: "${API_BASE_URL:-}"
};
EOF
