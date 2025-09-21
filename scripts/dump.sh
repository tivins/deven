#!/usr/bin/env bash

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="${SCRIPT_DIR}/../.env"


# Load credentials
if [[ ! -f "$CREDENTIALS_FILE" ]]; then
    echo "❌ Fichier de credentials non trouvé: $CREDENTIALS_FILE"
    exit 1
fi

source "$CREDENTIALS_FILE"

# trim BACKUP_DIR value and remove trailing slash
BACKUP_DIR=$(echo "$BACKUP_DIR" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;s/\/$//')

echo "ℹ️ Backup dir: '$BACKUP_DIR'."

# check if backup dir exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory does not exist: $BACKUP_DIR"
    exit 1
fi

# Load databases
DATABASES=$(docker exec -it deven_web mysql -sN -uroot -hdeven_db -p${DB_ROOT_PASSWORD} -e"SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');" | tr -d '\r')

for DATABASE in $DATABASES; do
    echo "🔄 Dumping database '$DATABASE'..."
    FILENAME="${DATABASE}_$(date +%Y%m%d_%H%M%S).sql"
    docker exec -it deven_web mysqldump -uroot -hdeven_db -p${DB_ROOT_PASSWORD} $DATABASE > ${BACKUP_DIR}/${FILENAME}
    echo "✅ Dump of database '$DATABASE' saved to ${FILENAME}"
done

