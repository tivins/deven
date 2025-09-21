#!/usr/bin/env bash

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="${SCRIPT_DIR}/../.env"
TARGET_DATABASE="$1"  # Optional database name parameter


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

dump_database() {
    local db="$1"
    echo "🔄 Dumping database '$db'..."
    local filename="${db}_$(date +%Y%m%d_%H%M%S).sql"
    docker exec -it deven_web mysqldump -uroot -hdeven_db -p${DB_ROOT_PASSWORD} "$db" > "${BACKUP_DIR}/${filename}"
    echo "✅ Dump of database '$db' saved to ${filename}"
}

if [[ -n "$TARGET_DATABASE" ]]; then
    # Vérifie si la base existe avant de lancer le dump
    DB_EXISTS=$(docker exec -it deven_web mysql -sN -uroot -hdeven_db -p${DB_ROOT_PASSWORD} -e "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME='$TARGET_DATABASE';" | tr -d '\r')
    if [[ "$DB_EXISTS" == "$TARGET_DATABASE" ]]; then
        dump_database "$TARGET_DATABASE"
    else
        echo "❌ La base de données '$TARGET_DATABASE' n'existe pas."
        exit 1
    fi
else
    DATABASES=$(docker exec -it deven_web mysql -sN -uroot -hdeven_db -p${DB_ROOT_PASSWORD} -e"SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');" | tr -d '\r')
    for DATABASE in $DATABASES; do
        dump_database "$DATABASE"
    done
fi

