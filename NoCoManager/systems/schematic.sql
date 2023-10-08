CREATE TABLE IF NOT EXISTS Identite(
	uid TEXT NOT NULL,
	email TEXT NOT NULL,
	nom TEXT NOT NULL,
	prenom TEXT NOT NULL,
	dob DATE NOT NULL DEFAULT NOW(),
	telephone TEXT,
	adresse TEXT,
	PRIMARY KEY (uid)
);

CREATE TABLE IF NOT EXISTS Session(
    uid TEXT NOT NULL,
    title TEXT NOT NULL,
    valid BOOLEAN NOT NULL DEFAULT '1',
	PRIMARY KEY (uid)
);

CREATE TABLE IF NOT EXISTS Ticket(
    uid TEXT NOT NULL,
    session_uid TEXT NOT NULL,
    identite_uid TEXT NOT NULL,
    used BOOLEAN NOT NULL DEFAULT 'f',
	PRIMARY KEY (uid),

    CONSTRAINT fk_session
      FOREIGN KEY(session_uid) 
	  REFERENCES Session(uid) ON DELETE CASCADE,
      
    CONSTRAINT fk_identite
      FOREIGN KEY(identite_uid) 
	  REFERENCES Identite(uid) ON DELETE CASCADE
);

