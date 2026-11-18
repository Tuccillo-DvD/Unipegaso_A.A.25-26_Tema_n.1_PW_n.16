-- Necessaria per i vincoli di esclusione
-- che impediscono sovrapposizioni temporali.
CREATE EXTENSION IF NOT EXISTS btree_gist;


CREATE TABLE utente (
    id_utente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    cognome VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(30) NOT NULL,
    ruolo VARCHAR(30) NOT NULL,
    telefono VARCHAR(30),
    data_creazione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    attivo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT check_utente_ruolo
        CHECK (ruolo IN ('PAZIENTE', 'MEDICO', 'SEGRETERIA', 'ADMIN'))
);


CREATE TABLE paziente (
    id_paziente INTEGER PRIMARY KEY,
    codice_fiscale VARCHAR(16) NOT NULL UNIQUE,
    data_nascita DATE NOT NULL,
    indirizzo VARCHAR(50),

    CONSTRAINT fk_paziente_utente
        FOREIGN KEY (id_paziente)
        REFERENCES utente(id_utente)
        ON DELETE CASCADE
);



CREATE TABLE medico (
    id_medico INTEGER PRIMARY KEY,
    numero_albo VARCHAR(30) NOT NULL UNIQUE,

    CONSTRAINT fk_medico_utente
        FOREIGN KEY (id_medico)
        REFERENCES utente(id_utente)
        ON DELETE CASCADE
);



CREATE TABLE esame (
    id_esame INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descrizione TEXT,
    durata_minuti INTEGER NOT NULL,
    prezzo NUMERIC(5,2) NOT NULL,
    attivo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT check_esame_durata
        CHECK (durata_minuti > 0),

    CONSTRAINT check_esame_prezzo
        CHECK (prezzo >= 0)
);



CREATE TABLE specializzazione (
    id_specializzazione INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descrizione TEXT
);



CREATE TABLE medico_esame (
    id_medico INTEGER NOT NULL,
    id_esame INTEGER NOT NULL,

    PRIMARY KEY (id_medico, id_esame),

    FOREIGN KEY (id_medico)
        REFERENCES medico(id_medico)
        ON DELETE CASCADE,

    FOREIGN KEY (id_esame)
        REFERENCES esame(id_esame)
        ON DELETE CASCADE
);



CREATE TABLE medico_specializzazione (
    id_medico INTEGER NOT NULL,
    id_specializzazione INTEGER NOT NULL,

    PRIMARY KEY (id_medico, id_specializzazione),

    FOREIGN KEY (id_medico)
        REFERENCES medico(id_medico)
        ON DELETE CASCADE,

    FOREIGN KEY (id_specializzazione)
        REFERENCES specializzazione(id_specializzazione)
        ON DELETE CASCADE
);



CREATE TABLE turno (
    id_turno INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_medico INTEGER NOT NULL,
    data_turno DATE NOT NULL,
    ora_inizio TIME NOT NULL,
    ora_fine TIME NOT NULL,

    FOREIGN KEY (id_medico)
        REFERENCES medico(id_medico)
        ON DELETE RESTRICT,

    CONSTRAINT check_turno_orari
        CHECK (ora_fine > ora_inizio),

    -- Impedisce turni sovrapposti dello stesso medico.
    CONSTRAINT ex_turno_sovrapposto
        EXCLUDE USING gist (
            id_medico WITH =,
            tsrange(
                data_turno + ora_inizio,
                data_turno + ora_fine,
                '[)'
            ) WITH &&
        )
);



CREATE TABLE prenotazione (
    id_prenotazione INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_paziente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    id_esame INTEGER NOT NULL,
    id_creatore INTEGER NOT NULL,
    data_appuntamento DATE NOT NULL,
    ora_inizio TIME NOT NULL,
    ora_fine TIME NOT NULL,
    stato VARCHAR(20) NOT NULL DEFAULT 'CONFERMATA',
    data_creazione TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_annullamento TIMESTAMP,

    FOREIGN KEY (id_paziente)
        REFERENCES paziente(id_paziente)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_medico)
        REFERENCES medico(id_medico)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_esame)
        REFERENCES esame(id_esame)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_creatore)
        REFERENCES utente(id_utente)
        ON DELETE RESTRICT,

    CONSTRAINT check_prenotazione_orari
        CHECK (ora_fine > ora_inizio),

    CONSTRAINT check_prenotazione_stato
        CHECK (stato IN ('CONFERMATA', 'COMPLETATA', 'ANNULLATA')),

    CONSTRAINT check_prenotazione_annullamento
        CHECK (
            (stato = 'ANNULLATA' AND data_annullamento IS NOT NULL)
            OR
            (stato <> 'ANNULLATA' AND data_annullamento IS NULL)
        ),

    -- Necessario per verificare che il medico
    -- che carica il referto sia quello assegnato.
    CONSTRAINT uq_prenotazione_medico
        UNIQUE (id_prenotazione, id_medico),

    -- Impedisce appuntamenti sovrapposti
    -- per lo stesso medico.
    CONSTRAINT ex_prenotazione_sovrapposta
        EXCLUDE USING gist (
            id_medico WITH =,
            tsrange(
                data_appuntamento + ora_inizio,
                data_appuntamento + ora_fine,
                '[)'
            ) WITH &&
        )
        WHERE (stato = 'CONFERMATA')
);



CREATE TABLE referto (
    id_referto INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_prenotazione INTEGER NOT NULL UNIQUE,
    id_medico_caricante INTEGER NOT NULL,
    nome_file VARCHAR(250) NOT NULL,
    percorso_file VARCHAR(500) NOT NULL,
    data_caricamento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Il medico caricante deve essere quello
    -- assegnato alla prenotazione.
    CONSTRAINT fk_referto_prenotazione_medico
        FOREIGN KEY (id_prenotazione, id_medico_caricante)
        REFERENCES prenotazione(id_prenotazione, id_medico)
        ON DELETE RESTRICT
);
