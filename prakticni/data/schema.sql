CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    master_password_hash VARCHAR(255) NOT NULL,
    mk_salt VARCHAR(255) NOT NULL,
    pdk_salt VARCHAR(255) NOT NULL,
    public_key VARCHAR(255) NOT NULL,
    private_key_encrypted VARCHAR(255) NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    lockout_count INTEGER DEFAULT 0,
    lockout_until DATETIME NULL,
    last_key_rotation DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    encrypted_name VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    binary TINYINT NOT NULL,
    date_uploaded DATETIME NOT NULL,
    date_modified DATETIME,
    dek_encrypted VARCHAR(255) NOT NULL,
    hash VARCHAR(255) NOT NULL,
    locked TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message VARCHAR(255) NOT NULL,
    hash_curr VARCHAR(255),
    hash_prev VARCHAR(255)
);
