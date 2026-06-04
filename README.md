# Matoppskrifter

## Hva er prosjektet?
Matoppskrifter er en webapplikasjon der brukere kan registrere seg, logge inn og dele matoppskrifter med hverandre. Tanken bak prosjektet er å lage et enkelt og oversiktlig sted der folk kan samle og dele oppskrifter. Prosjektet er bygget med Python og Flask som backend, MySQL som database, og HTML/CSS som frontend. Databasen kjører på en Raspberry Pi som fungerer som en lokal server.

### Brukerregistrering og innlogging
Brukere kan opprette en konto med brukernavn og passord. Når man logger inn opprettes en sesjon som holder brukeren innlogget mens de navigerer på siden. Uten en aktiv sesjon blir man automatisk sendt tilbake til innloggingssiden.

### Legge til oppskrifter
Innloggede brukere kan fylle ut et skjema med navn på oppskriften, ingredienser, fremgangsmåte, koketid og antall porsjoner. Når skjemaet sendes inn lagres oppskriften i databasen og blir synlig for alle brukere på hovedsiden.

### database

+-------------------------+
| Tables_in_mat_oppskrift |
+-------------------------+
| oppskrift               |
| saved_recipes           |
| users                   |
+-------------------------+
oppskrift
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int(11)      | NO   | PRI | NULL    | auto_increment |
| name           | varchar(255) | YES  |     | NULL    |                |
| ingredienser   | text         | YES  |     | NULL    |                |
| fremgangsmåte  | text         | YES  |     | NULL    |                |
| koketid        | float(3,2)   | YES  |     | NULL    |                |
| prsjoner       | int(11)      | YES  |     | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+
saved_recipes 
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| username  | varchar(255) | YES  |     | NULL    |                |
| recipe_id | int(11)      | YES  | MUL | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
 users 
 +---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| username      | varchar(50)  | NO   | UNI | NULL    |                |
| password_hash | varchar(255) | NO   |     | NULL    |                |
| epost         | varchar(255) | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+

### Se alle oppskrifter
På hovedsiden vises alle oppskrifter som er lagt til av alle brukere i en tabell. Tabellen viser navn, ingredienser, fremgangsmåte, koketid, porsjoner og hvem som la til oppskriften.

### Slette oppskrifter
Brukere kan slette oppskrifter direkte fra tabellen på hovedsiden. Når en oppskrift slettes fjernes den også automatisk fra alle brukeres lagrede lister.

### Lagre favorittoppskrifter
Brukere kan lagre oppskrifter de liker ved å trykke på en lagreknapp i tabellen. Lagrede oppskrifter dukker opp på en egen side der brukeren kun ser sine egne favoritter. Herfra kan brukeren også fjerne oppskrifter fra listen sin.

## Planlagt fremtidig funksjonalitet

### Passord-hashing
Per nå lagres passord i klartekst i databasen, noe som ikke er trygt. Planen er å implementere passord-hashing slik at passord lagres kryptert og ikke kan leses direkte fra databasen, selv om noen skulle få tilgang til den.

### Terms Of Service

### Lage FAQ
Det skal lages en egen FAQ-side (/faq) der brukere kan lese svar på vanlige spørsmål om appen. Siden er tilgjengelig uten innlogging.
Det er lagt inn fem ferdige spørsmål og svar om temaer som innlogging, oppskrifter og personvern.
Brukere kan også sende inn egne spørsmål via et skjema med navn, e-post og spørsmålstekst.
Alle innsendte spørsmål lagres i en egen tabell i databasen, og brukeren vil få svar tilbake på e-posten de oppgir.
I tillegg er det en egen side (/slett-data) der brukere kan slette alle sine personopplysninger i henhold til GDPR artikkel 17.
Når en bruker ber om sletting anonymiseres alle FAQ-spørsmål de har sendt inn, lagrede oppskrifter slettes, og brukerkontoen fjernes permanent. 
