#!/bin/sh
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh" && nvm use node >/dev/null
cd "$(dirname "$0")/slidev" && npm run dev
