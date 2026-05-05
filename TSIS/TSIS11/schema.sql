-- TSIS 1 PhoneBook extended schema
-- Run this after your Practice 7-8 base schema exists.
-- Assumption: base table contacts already has at least id, name/username, phone, created_at/date_added.
-- This script is defensive and can be run more than once.

CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add date_added if your previous schema did not have it.
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_contacts_group_id ON contacts(group_id);
CREATE INDEX IF NOT EXISTS idx_contacts_birthday ON contacts(birthday);
CREATE INDEX IF NOT EXISTS idx_contacts_date_added ON contacts(date_added);
CREATE INDEX IF NOT EXISTS idx_phones_contact_id ON phones(contact_id);
CREATE INDEX IF NOT EXISTS idx_phones_phone ON phones(phone);

-- Optional migration helper:
-- If your old contacts table has a single phone column, copy it into phones once.
-- It only copies rows that do not already have that phone in phones.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'contacts'
          AND column_name = 'phone'
    ) THEN
        INSERT INTO phones(contact_id, phone, type)
        SELECT c.id, c.phone, 'mobile'
        FROM contacts c
        WHERE c.phone IS NOT NULL
          AND c.phone <> ''
          AND NOT EXISTS (
              SELECT 1 FROM phones p
              WHERE p.contact_id = c.id AND p.phone = c.phone
          );
    END IF;
END $$;
